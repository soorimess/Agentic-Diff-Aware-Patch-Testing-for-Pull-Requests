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

import bisect
import difflib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openhands_f2p import flow
from openhands_f2p import runners as R
from openhands_f2p import swebench_env as E
from openhands_f2p import verify as V
from openhands_f2p.sandbox import Sandbox
from openhands_f2p.statements import widen

# Per half of the pool, not in total: `split_pool` spreads each half up to this many.
# 20 since 2026-09-28, so a patch with a large candidate pool is scored on up to 20
# unseen mutants rather than 10; a small patch stays small whatever this says.
DEFAULT_MUTANTS = 20

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


def _allow_decorated() -> None:
    """Let mutmut mutate inside decorated functions and classes, and inside `__new__`,
    `__getattribute__` and `__setattr__`. Once per process.

    mutmut 3 skips every decorated function (a lone `@staticmethod` / `@classmethod`
    aside) and every decorated class, whole -- for its own runner, which swaps functions
    through a trampoline that a decorator would wrap. We never use that runner, only the
    (original, mutated) node pairs, so the rule protected nothing here and silently cost
    every line under `@property`, `@cached_property`, `@functools.wraps` or a
    `@dataclass`. Found in the first 36-instance base run (2026-09-29): pytest-5262's
    whole patch is an `@property` and astropy-7336's sits in a `@wraps` wrapper, and both
    reported "mutmut offers no mutations on the lines this patch changed".

    The decorator expressions themselves stay unmutated -- they run when the module is
    imported, so a mutated argument breaks the import rather than the behaviour -- which
    is the one part of mutmut's reasoning that does apply. The node is asked about
    without its decorators; its other rules (names never mutated, pragmas) still apply.
    """
    import libcst as cst
    from mutmut.mutation import file_mutation
    from mutmut.mutation.file_mutation import MutationVisitor

    # Same origin, same cost: `__new__`, `__getattribute__` and `__setattr__` are never
    # mutated because a trampoline cannot stand in for them. sympy-24562's whole patch is
    # in `Rational.__new__` and reported "no mutations" after the decorator rule was
    # lifted (second base run, 2026-09-30). The rule reads the module global at call time.
    file_mutation.NEVER_MUTATE_FUNCTION_NAMES = set()
    original = MutationVisitor._skip_node_and_children
    if getattr(original, "_f2p_allows_decorated", False):
        return

    def skip(self, node):
        if isinstance(node, cst.Decorator):
            return True
        if isinstance(node, (cst.FunctionDef, cst.ClassDef)) and node.decorators:
            return original(self, node.with_changes(decorators=[]))
        return original(self, node)

    skip._f2p_allows_decorated = True
    MutationVisitor._skip_node_and_children = skip


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

    _allow_decorated()
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


def _rewrite(a: list[str], b: list[str]) -> tuple[set[int], str, str]:
    """What a mutant rewrites: the original lines whose non-blank text changed, and the
    changed text before and after, one line each.

    Line by line was not enough. Dropping an argument makes libcst join a wrapped call
    onto one line, and a line diff then marks the untouched continuation line as rewritten
    too: sphinx-7454 (fix check) kept `pending_xref(..., nodes.Text(text), ...)` minus its
    `nodes.Text(text)` -- on line 79, which the pull request never touched -- as a mutant
    of line 80, and labelled it `reftarget=text)   ->   ` from the shifted mutated file.
    Characters, not lines, say which line lost something."""
    touched: set[int] = set()
    befores, afters = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        befores.append(" ".join(x.strip() for x in a[i1:i2]))
        afters.append(" ".join(x.strip() for x in b[j1:j2]))
        if i1 == i2:                       # whole lines inserted
            touched.add(min(i1 + 1, max(len(a), 1)))
            continue
        block_a, block_b = "\n".join(a[i1:i2]), "\n".join(b[j1:j2])
        starts, pos = [], 0
        for x in a[i1:i2]:
            starts.append(pos)
            pos += len(x) + 1

        def line_of(c: int) -> int:
            return i1 + bisect.bisect_right(starts, c)
        for cop, c1, c2, d1, d2 in difflib.SequenceMatcher(
                a=block_a, b=block_b, autojunk=False).get_opcodes():
            if cop == "equal":
                continue
            gone, came = block_a[c1:c2], block_b[d1:d2]
            if not gone.strip() and not came.strip():
                continue                   # re-wrapping only
            if gone.strip():
                touched.update(line_of(c) for c in range(c1, c2) if not block_a[c].isspace())
            else:
                touched.add(line_of(min(c1, max(len(block_a) - 1, 0))))
    return touched, " | ".join(befores), " | ".join(afters)


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
    # `mutmut` selects by statement, so a patch whose only changed line is the
    # continuation of a wrapped expression matches nothing and the instance reports "no
    # mutations on the lines this patch changed" -- the same blind spot that made
    # coverage call `sympy-21612` unmeasurable. Widening to the statement each changed
    # line belongs to asks about the expression the patch actually edited. The originals
    # stay in the set, so nothing that already matched stops matching.
    wide = widen(source, changed) if changed else changed
    try:
        module, mutations, _, _ = create_mutations(filename, source, wide or None)
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
        # The lines of the original the mutant actually rewrites, and only a mutant that
        # rewrites one the patch changed is kept. Widening selects whole statements, so
        # mutmut also mutated tokens on a statement's *unchanged* first line:
        # sphinx-7454 (base, cap 125) changed line 80 only, and its two survivors were
        # `''` -> `None` / `'XXXX'` on line 79 -- code the pull request never touched,
        # scored as gaps in both tests. Checking against `wide` let them through.
        touched, _, _ = _rewrite(original, rows_b)
        hit = sorted(touched & changed) if changed else sorted(touched)
        if not hit:
            continue                   # outside the patch: reformatting, or a wide line
        line = hit[0]
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


def _gather(box: Sandbox, patch: str) -> tuple[list[tuple], dict[str, str]]:
    """Every candidate mutation on the changed lines, and the files they came from.

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
    return candidates, heads


def _build(picked: list[tuple], heads: dict[str, str]) -> list[Mutant]:
    out: list[Mutant] = []
    for path, line, index, mutated in picked:
        source = heads[path]
        _, before, after = _rewrite(source.splitlines(), mutated.splitlines())
        out.append(Mutant(
            name=f"{Path(path).stem}-L{line}-{index}",
            file=path, line=line, operator=f"{before}   ->   {after}",
            source=mutated,
            diff="".join(difflib.unified_diff(
                source.splitlines(keepends=True), mutated.splitlines(keepends=True),
                fromfile=f"a/{path}", tofile=f"b/{path}", n=2))))
    return out


def _halve(candidates: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    """Two candidate sets, alternating *within* each (file, line) group.

    Within, not across, and the distinction is the whole point. `_spread` round-robins
    over groups, so consecutive entries in its output come from *different* lines --
    taking every other one therefore splits by line, not by sample. On a two-line patch
    that gives one half every mutant on line A and the other every mutant on line B.

    That is not hypothetical. `requests-1142` split that way scored the developer's own
    test at 0 of 5, because the held-out half was entirely on a line that test does not
    exercise. A denominator built like that measures which line landed where.

    Alternating inside each group instead puts mutants from every changed line in both
    halves -- every line mutmut offers more than one of, at least; a line with a single
    candidate can only land on one side, and rotation is what stops that side always
    being the same one.

    The side each group *starts* on rotates, and that is a second bug's worth of care.
    While index 0 of every group went to the same half, and mutmut's order within one
    literal is fixed -- `False -> None` before `False -> True` -- one half collected every
    type-changing mutant and the other every value-changing one. Those are not the same
    question. `seaborn-3187` showed the agent `set_useOffset(None)`, which raises a
    TypeError deep in matplotlib and so dies against any test at all, and scored it on
    `set_useOffset(True)`, which formats identically unless the data is in the range where
    an offset would appear. The agent read a kill it had not earned and never learned that
    its inputs could not tell the fix from its absence.

    Rotating costs one counter and makes the halves samples of the same distribution of
    operators, which is the only thing that makes a held-out number mean anything.
    """
    groups: dict[tuple, list] = {}
    for c in candidates:
        groups.setdefault((c[0], c[1]), []).append(c)
    a, b = [], []
    for off, key in enumerate(sorted(groups)):
        for i, c in enumerate(groups[key]):
            (a if (i + off) % 2 == 0 else b).append(c)
    return a, b


def generate(box: Sandbox, patch: str, limit: int) -> list[Mutant]:
    """The mutants for one patch, read off the code as the patch leaves it."""
    candidates, heads = _gather(box, patch)
    return _build(_spread(candidates, limit), heads)


def split_pool(box: Sandbox, patch: str, n: int) -> tuple[list[Mutant], list[Mutant]]:
    """Two disjoint samples: one to show the agent, one to score it on.

    Without this the feature eats its own metric. `generate` is deterministic, so the
    agent's tool and the harness's measurement would be handed the *same* mutants; an
    agent that tunes its test until those ten die would then be scored on those ten, and
    the number would record compliance rather than whether the test generalises. It is
    the oldest mistake in the book -- testing on the training set.

    The split happens at the candidate level, inside each (file, line) group, for the
    reason `_halve` gives: splitting the *spread* output would divide the pool by line
    instead of sampling it.

    Only used when the agent has the `mutation` tool. Otherwise nothing has been shown to
    anyone and the whole pool is fair game, which is what every run so far measured.
    """
    candidates, heads = _gather(box, patch)
    shown, held = _halve(candidates)
    return _build(_spread(shown, n), heads), _build(_spread(held, n), heads)


def probe(box: Sandbox, patch: str, test_path: str, n: int) -> dict:
    """Run one test against the mutants the *agent* is allowed to see.

    The agent's instrument, not the measurement -- `measure` is the measurement, it runs
    later, and it uses the half of the pool this never shows.

    Unlike `measure` this never applies `test_patch`. The developer's test is the held-out
    answer; a tool that installed it during the agent's turn would put it in the tree the
    agent can read.
    """
    state = box.ensure_base(patch)
    if state != "base":
        return {"ok": False, "why": f"the working tree is {state}, not base"}
    try:
        for path in E.patched_source_files(patch):
            text = box.read(path)
            if text is not None:
                box.write(f"{BASE_COPIES}/{path}", text)
        box.apply_patch(patch)
        collected = V.own_outcomes(R.parse_output(
            box.exec(R.test_command(box, [test_path]), timeout=1800).output), [test_path])
        if not collected:
            return {"ok": False, "why": f"{test_path} collects nothing on the fixed code"}
        expected = list(collected)
        t0 = time.monotonic()
        failed = _fails(box, [test_path], expected)
        limit = _mutant_timeout(time.monotonic() - t0)
        if failed:
            return {"ok": False,
                    "why": "your test does not pass on the fixed code yet, so asking "
                           "what it notices about a wrong fix has no answer"}
        shown, _held = split_pool(box, patch, n)
        if not shown:
            return {"ok": True, "mutants": [],
                    "why": "no mutations are available on the lines this change touches"}
        originals = {m.file: box.read(m.file) or "" for m in shown}
        for m in shown:
            box.write(m.file, m.source)
            try:
                m.agent_kills = _fails(box, [test_path], expected, timeout=limit)
            finally:
                box.write(m.file, originals[m.file])
        return {"ok": True, "mutants": shown}
    finally:
        # The tree goes back whatever happened. A tree left at head would make the
        # harness's "before the fix" run actually be the after run, and the verdict
        # would invert silently. Reverted here rather than through `ensure_base`, which
        # logs a patch at head as "left applied by the agent" -- it was this tool's own.
        if box.patch_state(patch) == "head":
            box.apply_patch(patch, revert=True)


# A mutant run is given ten times what the same tests took on the unmutated fix, and
# never less than a minute (user, 2026-10-04) -- mutmut's own rule. It was a flat 1800 s:
# a mutant that loops forever cost half an hour per run, and sympy-24562's developer
# tests (7.6 s on the fix) hung that long on a `Rational` mutant. A run that times out
# objects to the mutant -- killed, as before -- since its output parses to nothing.
MUTANT_TIMEOUT_FACTOR = 10
MUTANT_TIMEOUT_MIN = 60


def _mutant_timeout(unmutated_s: float) -> int:
    return max(MUTANT_TIMEOUT_MIN, int(MUTANT_TIMEOUT_FACTOR * unmutated_s) + 1)


def _fails(box: Sandbox, targets: list[str], expected: list[str],
           timeout: int = 1800) -> bool:
    """True when the test objects to the code as it currently stands.

    "Objects" is `FAILED` or `ERROR` on a node expected to pass, or the node vanishing
    from the report -- a mutant that breaks collection kills the test as surely as a
    failed assertion, and reading a missing node as "passed" would count that as a
    survivor.
    """
    out = R.parse_output(box.exec(R.test_command(box, targets), timeout=timeout).output)
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
    held_out: bool = False
    """Whether the agent held the `mutation` tool, and so was shown the other half of the
    pool. Every run is scored on the same half since 2026-09-28 -- see `measure`."""
    agent_killed: int = 0
    developer_killed: int = 0
    # False when none of the developer's tests pass on the fixed code in this sandbox;
    # `developer_excluded` names the ones that do not (see `measure`).
    developer_measured: bool = True
    developer_excluded: list[str] = field(default_factory=list)
    mutants: list[dict] = field(default_factory=list)

    def _pct(self, n: int) -> float | None:
        return round(100.0 * n / self.total, 1) if self.total else None

    def as_dict(self) -> dict:
        return {"measured": self.measured, "why": self.why or None,
                "tool": "mutmut", "asked": self.asked, "total": self.total,
                "held_out": self.held_out,
                "agent": {"killed": self.agent_killed, "total": self.total,
                          "percent": self._pct(self.agent_killed)},
                "developer": ({"killed": self.developer_killed, "total": self.total,
                               "percent": self._pct(self.developer_killed),
                               "excluded": self.developer_excluded}
                              if self.developer_measured else
                              {"killed": None, "total": self.total, "percent": None,
                               "excluded": self.developer_excluded,
                               "why": "none of the developer's tests pass on the fixed "
                                      "code in this sandbox"}),
                "mutants": self.mutants}


def line(score: dict) -> str:
    if not score.get("measured"):
        return f"not measured -- {score.get('why') or 'no reason recorded'}"
    if not score.get("total"):
        # The reason recorded, not a fixed sentence: a pool of one goes to the agent's
        # half, and this said "mutmut offers none" for astropy-7336, astropy-14995 and
        # xarray-3677 (base, cap 125), whose result said otherwise.
        return f"no mutants -- {score.get('why') or 'mutmut offers none on the lines this patch changed'}"
    a, d = score["agent"], score["developer"]
    gaps = sum(1 for m in score.get("mutants", [])
               if m.get("verdict") == "developer only")
    dev = (f"{d['killed']}/{d['total']}" if d.get("killed") is not None
           else "not measured (none of its tests pass here)")
    return (f"agent test {a['killed']}/{a['total']}, "
            f"developer test {dev}"
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
            quiet: bool = False, held_out: bool = False) -> Score:
    """Mutation score for one generated test, and for the developer's, on one set.

    The box arrives at base and is left at base. In between the real patch goes on --
    mutants are variants of the *fixed* code, so the fix has to be there first -- and
    both tests are installed, because every mutant is asked of both.
    """
    score = Score(asked=n, held_out=held_out)
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
        collected = V.own_outcomes(R.parse_output(
            box.exec(R.test_command(box, [gen_path]), timeout=1800).output), [gen_path])
        if not collected:
            score.why = "the generated test collects nothing on the fixed code"
            return score
        gen_expected = list(collected)
        # Both tests must pass on the unmutated fix, or every mutant would read as
        # killed and the score would be meaningless rather than obviously wrong.
        # Only the developer's tests that pass on the unmutated fix *here* can say
        # anything about a mutant. Some cannot pass in this sandbox at all: requests'
        # tests call httpbin and astropy's refraction tests fetch IERS data, and the
        # container has no network. Returning here, as this did, dropped the *agent's*
        # column with the developer's -- requests-1766 and astropy-13398 in the second
        # base run (2026-09-30) had no mutation score for a test that passed. Now the
        # developer's column uses the tests that pass, names the ones left out, and is
        # marked unmeasured only when none pass.
        t0 = time.monotonic()
        gold_out = R.parse_output(
            box.exec(R.test_command(box, gold_targets), timeout=1800).output)
        gold_limit = _mutant_timeout(time.monotonic() - t0)
        gold_ok = [n for n in gold_expected if R.outcome_of(gold_out, n) == "PASSED"]
        score.developer_excluded = [n for n in gold_expected if n not in gold_ok]
        score.developer_measured = bool(gold_ok)
        t0 = time.monotonic()
        gen_failed = _fails(box, [gen_path], gen_expected)
        gen_limit = _mutant_timeout(time.monotonic() - t0)
        if gen_failed:
            score.why = "the generated test does not pass on the fixed code here"
            return score

        # Always the scoring half of the split, with or without the tool. With it, the
        # agent was shown the other half, so the number says whether the test
        # generalises rather than whether it memorised the sample. Without it, the same
        # half is used anyway: until 2026-09-28 such arms were scored on the whole pool
        # (often 10 mutants) while arms with the tool got the half (often 1-3), so the
        # two columns were different quantities and could not be paired per instance.
        shown, mutants = split_pool(box, instance["patch"], n)
        if not mutants:
            score.measured = True
            # A pool of one goes to the agent's half, and "offers no mutations" was false
            # of it: there was a mutant, and the agent's `mutation` tool had shown it.
            score.why = ("the only mutant(s) on these lines went to the half reserved "
                         "for the agent's `mutation` tool; none were left to score on"
                         if shown else
                         "mutmut offers no mutations on the lines this patch changed")
            return score

        originals = {m.file: box.read(m.file) or "" for m in mutants}
        for m in mutants:
            box.write(m.file, m.source)
            try:
                m.agent_kills = _fails(box, [gen_path], gen_expected, timeout=gen_limit)
                m.developer_kills = (_fails(box, gold_targets, gold_ok, timeout=gold_limit)
                                     if gold_ok else None)
            finally:
                box.write(m.file, originals[m.file])
            m.source = ""              # written; no reason to keep it in the record
            dev = ("not measured" if m.developer_kills is None else
                   "kills" if m.developer_kills else "survives")
            flow.record(flow.VERIFY, "mutant",
                        f"{m.name}: agent {'kills' if m.agent_kills else 'survives'}, "
                        f"developer {dev}")
            if not quiet:
                print(f"    {m.name:30} agent "
                      f"{'kill' if m.agent_kills else 'LIVE'}   developer {dev}")
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
    score.developer_killed = sum(1 for m in mutants if m.developer_kills is True)
    score.mutants = [m.as_dict() for m in mutants]
    score.measured = True
    if out_dir is not None:
        _write_records(out_dir, mutants, score)
    return score
