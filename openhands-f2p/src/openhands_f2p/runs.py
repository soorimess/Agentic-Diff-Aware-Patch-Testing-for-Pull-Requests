"""`RUNS.md` in a run folder -- the state of every instance, for someone who has just cloned this.

`out/` holds one directory per instance and each one holds a dozen files. That is the
right shape for reading a single run in detail and the wrong shape for the first
question anyone asks, which is "what is in here and when was it produced". This writes
the index that answers it: one row per pull request, its verdict, its coverage, when it
last ran, and the directory to open next.

Written from `result.json` and the file timestamps rather than kept by hand, so it
cannot drift from what is actually on disk. Regenerate any time:

    uv run python -m openhands_f2p.runs
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from openhands_f2p.layout import OUT
from openhands_f2p.prs import PRS



VERDICT_NOTE = {
    "YES": "fails at base, passes after the fix",
    "NO": "ran, but is not fail-to-pass",
    "BROKEN": "no usable result -- see `why`",
}


# What `arm` meant before configurations were a registry. Results written since carry
# `features.config` and need no translation; these two are the only values the old
# field ever took, so the table reads the same across the change.
LEGACY_ARM = {"agent": "full", "agent-blind": "no-patch+coverage-tool"}


def _config_of(r: dict) -> str:
    named = (r.get("features") or {}).get("config")
    if named:
        return named
    arm = r.get("arm") or ""
    return LEGACY_ARM.get(arm, arm or "—")


def _ran_at(d: Path, f: Path, r: dict) -> datetime:
    """When the agent ran -- not when the result file was last touched.

    `result.json`'s mtime is the obvious answer and the wrong one: re-judging two
    instances rewrote their files and moved them a day forward in this table. Results
    written since carry `ran_at`. For older ones, fall back to a file only a real run
    writes -- the child's own flow log -- and to the mtime only if neither exists.
    """
    stamped = r.get("ran_at")
    if stamped:
        try:
            return datetime.strptime(stamped, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc)
        except ValueError:
            pass
    for name in ("flow.jsonl", "child.log"):
        q = d / name
        if q.exists() and q.stat().st_size:
            return datetime.fromtimestamp(q.stat().st_mtime, tz=timezone.utc)
    return datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)


# Every key `build` reads, so a row for an instance with no result has the same shape as
# one that has it. This was a shorter dict, which was fine while the only table ever
# built was over `out/` with all twenty-six results present -- and a KeyError the first
# time a series directory held five of them.
BLANK = {"f2p": "\u2014", "when": "", "cov": None, "covered": None, "total": None,
         "actions": None, "why": "never run", "judge": "\u2014", "issue": "\u2014",
         "tools": "\u2014",
         "readable": "\u2014", "uncovered": [], "rechecked": False,
         "config": "\u2014", "tokens": 0, "cost": 0.0, "mutation": {},
         "lost": (0, 0)}


def _tools(d: Path) -> str:
    """Which tools the agent reached for, and how many times each.

    From `tool_log.json` rather than the action count, because the two answer different
    questions. `actions` says how much the agent did; this says what it did it *with*, and
    across the model ladder that is the difference that predicts the verdict -- a run that
    never calls `verify` is a run that never checked the one property it was asked for.

    Ordered by count so the shape reads at a glance: `run x94` beside a single
    `write_file` is a reading loop, whatever the total says.
    """
    f = d / "tool_log.json"
    if not f.exists():
        return "\u2014"
    try:
        log = json.loads(f.read_text())
    except (ValueError, OSError):
        return "\u2014"
    counts: dict[str, int] = {}
    reverted = 0
    for e in log:
        name = e.get("tool") or "?"
        # `guard` is the harness undoing an edit to a pre-existing file, not a tool the
        # agent chose. Counting it here put a call in the column the agent never made and
        # left the row summing to one more than its own action count. It stays in the
        # cell, because an agent working against the rules is the most interesting thing
        # a row can say -- but as an annotation, not an instrument.
        if name == "guard":
            reverted += len(e.get("reverted") or []) or 1
            continue
        counts[name] = counts.get(name, 0) + 1
    body = ", ".join(f"`{k}` x{v}" for k, v in
                     sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))) or "none"
    return f"{body}  (+{reverted} edit{'s' if reverted > 1 else ''} reverted)" \
        if reverted else body


def _lost_turns(d: Path) -> tuple[int, int]:
    """Model replies that carried nothing at all, over replies made.

    A reply with no content and no tool call is a turn the agent did not get. OpenHands
    reads one as the conversation ending, so a model that produces them often cannot
    finish however capable it is -- `qwen3-coder-30b` returned an empty message object on
    113 of 232 calls, 182 completion tokens billed and nothing delivered, and scored 4/10
    while writing 100% coverage on every test it did complete. Without this column that
    reads as a weak model rather than a broken transport.

    Returns `(0, 0)` when `completions/` is absent -- it is git-ignored, so a table built
    from a cloned run folder simply omits the column rather than claiming zero.
    """
    empty = total = 0
    for f in (d / "completions").glob("*.json"):
        try:
            c = json.loads(f.read_text())
        except (ValueError, OSError):
            continue
        total += 1
        m = (((c.get("response") or {}).get("choices") or [{}])[0].get("message") or {})
        if not m.get("tool_calls") and not (m.get("content") or "").strip():
            empty += 1
    return empty, total


def _row(pr: dict, root: Path) -> dict:
    d = root / pr["id"]
    f = d / "result.json"
    if not f.exists():
        return {**pr, **BLANK}
    r = json.loads(f.read_text())
    c = r.get("changed_line_coverage") or {}
    when = _ran_at(d, f, r)
    return {**pr, "f2p": r.get("f2p", "?"),
            "when": when.strftime("%Y-%m-%d %H:%M UTC"),
            "cov": c.get("percent") if c.get("measured") else None,
            "covered": c.get("covered"), "total": c.get("executable_changed_lines"),
            "actions": r.get("actions"), "why": (r.get("why") or "").strip(),
            "tools": _tools(d),
            "judge": (r.get("concept") or {}).get("verdict", "—"),
            "issue": ((r.get("concept") or {}).get("issue_coverage")
                      or {}).get("verdict", "—"),
            "readable": ((r.get("concept") or {}).get("readability")
                         or {}).get("verdict", "—"),
            "uncovered": ((r.get("concept") or {}).get("issue_coverage")
                          or {}).get("uncovered") or [],
            "rechecked": bool(r.get("rechecked")),
            "config": _config_of(r),
            "mutation": r.get("mutation") or {},
            "tokens": (r.get("usage") or {}).get("total_tokens") or 0,
            "cost": (r.get("usage") or {}).get("cost_usd") or 0.0,
            "second_chance": r.get("second_chance"),
            "lost": _lost_turns(d)}


def _brief(why: str | None) -> str:
    """One readable clause for a row that never reached a verdict.

    What failed is data; the transcript of how is not. A Docker registry refusal arrives
    as three hundred characters of image reference and HTTP detail, and four of them
    turned the bottom of this table into a wall of URLs that said one thing: the pull was
    rate-limited. The cause survives, the transport does not.
    """
    if not why:
        return "never run"
    lowered = why.lower()
    for needle, said in (("429", "image pull refused by the registry (rate limited)"),
                         ("failed to resolve reference", "image not available to pull"),
                         ("no space left", "out of disk")):
        if needle in lowered:
            return said
    why = " ".join(why.split())
    return why if len(why) <= 120 else why[:117] + "..."


def _second_chance_table(retried: list[dict]) -> list[str]:
    """Which refusals converted, split by what the agent was told.

    Worth its own table because the totals mislead. `loop_open` is not this flag's --
    it belongs to `require-tools`, which is on by default and fires whether or not a
    second chance was offered, so counting its conversions as the flag's work credits it
    with runs it did not cause. `passes_at_base` and `collects_nothing` are the two
    reasons `--second-chance` adds, and they are the only rows that answer whether it
    earned its place.
    """
    OWN = ("passes_at_base", "collects_nothing")
    by_reason: dict[str, list[dict]] = {}
    for r in retried:
        by_reason.setdefault(r["second_chance"]["reason"], []).append(r)

    lines = ["", "### What the refused runs did next", "",
             "`loop_open` belongs to `require-tools` and fires with or without "
             "`--second-chance`; the rows marked *added by the flag* are the ones this "
             "flag is answerable for.", "",
             "| told | runs | ended YES | ended NO | ended BROKEN | |",
             "|---|---|---|---|---|---|"]
    for reason in sorted(by_reason):
        rs = by_reason[reason]
        tally = {v: sum(1 for r in rs if r["f2p"] == v) for v in ("YES", "NO", "BROKEN")}
        own = "**added by the flag**" if any(k in reason for k in OWN) else "from `require-tools`"
        lines.append(f"| `{reason}` | {len(rs)} | {tally['YES']} | {tally['NO']} | "
                     f"{tally['BROKEN']} | {own} |")
    flag_rows = [r for r in retried
                 if any(k in r["second_chance"]["reason"] for k in OWN)]
    flag_yes = sum(1 for r in flag_rows if r["f2p"] == "YES")
    if flag_rows:
        lines += ["", f"Of the **{len(flag_rows)}** refused for a reason the flag itself "
                      f"adds, **{flag_yes}** ended fail-to-pass.", ""]
    return lines


def changed_source_lines(diff: str) -> int:
    """Lines of Python the patch adds or rewrites, from the diff alone.

    The denominator that does not move. `executable_changed_lines`, which the coverage
    measurement reports, is `len(hit) + len(missed)` over the files that test's coverage
    run actually traced -- so it is a property of the test as much as of the patch, and
    two arms measuring the same instance can disagree about it. `sphinx-7590` came back
    as 47 lines in one arm and 54 in another. A number that moves with the test cannot be
    the fixed denominator that makes two arms comparable.

    This one is static: the same for an instance in every arm and every run, because it
    reads the patch and nothing else. Blanks, comments and docstrings are excluded, none
    of them being executable.

    It is not the same quantity as `executable_changed_lines` and is not meant to be.
    Coverage counts statements it could trace; this counts source lines the patch wrote.
    A ratio built from the two is approximate -- good for comparing arms against a fixed
    corpus, not for claiming an exact percentage of any one patch.
    """
    n, in_py, in_doc = 0, False, False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            in_py, in_doc = line.rstrip().endswith(".py"), False
            continue
        if not in_py or not line.startswith("+") or line.startswith("+++"):
            continue
        body = line[1:].strip()
        if not body:
            continue
        quotes = body.count('"""') + body.count("'''")
        if in_doc:
            if quotes % 2:
                in_doc = False
            continue
        if body.startswith("#"):
            continue
        if body.startswith(('"""', "'''")):
            if quotes % 2:
                in_doc = True
            continue
        n += 1
    return n


def build(root: Path = OUT) -> str:
    """The table for one series of runs.

    `root` is which series: a run made with `--out-root out_nocov` writes its results
    there, and its table has to be built from there too. Reading `out/` regardless would
    describe a different series than the one that just finished.
    """
    # Only instances this directory actually holds. `out/` holds the whole set, so
    # nothing changes there; a series run on a subset used to get all 26 rows, 21 of
    # them dashes linking to directories that were never created. A table of mostly
    # absent rows reads as a run that mostly failed, which is the opposite of true.
    present = [pr for pr in PRS if (root / pr["id"] / "result.json").is_file()]
    rows = [_row(pr, root) for pr in (present or PRS)]
    decided = [r for r in rows if r["f2p"] in ("YES", "NO")]
    yes = [r for r in rows if r["f2p"] == "YES"]
    # Fail-to-pass only. Coverage is measured during `verify`, before a run can be voided
    # for editing the tree, so a voided run reaches this table carrying a figure -- and a
    # number taken off a tree the agent altered is not a fact about the pull request. It is
    # also what the note under the table already claims, which was true until --no-guard
    # produced the first run that was measured and then thrown out.
    measured = [r for r in rows if r["cov"] is not None and r["f2p"] == "YES"]
    covs = [r["cov"] for r in measured]
    # Two averages, because they answer different questions and a patch of two
    # lines and a patch of forty are not the same evidence. The mean weights each
    # test equally and says how the typical generated test did. The pooled figure
    # weights each changed line equally -- every line this set of pull requests
    # touched, against the ones some generated test actually executed -- and is the
    # one that answers "how much of the work did we cover".
    hit = sum(r["covered"] for r in measured if r["covered"] is not None)
    lines_changed = sum(r["total"] for r in measured if r["total"] is not None)
    # Every instance in the set, whether or not a test was ever measured against it. A
    # pull request nobody covered is a pull request nobody covered, and dropping it from
    # the denominator is how an arm that produced fewer tests scores better per line.
    corpus_lines = 0
    for pr in (present or PRS):
        fd = root / pr["id"] / "fix.diff"
        if fd.is_file():
            corpus_lines += changed_source_lines(fd.read_text(errors="replace"))
    stamps = sorted(r["when"] for r in rows if r["when"])

    out = ["# Run status, per pull request", "",
           f"Last run in this table: {stamps[-1] if stamps else 'none'}.", ""]

    out += [f"- **{len(rows)}** instances across "
            f"**{len({r['id'].split('__')[0] for r in rows})}** repositories",
            f"- **{len(yes)}/{len(decided)}** fail-to-pass, of those that reached a "
            f"verdict",
            (f"- **{len(covs)}** measured for changed-line coverage: "
             f"**mean {sum(covs) / len(covs):.0f}%** per test, "
             f"median {sorted(covs)[len(covs) // 2]:.0f}%") if covs else "",
            (f"- **{100 * hit / lines_changed:.0f}%** of the changed lines those tests "
             f"were measured against ({hit}/{lines_changed}, pooled)")
            if lines_changed else "",
            (f"- **{100 * hit / corpus_lines:.0f}%** of every source line all "
             f"{len(present or PRS)} patches change ({hit}/{corpus_lines}) -- a fixed "
             f"denominator, so this is the figure that compares across arms")
            if corpus_lines else "",
            # Escaped: a bare `$` opens LaTeX math in renderers that support it, and a
            # second `$` later in the line closes it -- the cost line and every figure
            # after it then render as typeset algebra.
            f"- \\${sum(r['cost'] for r in rows):.2f} and "
            f"{sum(r['tokens'] for r in rows) / 1e6:.1f}M tokens in total",
            ""]

    # A second chance is not part of the feature configuration, so the `full` line below
    # says nothing about it -- and two runs that differ only by this are not comparable.
    # Naming it here is what keeps that visible in the table rather than only in the
    # per-instance JSON.
    lost = sum(r["lost"][0] for r in rows)
    calls = sum(r["lost"][1] for r in rows)
    if calls and lost:
        out[-1:] = [f"- **{lost} of {calls}** model replies arrived empty -- no text and no "
                    f"tool call, and three of those in a row trip OpenHands' stuck "
                    f"detector, which ends the run. A run losing turns at that rate is "
                    f"bounded by its transport rather than by the model, and the verdicts "
                    f"below should be read with that in mind", ""]

    retried = [r for r in rows if r.get("second_chance")]
    if retried:
        won = [r for r in retried if r["f2p"] == "YES"]
        out[-1:] = [f"- **{len(retried)}** of these were sent a second-chance message "
                    f"after stopping with nothing to score, and **{len(won)}** of them "
                    f"ended fail-to-pass; the other {len(rows) - len(retried)} finished "
                    f"or failed for a reason the agent could not have seen at base", ""]
        out += _second_chance_table(retried)

    # The column only exists when something filled it. A `mutants` column of dashes on
    # every row of every table describes nothing and pushes the rest sideways.
    has_mutation = any(r["mutation"].get("measured") for r in rows)
    # A note rather than a column: it is a property of the whole run, and a score taken
    # on mutants the agent had already been shown is not comparable with one taken on
    # mutants it had not. Silently mixing the two in one column would be the error.
    held_out = any(r["mutation"].get("held_out") for r in rows)
    configs = sorted({r["config"] for r in rows if r["config"] != "—"})
    if len(configs) == 1:
        out += [f"Every row was produced with the same configuration: "
                f"**`{configs[0]}`** &mdash; what the agent was given. `full` means "
                f"nothing was withheld.", ""]
    elif configs:
        out += ["> **These rows come from more than one configuration** "
                f"({', '.join(f'`{c}`' for c in configs)}), so the totals above mix "
                "runs in which the agent was given different things. Compare a series "
                "against a series, one `--out-root` each, rather than reading this "
                "table as a single measurement.", ""]

    out += ["Coverage is measured only for tests that are fail-to-pass; for anything "
            "else the question does not apply. A `—` in that column means not "
            "measured, not zero.", ""]
    if held_out:
        out += ["The agent held the `mutation` tool in this run, so the mutants scored "
                "here are the **held-out half** of the pool &mdash; the agent was shown "
                "the other half and never these. That keeps the number a measurement "
                "rather than a mark for revising against the sample, but it also halves "
                "the denominator, so a per-instance figure is noisier than one from a "
                "run without the tool. The two are not comparable row for row.", ""]
    out += [
            "`concept`, `issue` and `readable` are three separate answers from one "
            "judgement call by a stronger model that wrote none of these tests: whether "
            "the test is about the same behaviour as the maintainer's, whether it "
            "reaches every behaviour the pull request settles, and whether it would pass "
            "review. None of them feeds the F2P verdict.", "",
            *([] if not has_mutation else
              ["The two `mutants` columns are the same set of mutants asked of two "
               "tests. `mutmut` mutates the lines the patch changed -- negating a "
               "condition, moving a boundary, replacing a literal -- and each column is "
               "how many of those mutants that test fails on, which is how many wrong "
               "versions of the fix it would have caught. Nothing is filtered out, so "
               "the columns are comparable: a mutant the developer's test kills and the "
               "agent's does not is a gap, and one neither kills is probably "
               "behaviourally equivalent to the fix and says nothing about either test. "
               "The individual diffs are in each instance's `mutations/`.", ""]),
            f"| instance | version | verdict | coverage |"
            f"{' mutants: agent test | mutants: dev test |' if has_mutation else ''}"
            f" actions | tools used | concept | issue | readable | last run |",
            f"|---|---|---|---|{'---|---|' if has_mutation else ''}"
            f"---|---|---|---|---|---|"]
    for r in rows:
        cov = (f"{r['cov']:.0f}% ({r['covered']}/{r['total']})"
               if r["cov"] is not None else "—")
        m = r["mutation"]
        # Killed over total, not a percentage: `2/2` says more than `100%` when the
        # denominator is two, and the denominator is the interesting part.
        def _cell(side: str) -> str:
            if not m.get("measured"):
                return "—"
            if not m.get("total"):
                return "no mutants"
            return f"{m[side]['killed']}/{m['total']}"
        cell = (f" {_cell('agent')} | {_cell('developer')} |" if has_mutation else "")
        out.append(f"| [`{r['id']}`](./{r['id']}/) | {r['version']} | "
                   f"{r['f2p']}{' ¹' if r['rechecked'] else ''} | {cov} |{cell} "
                   f"{r['actions'] if r['actions'] is not None else '—'} | "
                   f"{r['tools']} | "
                   f"{r['judge']} | {r['issue']} | {r['readable']} | "
                   f"{r['when'] or '—'} |")
    if any(r["rechecked"] for r in rows):
        out += ["", "¹ re-judged by `--recheck`: the same saved test run again under a "
                    "later harness, with no new model call. The trajectory and token "
                    "counts belong to the original run; the verdict and coverage are "
                    "from the re-judgement."]

    gaps = [r for r in rows if r["uncovered"]]
    if gaps:
        out += ["", "## Behaviours the judge says are not covered", "",
                "Read alongside the coverage column: these come from reading the issue "
                "and the fix, not from line execution, so the two disagree in useful "
                "ways.", ""]
        for r in gaps:
            out.append(f"- **{r['id']}** ({r['issue']})")
            for u in r["uncovered"][:3]:
                out.append(f"  - {u}")

    unresolved = [r for r in rows if r["f2p"] not in ("YES", "NO")]
    if unresolved:
        out += ["", "## Without a verdict", ""]
        for r in unresolved:
            out.append(f"- **{r['id']}** — {_brief(r['why'])}")

    return "\n".join(line for line in out if line is not None) + "\n"


def main(root: Path | None = None) -> int:
    root = root or OUT
    root.mkdir(parents=True, exist_ok=True)
    path = root / "RUNS.md"
    path.write_text(build(root))
    try:
        shown = path.relative_to(Path(__file__).resolve().parents[3])
    except ValueError:
        shown = path
    print(f"wrote {shown}")
    return 0


def _cli() -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-root", default=None,
                   help="build the table for the series in this directory "
                        "(default: out/)")
    a = p.parse_args()
    return main(Path(a.out_root) if a.out_root else None)


if __name__ == "__main__":
    sys.exit(_cli())
