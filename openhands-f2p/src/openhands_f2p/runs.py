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

from openhands_f2p.compare import SCALE_VERSION, SCALES, SCALES_V5, shown
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
         "actions": None, "why": "never run", "body": None, "meaningful": "\u2014", "judge": "\u2014", "issue": "\u2014",
         "tools": "\u2014",
         "readable": "\u2014", "uncovered": [], "rechecked": False,
         "config": "\u2014", "tokens": 0, "cost": 0.0, "mutation": {},
         "lost": (0, 0), "second_chance_on": False}


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
            # Without the changed lines that run on import (user, 2026-10-04: both).
            "body": c.get("excluding_import_time") if c.get("measured") else None,
            "actions": r.get("actions"), "why": (r.get("why") or "").strip(),
            "tools": _tools(d),
            # `narrower (3)` on the five-level judge, the bare word on the old one.
            "judge": shown(r.get("concept")),
            # The judge's first label, absolute: yes / no / "—" when not judged.
            "meaningful": ((r.get("concept") or {}).get("meaningful") or {}).get("answer", "\u2014"),
            "issue": shown((r.get("concept") or {}).get("issue_coverage")),
            "readable": shown((r.get("concept") or {}).get("readability")),
            "scale": (r.get("concept") or {}).get("scale"),
            "uncovered": ((r.get("concept") or {}).get("issue_coverage")
                          or {}).get("uncovered") or [],
            "rechecked": bool(r.get("rechecked")),
            "config": _config_of(r),
            "mutation": r.get("mutation") or {},
            "tokens": (r.get("usage") or {}).get("total_tokens") or 0,
            "cost": (r.get("usage") or {}).get("cost_usd") or 0.0,
            # Stop refusals; results before 2026-09-28 kept them under `second_chance`,
            # which since holds the restart record (it has `first_verdict`).
            "refusals": r.get("refusals") or (
                r.get("second_chance")
                if "reason" in (r.get("second_chance") or {}) else None),
            "f2p_history": r.get("f2p_history"),
            "restart": (r.get("second_chance")
                        if "first_verdict" in (r.get("second_chance") or {}) else None),
            "second_chance_on": "second-chance" in ((r.get("features") or {}).get("on")
                                                    or []),
            "lost": _lost_turns(d)}


def _judge_legend(scales_seen: set) -> list[str]:
    """What each judge number means, above the table that uses them.

    Printed from `compare.SCALES` rather than written here, so the legend is the same
    table the labels were looked up in and cannot describe a scale the judge was not
    given. A folder judged on the older absolute scale gets that legend instead, or both
    when rows from both are present.
    """
    out = []
    if SCALE_VERSION in scales_seen:
        names = {"concept": "concept -- which pins the fix's behaviour better?",
                 "issue": "issue -- which covers more of what the fix settles?",
                 "readable": "readable -- which reads better?"}
        out += ["The three judge columns compare the generated test with the developer's, "
                "from 1 (the developer's clearly better) through 3 (on a par) to 5 (the "
                "generated clearly better), printed as `label (level)`:", "",
                "| scale | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
        for key, scale in SCALES.items():
            out.append(f"| {names[key]} | " + " | ".join(scale[n] for n in range(1, 6)) + " |")
        out.append("")
    if 5 in scales_seen:
        names = {"concept": "concept -- same behaviour as the maintainer's test?",
                 "issue": "issue -- every behaviour the pull request settles?",
                 "readable": "readable -- would it pass review?"}
        out += ["Rows judged before 2026-09-28 use the older absolute scale, 1 (worst) to "
                "5 (best):", "", "| scale | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|"]
        for key, scale in SCALES_V5.items():
            out.append(f"| {names[key]} | " + " | ".join(scale[n] for n in range(1, 6)) + " |")
        out.append("")
    return out


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


def _refusal_table(retried: list[dict]) -> list[str]:
    """Which refusals converted, split by what the agent was told.

    Every stop refusal is `require-tools`' since 2026-09-28 (second revision): the
    harness's base run (`no_test`, `collects_nothing`, `passes_at_base`,
    `skipped_at_base`), the agent's own last `verify` (`verify_open`), the source-text
    check (`reads_source`), and once the test flips the coverage/mutation duties
    (`duties_open`) and the no-reach question (`runs_no_change`, coverage tool only).
    The column says which part of the check each reason is. Older results carry
    `loop_open`, `require-tools`' verify loop and duties together.
    """
    OWN = ("passes_at_base", "collects_nothing", "no_test", "skipped_at_base", "verify_open")

    def owner(reason: str) -> str:
        parts = []
        if any(k in reason for k in OWN):
            parts.append("not fail-to-pass yet")
        if "duties_open" in reason:
            parts.append("checks after fail-to-pass")
        if "loop_open" in reason:
            parts.append("verify loop or duties (before 2026-09-28)")
        if "reads_source" in reason:
            parts.append("reads source as text")
        if "runs_no_change" in reason:
            parts.append("flips without reaching the change")
        return " + ".join(parts) or "—"

    by_reason: dict[str, list[dict]] = {}
    for r in retried:
        by_reason.setdefault(r["refusals"]["reason"], []).append(r)

    lines = ["", "### What the refused runs did next", "",
             "Every refusal comes from `require-tools`; the last column says which part of the "
             "check the first reason was.", "",
             "| told | runs | ended YES | ended NO | ended BROKEN | |",
             "|---|---|---|---|---|---|"]
    for reason in sorted(by_reason):
        rs = by_reason[reason]
        tally = {v: sum(1 for r in rs if r["f2p"] == v) for v in ("YES", "NO", "BROKEN")}
        own = owner(reason)
        lines.append(f"| `{reason}` | {len(rs)} | {tally['YES']} | {tally['NO']} | "
                     f"{tally['BROKEN']} | {own} |")
    flag_rows = [r for r in retried
                 if any(k in r["refusals"]["reason"] for k in OWN)]
    flag_yes = sum(1 for r in flag_rows if r["f2p"] == "YES")
    if flag_rows:
        lines += ["", f"Of the **{len(flag_rows)}** first refused as not fail-to-pass yet, "
                      f"**{flag_yes}** ended fail-to-pass.", ""]
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
    bodies = [r["body"] for r in measured if r.get("body")]
    body_hit = sum(b["covered"] for b in bodies)
    body_lines = sum(b["executable_changed_lines"] for b in bodies)
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
    chance_on = any(r.get("second_chance_on") for r in rows)
    judged_m = [r for r in yes if r.get("meaningful") in ("yes", "no")]
    rescued = [r for r in rows if r.get("restart") and not r["restart"].get("skipped")
               and r["f2p"] == "YES"]

    out = ["# Run status, per pull request", "",
           f"Last run in this table: {stamps[-1] if stamps else 'none'}.", ""]

    out += [f"- **{len(rows)}** instances across "
            f"**{len({r['id'].split('__')[0] for r in rows})}** repositories",
            f"- **{len(yes)}/{len(decided)}** fail-to-pass, of those that reached a "
            f"verdict",
            # Said up front whenever the second chance was on (user, 2026-10-04): how
            # much of the YES count the restart bought, so an arm with it and an arm
            # without it can be compared on first attempts too.
            (f"- **{len(rescued)}** of those rescued by the second chance (no YES on the "
             f"first attempt, YES after the restart); first attempts alone: "
             f"**{len(yes) - len(rescued)}/{len(decided)}**") if chance_on else "",
            # The run's main coverage number (user, 2026-10-04): the mean of the per-PR
            # percentages over its YES PRs. Two runs are compared on another one -- pooled
            # covered/all changed lines over the PRs YES in both -- in the compare report.
            (f"- **Changed-line coverage (main): mean {sum(covs) / len(covs):.1f}%** of "
             f"the per-PR figures over the {len(covs)} measured YES PRs; median "
             f"{sorted(covs)[len(covs) // 2]:.0f}%") if covs else "",
            (f"- **{100 * hit / lines_changed:.0f}%** of the changed lines those tests "
             f"were measured against ({hit}/{lines_changed}, pooled)")
            if lines_changed else "",
            (f"- **{100 * body_hit / body_lines:.0f}%** pooled without the lines that run "
             f"on import ({body_hit}/{body_lines})")
            if body_lines and body_lines != lines_changed else "",
            (f"- **{100 * hit / corpus_lines:.0f}%** of every source line all "
             f"{len(present or PRS)} patches change ({hit}/{corpus_lines}), a fixed "
             f"denominator (secondary; arms are compared on pooled lines over the PRs YES "
             f"in both, in the compare report)")
            if corpus_lines else "",
            # Escaped: a bare `$` opens LaTeX math in renderers that support it, and a
            # second `$` later in the line closes it -- the cost line and every figure
            # after it then render as typeset algebra.
            (f"- **{sum(r['meaningful'] == 'yes' for r in yes)}/{len(judged_m)}** of the "
             f"judged YES tests are meaningful by the judge's first label")
            if judged_m else "",
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

    retried = [r for r in rows if r.get("refusals")]
    if retried:
        won = [r for r in retried if r["f2p"] == "YES"]
        out[-1:] = [f"- **{len(retried)}** of these had a stop refused at least once, and "
                    f"**{len(won)}** of them ended fail-to-pass", ""]
        out += _refusal_table(retried)
    restarted = [r for r in rows if r.get("restart") and not r["restart"].get("skipped")]
    skipped = [r for r in rows if (r.get("restart") or {}).get("skipped")]
    # Written whenever the second chance was on, a zero included: "rescued none" is a
    # finding about the add-on, and a missing section reads as "not measured".
    if restarted or chance_on:
        first_no = sum(1 for r in restarted if r["restart"]["first_verdict"] == "NO")
        out += ["", "### The second chance", "",
                f"**Rescued {len(rescued)}** of {len(restarted)} restarted run(s): "
                f"{len(restarted)} ended without a YES and were restarted with the record "
                f"of their first attempt ({first_no} after a NO, "
                f"{len(restarted) - first_no} after a BROKEN), and {len(rescued)} ended "
                f"fail-to-pass on the second attempt: "
                + (", ".join(f"`{r['id']}`" for r in rescued) or "none") + "."
                + (f" {len(skipped)} more ended without a YES with too few actions left "
                   f"to restart: " + ", ".join(f"`{r['id']}`" for r in skipped) + "."
                   if skipped else ""), ""]

    # The agent had a fail-to-pass test by its own `verify` and handed in something else.
    # Record only -- the agent's last file is what is scored.
    worse = [r for r in rows if (r.get("f2p_history") or {}).get("made_worse")]
    tracked = [r for r in rows if r.get("f2p_history")]
    if tracked:
        out += ["", "### Fail-to-pass, then lost", "",
                f"**{len(tracked)}** run(s) had a test their own `verify` called "
                f"fail-to-pass; **{len(worse)}** handed in a test that is not: "
                + (", ".join(f"`{r['id']}`" for r in worse) or "none")
                + ". Each such test is kept in the run's `f2p_snapshots/`.", ""]

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
                f"every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.", ""]
    elif configs:
        out += ["> **These rows come from more than one configuration** "
                f"({', '.join(f'`{c}`' for c in configs)}), so the totals above mix "
                "runs in which the agent was given different things. Compare a series "
                "against a series, one `--out-root` each, rather than reading this "
                "table as a single measurement.", ""]

    out += ["Coverage is measured only for tests that are fail-to-pass; for anything "
            "else the question does not apply. A `—` in that column means not "
            "measured, not zero.", ""]
    if any(r["mutation"].get("measured") for r in rows):
        out += ["Mutants are scored on the **held-out half** of each instance's pool, in "
                "every configuration, so runs with and without the `mutation` tool are "
                "scored on the same mutants"
                + (" &mdash; the agent held the tool here and was shown the other half, "
                   "never these." if held_out else ".")
                + " Results from before 2026-09-28 scored runs without the tool on the "
                "whole pool and are not comparable row for row.", ""]
    out += [
            "`concept`, `issue` and `readable` are three separate answers from one "
            "judgement call by a model that wrote none of these tests, comparing the "
            "generated test with the developer's: which pins the behaviour the fix "
            "establishes better, which covers more of what the pull request settles, "
            "and which reads better. None of them feeds the F2P verdict.", "",
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
            *_judge_legend({r["scale"] for r in rows}),
            f"| instance | version | verdict | coverage |"
            f"{' mutants: agent test | mutants: dev test |' if has_mutation else ''}"
            f" actions | tools used | meaningful | concept | issue | readable | last run |",
            f"|---|---|---|---|{'---|---|' if has_mutation else ''}"
            f"---|---|---|---|---|---|---|"]
    for r in rows:
        cov = (f"{r['cov']:.0f}% ({r['covered']}/{r['total']})"
               if r["cov"] is not None else "—")
        b = r.get("body") or {}
        if r["cov"] is not None and b.get("import_time_lines"):
            cov += (f"; {b['percent']:.0f}% ({b['covered']}/{b['executable_changed_lines']}) "
                    f"without import-time" if b.get("percent") is not None
                    else "; all import-time")
        m = r["mutation"]
        # Killed over total, not a percentage: `2/2` says more than `100%` when the
        # denominator is two, and the denominator is the interesting part.
        def _cell(side: str) -> str:
            if not m.get("measured"):
                return "—"
            if not m.get("total"):
                # The only mutant(s) went to the agent's half: there was a pool, none of
                # it was left to score on -- not the same as mutmut offering nothing.
                return ("none held out" if "reserved" in (m.get("why") or "")
                        else "no mutants")
            if m[side].get("killed") is None:
                return "n/a"
            return f"{m[side]['killed']}/{m['total']}"
        cell = (f" {_cell('agent')} | {_cell('developer')} |" if has_mutation else "")
        out.append(f"| [`{r['id']}`](./{r['id']}/) | {r['version']} | "
                   f"{r['f2p']}{' ¹' if r['rechecked'] else ''} | {cov} |{cell} "
                   f"{r['actions'] if r['actions'] is not None else '—'} | "
                   f"{r['tools']} | "
                   f"{r['meaningful']} | {r['judge']} | {r['issue']} | {r['readable']} | "
                   f"{r['when'] or '—'} |")
    if has_mutation:
        out += ["", "Mutation cells: *none held out* -- the only mutant(s) went to the half "
                    "shown by the agent's `mutation` tool, so none were left to score on; "
                    "*no mutants* -- mutmut offers none on the changed lines; *n/a* -- none "
                    "of the developer's tests pass offline here, so its column is not "
                    "measured."]
    if any(r.get("body") and r["body"].get("import_time_lines") for r in rows):
        out += ["", "Coverage cells: the second figure leaves out changed lines that run on "
                    "import (imports, module constants, decorators, `def` and class lines) "
                    "-- any test that imports the module runs them."]
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
