"""Does the test notice when the fix is subtly wrong?

Fail-to-pass says the test fails at base and passes at head. Changed-line coverage says
the test executed the lines the fix touched. Neither says the test would *object* to a
fix that is nearly right: a test can flip, run every changed line, and still pass against
a version of the patch with a comparison inverted or a boundary moved.

So after the verdict is settled, each line the patch changed is mutated -- the condition
negated, the operator flipped, a literal replaced -- and the test is run against the
result. A mutant the test fails on is *killed*; one it still passes is a *survivor*, and
each survivor is a specific thing the test does not pin down. The maintainer's own test
is run against exactly the same mutants, so the two numbers sit side by side.

**Deterministic, and no model call.** The mutants come from `mutmut` 3's operators applied
to the patched source, so the same pull request yields the same mutants every time and
the measurement is repeatable. An earlier version asked a frontier model to invent
plausible wrong fixes. It produced good mutants, but it was neither reproducible nor
free, its five-to-six-minute call dominated the whole run, and seven of twenty-three
instances failed on the gateway rather than on anything about the code.

**Confined to the change.** `mutmut` will happily mutate a whole file; only mutations on
a line the patch touched are kept. The question is whether the test pins down *this fix*,
so a mutant elsewhere in the file answers a different question.

**Raw, and both sides.** Nothing is filtered. `killed/total` is reported for the
generated test and for the maintainer's test against the identical set of mutants, which
says more than folding them into one figure: where the maintainer's test kills a mutant
the generated one survives, that is a gap; where neither kills it, the mutant is likely
behaviourally equivalent and says nothing about either test. Both readings stay visible
because both numbers are printed.

**Ordering.** This runs the maintainer's test, so it sits where the judge sits: after the
generated test is finalised and scored, never before. The agent is never shown a mutant,
a survivor, or a score -- a score in front of the agent is a score to raise.
"""
from __future__ import annotations

import difflib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openhands_f2p import flow
from openhands_f2p import runners as R
from openhands_f2p import swebench_env as E
from openhands_f2p import verify as V
from openhands_f2p.sandbox import Sandbox

DEFAULT_MUTANTS = 10

# Where the pre-patch copies are parked while mutants are generated. Inside the
# container but outside the repository, so nothing walks into it.
BASE_COPIES = "/tmp/f2p_base"


@dataclass
class Mutant:
    """One mutated version of one changed line."""

    name: str
    file: str
    line: int
    """1-based, in the file as the patch leaves it."""
    operator: str
    """What changed, as `before   ->   after` for that line."""
    source: str = ""
    """The whole mutated file, held only long enough to write it into the container."""
    diff: str = ""
    agent_kills: bool | None = None
    developer_kills: bool | None = None

    def as_dict(self) -> dict:
        return {"name": self.name, "file": self.file, "line": self.line,
                "operator": self.operator,
                "killed_by_agent_test": self.agent_kills,
                "killed_by_developer_test": self.developer_kills,
                "verdict": ("both" if self.agent_kills and self.developer_kills else
                            "agent only" if self.agent_kills else
                            "developer only" if self.developer_kills else
                            "survived both")}


def _configure_mutmut() -> None:
    """Give mutmut a configuration instead of letting it guess one.

    `create_mutations` reads `Config.get()` to find the "do not mutate" pragma patterns,
    and loading that config walks the working directory looking for a package to mutate.
    Here there is nothing to find -- the code being mutated lives inside a container and
    arrives as a string -- so it raised `FileNotFoundError`, which a blanket `except`
    then reported as "this patch has no mutable lines". A misconfiguration that reads as
    a measurement is the failure mode this whole harness is built to avoid.

    The Config dataclass has twenty-one fields and no defaults, so it is filled by
    introspecting the field types rather than by listing them: a field added in a later
    mutmut gets a zero of the right type instead of a TypeError. Only
    `do_not_mutate_patterns` is consulted on this path, and empty is what we want -- the
    lines to mutate are already chosen by the diff.
    """
    import dataclasses
    from mutmut import configuration as C

    if getattr(C, "_config", None) is not None:
        return
    zeros: dict[str, object] = {}
    for f in dataclasses.fields(C.Config):
        name = str(f.type)
        zeros[f.name] = ([] if name.startswith("list") else
                         False if name == "bool" else
                         0 if name == "int" else
                         0.0 if name == "float" else "")
    C._config = C.Config(**zeros)


def _candidates(source: str, filename: str, changed: set[int]) -> list[tuple]:
    """Every mutation `mutmut` offers on a changed line, in a stable order.

    `create_mutations` takes the set of lines to consider, so confining the work to the
    patch is the library's own parameter rather than a filter of ours. What it returns
    is a parsed module plus a list of (original node, mutated node) pairs; a single
    mutant is that module with exactly one pair swapped, which `deep_replace` does.

    The line number comes from diffing the result against the input rather than from
    position metadata: it is the line that actually moved, which is what the record
    should name, and it needs no second pass over the tree.
    """
    from libcst import ParserSyntaxError
    from mutmut.mutation.file_mutation import create_mutations

    _configure_mutmut()
    try:
        module, mutations, _, _ = create_mutations(filename, source, changed or None)
    except ParserSyntaxError:
        # The only failure worth absorbing: a file this libcst cannot parse. Anything
        # else -- a missing config, a changed API -- has to surface, because silently
        # returning "no mutants" makes a broken measurement look like a finished one.
        return []
    rows, seen_on_line = [], {}
    original = source.splitlines()
    for mutation in mutations:
        try:
            mutated = module.deep_replace(
                mutation.original_node, mutation.mutated_node).code
        except Exception:
            continue
        if mutated == source:
            continue
        rows_b = mutated.splitlines()
        line = next((i + 1 for i, (a, b) in enumerate(zip(original, rows_b)) if a != b),
                    0)
        if not line or line not in changed:
            continue                   # mutmut reformatted something outside the patch
        index = seen_on_line.get(line, 0)
        seen_on_line[line] = index + 1
        rows.append((filename, line, index, mutated))
    return sorted(rows, key=lambda t: (t[1], t[2]))


def _spread(candidates: list[tuple], limit: int) -> list[tuple]:
    """Pick `limit` of them, spread across lines rather than taken off the front.

    The first N candidates of a file are usually N variations of its first mutable line,
    which measures one line N times. Round-robin over (file, line) groups instead, so a
    patch touching four lines is asked about all four before any line is asked twice.
    """
    groups: dict[tuple, list] = {}
    for c in candidates:
        groups.setdefault((c[0], c[1]), []).append(c)
    picked, keys = [], sorted(groups)
    while len(picked) < limit and any(groups[k] for k in keys):
        for k in keys:
            if groups[k] and len(picked) < limit:
                picked.append(groups[k].pop(0))
    return picked


def generate(box: Sandbox, patch: str, limit: int) -> list[Mutant]:
    """The mutants for one patch, read off the code as the patch leaves it.

    The box must be at head: the lines the patch adds exist at no other moment, and they
    are exactly the lines worth mutating.
    """
    candidates: list[tuple] = []
    heads: dict[str, str] = {}
    for path in E.patched_source_files(patch):
        if E.is_test_file(path):
            continue                   # mutating a test measures nothing
        head = box.read(path)
        if head is None:
            continue
        base = box.read(f"{BASE_COPIES}/{path}")
        changed = (set(E.added_lines_between(base, head)) if base is not None
                   else set(range(1, head.count("\n") + 2)))
        if not changed:
            continue
        heads[path] = head
        candidates += _candidates(head, path, changed)

    out: list[Mutant] = []
    for path, line, index, mutated in _spread(candidates, limit):
        source = heads[path]
        rows_a, rows_b = source.splitlines(), mutated.splitlines()
        before = rows_a[line - 1].strip() if len(rows_a) >= line else ""
        after = rows_b[line - 1].strip() if len(rows_b) >= line else ""
        out.append(Mutant(
            name=f"{Path(path).stem}-L{line}-{index}",
            file=path, line=line, operator=f"{before}   ->   {after}",
            source=mutated,
            diff="".join(difflib.unified_diff(
                source.splitlines(keepends=True), mutated.splitlines(keepends=True),
                fromfile=f"a/{path}", tofile=f"b/{path}", n=2))))
    return out


def _fails(box: Sandbox, targets: list[str], expected: list[str]) -> bool:
    """True when the test objects to the code as it currently stands.

    "Objects" is `FAILED` or `ERROR` on a node expected to pass, or the node vanishing
    from the report -- a mutant that breaks collection kills the test as surely as a
    failed assertion, and reading a missing node as "passed" would count that as a
    survivor.
    """
    out = R.parse_output(box.exec(R.test_command(box, targets), timeout=1800).output)
    if not out:
        return True                    # nothing collected at all
    return any(R.outcome_of(out, node) in (None, "FAILED", "ERROR")
               for node in expected)


@dataclass
class Score:
    measured: bool = False
    why: str = ""
    asked: int = 0
    total: int = 0
    agent_killed: int = 0
    developer_killed: int = 0
    mutants: list[dict] = field(default_factory=list)

    def _pct(self, n: int) -> float | None:
        return round(100.0 * n / self.total, 1) if self.total else None

    def as_dict(self) -> dict:
        return {"measured": self.measured, "why": self.why or None,
                "tool": "mutmut", "asked": self.asked, "total": self.total,
                "agent": {"killed": self.agent_killed, "total": self.total,
                          "percent": self._pct(self.agent_killed)},
                "developer": {"killed": self.developer_killed, "total": self.total,
                              "percent": self._pct(self.developer_killed)},
                "mutants": self.mutants}


def line(score: dict) -> str:
    if not score.get("measured"):
        return f"not measured -- {score.get('why') or 'no reason recorded'}"
    if not score.get("total"):
        return "no mutants -- mutmut offers none on the lines this patch changed"
    a, d = score["agent"], score["developer"]
    gaps = sum(1 for m in score.get("mutants", [])
               if m.get("verdict") == "developer only")
    return (f"agent test {a['killed']}/{a['total']}, "
            f"developer test {d['killed']}/{d['total']}"
            + (f"   ({gaps} killed only by the developer's)" if gaps else ""))


def _write_records(d: Path, mutants: list[Mutant], score: Score) -> None:
    """One diff per mutant, plus an index, under `out/<instance>/mutations/`.

    The diff rather than the whole mutated file: the diff *is* the mutation, it reads in
    one glance, and the file it applies to is already recoverable -- `fix.diff` is beside
    it and the image is fixed. A directory holding forty near-identical copies of a
    three-thousand-line module would bury the one line that matters in each.
    """
    out = d / "mutations"
    out.mkdir(parents=True, exist_ok=True)
    for stale in out.glob("*.diff"):
        stale.unlink()                 # a re-measure replaces the set, never merges it
    for i, m in enumerate(mutants, 1):
        (out / f"{i:02d}-{m.name}.diff").write_text(
            f"# {m.name}\n"
            f"# {m.file}:{m.line}\n"
            f"# {m.operator}\n"
            f"# killed by: agent test = {m.agent_kills}, "
            f"developer test = {m.developer_kills}\n\n"
            f"{m.diff}")
    (out / "index.json").write_text(json.dumps(score.as_dict(), indent=2))


def measure(instance: dict[str, Any], box: Sandbox, generated_test: str,
            gen_path: str, n: int = DEFAULT_MUTANTS, out_dir: Path | None = None,
            quiet: bool = False) -> Score:
    """Mutation score for one generated test, and for the developer's, on one set.

    The box arrives at base and is left at base. In between the real patch goes on --
    mutants are variants of the *fixed* code, so the fix has to be there first -- and
    both tests are installed, because every mutant is asked of both.
    """
    score = Score(asked=n)
    if n <= 0:
        score.why = "not requested"
        return score

    state = box.patch_state(instance["patch"])
    if state != "base":
        score.why = f"the tree was {state}, not base, when mutation started"
        return score

    gold_expected = json.loads(instance["FAIL_TO_PASS"])
    mutants: list[Mutant] = []
    try:
        # The pre-patch copies are parked first. The changed line numbers come from
        # comparing before against after, not from trusting the diff's own offsets --
        # `git apply` relocates a hunk whose context has moved, and the header then
        # points at unrelated code. That has already cost this harness two instances.
        for path in E.patched_source_files(instance["patch"]):
            text = box.read(path)
            if text is not None:
                box.write(f"{BASE_COPIES}/{path}", text)
        box.apply_patch(instance["patch"])
        box.apply_patch(instance["test_patch"])
        box.write(gen_path, generated_test)

        gold_targets = V.targets_for_gold(box, instance)
        collected = R.parse_output(
            box.exec(R.test_command(box, [gen_path]), timeout=1800).output)
        if not collected:
            score.why = "the generated test collects nothing on the fixed code"
            return score
        gen_expected = list(collected)
        # Both tests must pass on the unmutated fix, or every mutant would read as
        # killed and the score would be meaningless rather than obviously wrong.
        if _fails(box, gold_targets, gold_expected):
            score.why = "the developer's test does not pass on the fixed code here"
            return score
        if _fails(box, [gen_path], gen_expected):
            score.why = "the generated test does not pass on the fixed code here"
            return score

        mutants = generate(box, instance["patch"], n)
        if not mutants:
            score.measured = True
            score.why = "mutmut offers no mutations on the lines this patch changed"
            return score

        originals = {m.file: box.read(m.file) or "" for m in mutants}
        for m in mutants:
            box.write(m.file, m.source)
            try:
                m.agent_kills = _fails(box, [gen_path], gen_expected)
                m.developer_kills = _fails(box, gold_targets, gold_expected)
            finally:
                box.write(m.file, originals[m.file])
            m.source = ""              # written; no reason to keep it in the record
            flow.record(flow.VERIFY, "mutant",
                        f"{m.name}: agent {'kills' if m.agent_kills else 'survives'}, "
                        f"developer {'kills' if m.developer_kills else 'survives'}")
            if not quiet:
                print(f"    {m.name:30} agent "
                      f"{'kill' if m.agent_kills else 'LIVE'}   developer "
                      f"{'kill' if m.developer_kills else 'LIVE'}")
    finally:
        # Back to base, tests off before the fix because they went on after it. A tree
        # left patched would make the next "before the fix" run be the after run.
        for undo in (instance["test_patch"], instance["patch"]):
            try:
                box.apply_patch(undo, revert=True)
            except Exception:
                pass
        box.exec(f"rm -rf {BASE_COPIES}")

    score.total = len(mutants)
    score.agent_killed = sum(1 for m in mutants if m.agent_kills)
    score.developer_killed = sum(1 for m in mutants if m.developer_kills)
    score.mutants = [m.as_dict() for m in mutants]
    score.measured = True
    if out_dir is not None:
        _write_records(out_dir, mutants, score)
    return score
