"""What the agent is given, as one registry that everything else reads.

A run is defined partly by its instance and partly by its *configuration*: whether the
agent was shown the bug report, whether it was shown the diff, which tools it held. Those
used to be scattered -- a `--blind` boolean threaded through four functions, a
`coverage_tool` boolean threaded through five, each with its own ad-hoc handling in the
prompt builder. Adding a third switch meant touching all of them and hoping nothing was
missed.

Here they are data. Add a `Feature` to `FEATURES` and it gets a `--no-<name>` flag, a
place in the recorded result, dependency handling, and the ability to gate a prompt piece
or a paragraph inside one. Nothing else needs editing.

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

* **Dependencies cascade.** `coverage-tool` needs `patch`, so `--no-patch` turns the
  coverage tool off too and says so. It does not fail; the resulting configuration is a
  coherent one, and refusing it would only make the caller pass both flags to mean one
  thing.
* **Something has to describe the bug.** With neither the report nor the diff the task
  is not harder, it is impossible, and the run would produce a row that looks like a
  measurement. That is refused.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Feature:
    name: str
    """Also the flag: `issue` gives `--no-issue`."""

    summary: str
    """One line for `--help`, phrased as what withholding it does."""

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
    Feature("verify-tool", "withhold the `verify` tool, so the agent can watch its test "
                           "fail on this code but never watch it pass. The harness "
                           "still decides the verdict either way",
            tools=("verify",)),
    Feature("coverage-tool", "withhold the `coverage` tool. The harness still measures "
                             "changed-line coverage; the agent just cannot see it while "
                             "it works",
            needs=("patch", "verify-tool"), tools=("coverage",)),
    Feature("mutation-tool", "withhold the `mutation` tool, which runs the agent's test "
                             "against small wrong variants of the fix and reports which "
                             "ones it fails to notice. The harness still measures a "
                             "mutation score afterwards, on mutants the agent was never "
                             "shown",
            needs=("patch", "verify-tool"), tools=("mutation",),
            aliases=("--no-mutation",)),
    Feature("guard", "stop reverting edits the agent makes to files that were already "
                     "here. The prohibition stays in the prompt and the audit still "
                     "reports a dirty tree as BROKEN -- what goes away is the repair "
                     "between actions, so an agent that applies the fix to the library "
                     "keeps it. Withhold it to measure how often that happens rather "
                     "than how often it is caught"),
    Feature("require-tools", "stop requiring the agent to have used the tools it was "
                             "given. With this on -- the default -- a run that finishes "
                             "without calling a registered instrument is sent back with "
                             "the names of the ones it skipped, because a tool that is "
                             "present and unused is a configuration we are not actually "
                             "measuring",
            needs=("verify-tool",)),
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
    return f"--no-{name}"


def dest(name: str) -> str:
    """argparse turns `--no-coverage-tool` into `no_coverage_tool`."""
    return f"no_{name.replace('-', '_')}"


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
    def from_args(cls, args: object) -> FeatureSet:
        return cls.of([f.name for f in FEATURES if getattr(args, dest(f.name), False)])

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
        """A short name for this configuration, for labelling a series of runs."""
        return "full" if self.default else "no-" + "+".join(self.withheld)

    def as_dict(self) -> dict:
        """Recorded in every result, so a series of runs can be compared by what the
        agent was given rather than by whoever remembers which flags they typed."""
        return {"config": self.slug(), "on": list(self.on),
                "withheld": list(self.withheld),
                "withheld_by_dependency": {n: need for n, need in self.cascaded}}

    def describe(self) -> str:
        """One line for the run header."""
        if self.default:
            return "everything (no --no-* flags)"
        parts = []
        for name in self.withheld:
            why = dict(self.cascaded).get(name)
            parts.append(f"{name} (needs {why})" if why else name)
        return f"without {', '.join(parts)}"


def add_arguments(parser: object) -> None:
    """Give the parser one `--no-<name>` per feature. Generated, so a new feature
    cannot be added to the registry and forgotten here."""
    group = parser.add_argument_group(
        "what to withhold from the agent",
        "Each flag removes one component. The harness measures the same things either "
        "way, so runs made with different flags are comparable; every result records "
        "which flags were in force.")
    for f in FEATURES:
        group.add_argument(flag(f.name), *f.aliases, action="store_true",
                           help=f.summary)


def child_flags(features: FeatureSet) -> list[str]:
    """The flags a child process needs to reproduce this configuration.

    Only what was asked for: a cascaded feature comes back on its own in the child, and
    passing it explicitly would report it as a deliberate choice.
    """
    cascaded = {name for name, _ in features.cascaded}
    return [flag(n) for n in features.withheld if n not in cascaded]
