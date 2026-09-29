"""What the agent is given, as one registry that everything else reads.

A run is defined partly by its instance and partly by its *configuration*: whether the
agent was shown the bug report, whether it was shown the diff, which tools it held. Those
used to be scattered -- a `--blind` boolean threaded through four functions, a
`coverage_tool` boolean threaded through five, each with its own ad-hoc handling in the
prompt builder. Adding a third switch meant touching all of them and hoping nothing was
missed.

Here they are data. Add a `Feature` to `FEATURES` and it gets a flag, a place in the
recorded result, dependency handling, and the ability to gate a prompt piece or a
paragraph inside one. Nothing else needs editing.

**Two kinds of feature, two kinds of flag (since 2026-09-28).** What the agent is *shown*
-- the report, the diff, the briefing on how the project tests -- is an input: on unless
withheld, `--no-issue`, `--no-patch`, `--no-repo-facts`. What is *added* to a bare agent --
the tools beyond run/write/run_tests, the guard, the two stop gates -- is an add-on: off
unless asked for, `--add-verify-tool`, `--add-coverage-tool`, `--add-mutation-tool`,
`--add-guard`, `--add-require-tools`, `--add-second-chance`. A command line then reads as
what the run has, and a run with no flags is the bare agent shown everything. Before,
every feature was on by default and removed by `--no-<name>`, except the second chance,
which was added by `--second-chance` -- two conventions in one list.

An input and a tool are separate features even when they are about the same thing. The
diff and `verify` were one switch at first, on the reasoning that a check against the
change is only possible once the change has been shown. That was wrong: the harness holds
the patch in every configuration and applies it itself, so `verify` can report whether the
agent's test flips without the agent ever seeing a line of the diff. Coupling them also
confounded the comparison it exists to make -- if withholding the diff also withheld the
feedback loop, a drop in the result could not be attributed to either.

What genuinely cannot be separated is `coverage`, which prints the source of the lines a
test missed. That is the diff, so it needs `patch`.

`repo-facts` is the first feature whose withholding has to *add* something. The others
take a component away and the prompt is simply shorter; take away the briefing on how
this project tests and the agent needs to be told to work it out instead, or the run
measures a missing instruction rather than a missing input. `prompt.py` grew a negative
`needs: !repo-facts` for exactly that, and it is why a feature can now own a substitute
piece as well as gate its own.

    features = FeatureSet.from_args(args)     # or FeatureSet(off=["patch"])
    if "coverage-tool" in features: ...

Two rules are enforced rather than documented:

* **Dependencies are checked, not guessed.** On the command line, an add-on whose need
  is missing is refused with the flag to add: `--add-coverage-tool` without
  `--add-verify-tool`, or with `--no-patch`, is an error, never a quiet change of
  configuration. `FeatureSet.of`, the programmatic form, still cascades (withholding
  `patch` takes the coverage tool with it) and records why in `cascaded`.
* **Something has to describe the bug.** With neither the report nor the diff the task
  is not harder, it is impossible, and the run would produce a row that looks like a
  measurement. That is refused.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Feature:
    name: str
    """Also the flag: `issue` gives `--no-issue`, `guard` gives `--add-guard`."""

    summary: str
    """One line for `--help`: what withholding an input does, what adding an add-on does."""

    added: bool = False
    """An add-on: off unless `--add-<name>` asks for it. An input (False) is on unless
    `--no-<name>` withholds it."""

    implies: tuple[str, ...] = ()
    """Add-ons this one's flag turns on as well, because it is a variant of them rather
    than a separate component: `--add-require-tools-with-score-report` is require-tools
    with scores. Part of what the flag means, stated here, not a repair of a missing
    flag."""

    needs: tuple[str, ...] = ()
    """Features that must be on for this one to mean anything."""

    tools: tuple[str, ...] = ()
    """Agent tools that exist only while this feature is on. The prompt builder uses
    these to prove no piece of the finished prompt names a tool that was not
    registered."""

    aliases: tuple[str, ...] = ()
    """Extra spellings of the flag. `--no-repo-facts` says what the registry does;
    `--repo-search` says what the run is for. Both set the same switch, so a name that
    reads better at the command line does not cost a second code path."""


FEATURES: tuple[Feature, ...] = (
    Feature("issue", "withhold the bug report; the agent has only the diff to work "
                     "out what the change is for"),
    Feature("patch", "withhold the pull request diff from the prompt. The agent has to "
                     "work out the intended behaviour from the report alone"),
    Feature("verify-tool", "add the `verify` tool, which runs the agent's test before "
                           "and after the fix and says whether it flips. Without it the "
                           "agent can watch its test fail on this code but never watch it "
                           "pass; the harness decides the verdict either way",
            added=True, tools=("verify",)),
    Feature("coverage-tool", "add the `coverage` tool: which changed lines the test never "
                             "runs, with their code and the conditions above them. The "
                             "harness measures changed-line coverage either way",
            added=True, needs=("patch", "verify-tool"), tools=("coverage",)),
    Feature("mutation-tool", "add the `mutation` tool, which runs the agent's test "
                             "against small wrong variants of the fix and reports which "
                             "ones it fails to notice. The harness measures a mutation "
                             "score either way, on mutants the agent was never shown",
            added=True, needs=("patch", "verify-tool"), tools=("mutation",)),
    Feature("guard", "add the guard: edits the agent makes to files that were already "
                     "here are reverted between actions. Without it the prohibition "
                     "stays in the prompt and the audit still reports a dirty tree as "
                     "BROKEN, but an agent that applies the fix to the library keeps it",
            added=True),
    # The stop checks and the restart (2026-09-28, second revision). `require-tools` holds
    # every refusal of a stop: the harness's own base run of the file, the agent's
    # `verify` loop until fail-to-pass, then the coverage/mutation duties. The second
    # chance is no longer a refusal at all -- it is a restart after the run has ended
    # without a test that scores YES.
    Feature("require-tools", "add the stop checks, as three loops: `verify` until the test "
                             "is fail-to-pass (the harness also runs it at base: no file, "
                             "nothing collected, passing or skipped is refused), then "
                             "`coverage` until no changed line is missed and `mutation` "
                             "until no variant survives -- each ending early when an "
                             "honest attempt stops improving it",
            added=True, needs=("verify-tool",)),
    Feature("require-tools-with-score-report",
            "add the loops of --add-require-tools, with scores: `coverage` and `mutation` "
            "report changed-line coverage (target 100 percent) and mutation score "
            "(maximised), and the agent is asked to reach them. Implies "
            "--add-require-tools",
            added=True, needs=("verify-tool", "require-tools"),
            implies=("require-tools",)),
    Feature("second-chance", "add a restart: when the run ends without a test that scores "
                             "fail-to-pass and actions remain, the agent starts a fresh "
                             "conversation with the task, the record of its first "
                             "attempt, the test it left (unless the run was BROKEN) and "
                             "the rest of its budget. The run is scored again at the end",
            added=True),
    Feature("repo-facts", "withhold the briefing on how this project tests: the target "
                          "convention, where a new test file has to live to be "
                          "collected, the neighbouring tests and the test "
                          "configuration. The agent establishes those itself, and "
                          "chooses the directory its test goes in",
            aliases=("--repo-search",)),
)

BY_NAME = {f.name: f for f in FEATURES}

# At least one of these has to survive, or nothing in the prompt says what bug to write
# a test for.
DESCRIBES_THE_BUG = ("issue", "patch")


def instruments(features: "FeatureSet") -> tuple[str, ...]:
    """Tools the agent holds in this configuration and is expected to have used.

    Read off the registry rather than listed, so a tool added later is covered without
    anyone remembering this function. Only tools a feature *owns* count: `run`,
    `write_file` and `run_tests` exist in every configuration and are means rather than
    checks, while `verify`, `coverage` and `mutation` each answer a question nothing else
    answers, which is the whole reason they were built.

    The point of the list is that a registered tool that goes uncalled is not a result
    about the model. It is a configuration we never actually ran: the arm says `full` and
    the behaviour is the arm without the tool.
    """
    return tuple(t for f in FEATURES if f.name in features for t in f.tools)


def flag(name: str) -> str:
    """The flag that departs from the default: `--add-<name>` for an add-on, `--no-<name>`
    for an input."""
    return f"--{'add' if BY_NAME[name].added else 'no'}-{name}"


def dest(name: str) -> str:
    """argparse turns `--add-coverage-tool` into `add_coverage_tool`, `--no-issue` into
    `no_issue`."""
    return flag(name)[2:].replace("-", "_")


@dataclass(frozen=True)
class FeatureSet:
    """Which features are on for one run. Immutable, so it can be passed freely."""

    off: frozenset[str] = field(default_factory=frozenset)
    cascaded: tuple[tuple[str, str], ...] = ()
    """(feature, the dependency that took it out) -- kept so the run can say why a
    feature is off that nobody asked to turn off."""

    def __post_init__(self) -> None:
        unknown = sorted(self.off - set(BY_NAME))
        if unknown:
            raise ValueError(
                f"unknown feature(s): {', '.join(unknown)}. "
                f"Known: {', '.join(BY_NAME)}")

    @classmethod
    def of(cls, off: object = ()) -> FeatureSet:
        """Build a set from the names to withhold, cascading dependencies."""
        asked = frozenset(off or ())
        cls(off=asked)                                   # validate the names first
        resolved, cascaded = set(asked), []
        changed = True
        while changed:                                   # a need can itself have needs
            changed = False
            for f in FEATURES:
                if f.name in resolved:
                    continue
                for need in f.needs:
                    if need in resolved:
                        resolved.add(f.name)
                        cascaded.append((f.name, need))
                        changed = True
                        break
        if not set(DESCRIBES_THE_BUG) - resolved:
            raise SystemExit(
                f"  {' and '.join(flag(n) for n in DESCRIBES_THE_BUG)} cannot be "
                f"combined: with neither the report nor the diff, nothing tells the "
                f"agent which bug to write a test for. The run would still produce a "
                f"verdict, which is worse than refusing.")
        return cls(off=frozenset(resolved), cascaded=tuple(cascaded))

    @classmethod
    def full(cls) -> FeatureSet:
        """Everything on. The programmatic default -- not what a command line with no flags
        means, which is the bare agent shown everything."""
        return cls.of()

    @classmethod
    def from_args(cls, args: object) -> FeatureSet:
        """The configuration a command line asked for, checked rather than completed.

        An input is off when its `--no-` flag was given; an add-on is off unless its
        `--add-` flag was. A feature left on whose need is off is refused with the flag
        that fixes it -- no cascade here: a configuration someone typed must be the one
        that runs, and the one the result records."""
        given = {f.name for f in FEATURES if getattr(args, dest(f.name), False)}
        given |= {i for f in FEATURES if f.name in given for i in f.implies}
        off = {f.name for f in FEATURES if (f.name in given) != f.added}
        problems = []
        for f in FEATURES:
            if f.name in off:
                continue
            for need in f.needs:
                if need in off:
                    fix = (f"add {flag(need)}" if BY_NAME[need].added
                           else f"drop {flag(need)}")
                    problems.append(f"{flag(f.name)} needs {need}: {fix}")
        if problems:
            raise SystemExit("  " + "\n  ".join(problems))
        return cls.of(sorted(off))

    def __contains__(self, name: str) -> bool:
        if name not in BY_NAME:
            raise KeyError(f"unknown feature {name!r}. Known: {', '.join(BY_NAME)}")
        return name not in self.off

    @property
    def on(self) -> tuple[str, ...]:
        return tuple(f.name for f in FEATURES if f.name not in self.off)

    @property
    def withheld(self) -> tuple[str, ...]:
        return tuple(f.name for f in FEATURES if f.name in self.off)

    @property
    def absent_tools(self) -> tuple[str, ...]:
        """Tools that will not be registered, so the prompt must not mention them."""
        return tuple(t for f in FEATURES if f.name in self.off for t in f.tools)

    @property
    def default(self) -> bool:
        return not self.off

    def slug(self) -> str:
        """A short name for this configuration, for labelling a series of runs.

        In the terms of the flags: `full` is every add-on; otherwise the add-ons present
        (`bare` when there are none). A variant add-on (one that `implies` another, like
        `require-tools-with-score-report`) is a suffix, not part of `full`:
        `full+require-tools-with-score-report`. Withheld inputs follow: `full no-repo-facts`,
        `bare no-issue`. Before 2026-09-28 names were `no-<withheld>`, which recorded
        results still carry."""
        core = [f.name for f in FEATURES if f.added and not f.implies]
        variants = [f.name for f in FEATURES if f.added and f.implies and f.name in self.on]
        present = [n for n in core if n in self.on]
        head = ("full" if present == core else "+".join(present) or "bare")
        head += "".join(f"+{v}" for v in variants)
        withheld = [f.name for f in FEATURES if not f.added and f.name in self.off]
        return head + "".join(f" no-{n}" for n in withheld)

    def as_dict(self) -> dict:
        """Recorded in every result, so a series of runs can be compared by what the
        agent was given rather than by whoever remembers which flags they typed."""
        return {"config": self.slug(), "on": list(self.on),
                "withheld": list(self.withheld),
                "withheld_by_dependency": {n: need for n, need in self.cascaded}}

    def describe(self) -> str:
        """One line for the run header."""
        if not self.off:
            return "everything: every input shown, every add-on added"
        added = [f.name for f in FEATURES if f.added and f.name in self.on]
        withheld = []
        for f in FEATURES:
            if not f.added and f.name in self.off:
                why = dict(self.cascaded).get(f.name)
                withheld.append(f"{f.name} (needs {why})" if why else f.name)
        return (f"added: {', '.join(added) or 'nothing'}"
                + (f"; withheld: {', '.join(withheld)}" if withheld else ""))


def add_arguments(parser: object) -> None:
    """One flag per feature, in two groups. Generated, so a new feature cannot be added to
    the registry and forgotten here."""
    shown = parser.add_argument_group(
        "what the agent is shown (on unless withheld)",
        "Each flag removes one input. The harness measures the same things either way, "
        "so runs made with different flags are comparable; every result records the "
        "configuration.")
    added = parser.add_argument_group(
        "what is added to the agent (off unless asked for)",
        "With none of these the agent has run, write_file and run_tests, and its first "
        "stop is final. Each flag adds one component; an add-on whose need is missing is "
        "refused.")
    for f in FEATURES:
        (added if f.added else shown).add_argument(
            flag(f.name), *f.aliases, dest=dest(f.name), action="store_true",
            help=f.summary)


def child_flags(features: FeatureSet) -> list[str]:
    """The flags a child process needs to reproduce this configuration: `--no-` for each
    input withheld, `--add-` for each add-on present. A feature a cascade took out is off
    in both processes without being named, so the child is not told it was a choice."""
    cascaded = {name for name, _ in features.cascaded}
    return ([flag(f.name) for f in FEATURES
             if not f.added and f.name in features.withheld and f.name not in cascaded]
            + [flag(f.name) for f in FEATURES if f.added and f.name in features.on])
