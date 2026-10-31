"""Build MUTATION_REPORT.md and mutation.html: why the mutation tool does not help, and how to fix it.

    python3 scripts/reports/mutation_report.py   (from the repository root)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import common as C  # noqa: E402

E = C.E
OUT = C.RUNS / "mutation.html"
MD = C.RUNS / "MUTATION_REPORT.md"

LEDE = ("On top of the coverage tool, the mutation tool did not make the weak model's tests catch more bugs. "
        "The mutation score is a good measure of a test; as feedback to the agent it does not work.")

WHY = [
    ("The agent cannot act on what it is shown.",
     "The tool lists surviving mutants and wrong versions, often as a one-line description. To kill one, the model "
     "must work out an input that tells it apart from the fix and the value to assert. A weak model rarely does, so "
     "the same survivors come back call after call."),
    ("Tests kill mutants by crashing, not by checking.",
     "Most mutants die because the test errors on them, not because an assertion fails. The tool counts both the same, "
     "so the agent is never pushed to check the values the change computes."),
    ("It competes with the coverage duty.",
     "Both duties share one stop budget and one action budget. Time spent on survivors is taken from raising coverage, "
     "and coverage is what actually improved the tests."),
    ("Some survivors cannot be caught.",
     "Mutants on lines the test never reaches, or that behave like the fix on any sensible input, are reported anyway "
     "and spend the agent's effort for nothing."),
]

CHANGE = [
    ("One duty at a time.", "Ask about survivors only after the coverage duty is met, with its own small budget."),
    ("One survivor at a time.", "Show the single most useful survivor, on a line the test already reaches."),
    ("Count only assertion kills.", "A mutant the test kills by crashing is reported as still open."),
    ("Drop survivors no test can catch.", "Leave out unreached lines and mutants that behave like the fix."),
]

LLM = [
    ("Generate realistic bugs, not syntax edits.",
     "A cheap model reads the change and writes a few plausible wrong versions of it: a missed case from the issue, a "
     "wrong default, an off-by-one on the new branch. These are the bugs a reviewer worries about, unlike mutmut's "
     "operator swaps."),
    ("Ship each bug with a failing example.",
     "For every wrong version the model also writes one input and the value the correct code returns. The harness runs "
     "that input on the fix and on the wrong version and keeps the bug only if the two really differ, so nothing "
     "hallucinated reaches the agent."),
    ("Hand the agent the example, not the bug.",
     "The agent is told: \"with this input the change returns X; a likely bug returns Y; assert on it\". Turning that "
     "into a test is copying, which a weak model can do."),
    ("Keep a held-out set for scoring.",
     "Generate the bugs once per PR and freeze them; show the agent one half and score every configuration on the "
     "other, as now."),
]


def bullets_html(items, ordered=False):
    tag = "ol" if ordered else "ul"
    return f'<{tag} class="findings">' + "".join(f"<li><b>{E(h)}</b> {E(t)}</li>" for h, t in items) + f"</{tag}>"


def build():
    css = C.CSS.read_text()
    return f"""<title>Mutation Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{css}</style>
<main>
<header>
  <div class="eyebrow">Mutation report · qwen3-coder-30b</div>
  <h1>Why the mutation tool does not help, and how to fix it</h1>
  <p class="lede">{E(LEDE)}</p>
</header>
<section>
  <h2>Why it is not useful</h2>
  {bullets_html(WHY)}
</section>
<section>
  <h2>Changes to the current tool</h2>
  {bullets_html(CHANGE)}
</section>
<section>
  <h2>A new design: LLM-based mutation</h2>
  {bullets_html(LLM, ordered=True)}
</section>
</main>
"""


def build_md():
    L = ["# Mutation report: why the mutation tool does not help, and how to fix it", "", LEDE, "",
         "## Why it is not useful", ""]
    L += [f"- **{h}** {t}" for h, t in WHY]
    L += ["", "## Changes to the current tool", ""] + [f"- **{h}** {t}" for h, t in CHANGE]
    L += ["", "## A new design: LLM-based mutation", ""] + [f"{n}. **{h}** {t}" for n, (h, t) in enumerate(LLM, 1)]
    return "\n".join(L + [""])


if __name__ == "__main__":
    OUT.write_text(build())
    MD.write_text(build_md())
    print(OUT.relative_to(C.ROOT))
    print(MD.relative_to(C.ROOT))
