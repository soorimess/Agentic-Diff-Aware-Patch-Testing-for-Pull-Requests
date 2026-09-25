"""Build the ten-arm comparison from collected data. Regenerate, never hand-edit."""
import json, sys, pathlib

d = json.load(open(sys.argv[1]))
arms = {a["num"]: a for a in d["arms"]}
order = [a["num"] for a in d["arms"]]
CORPUS = d["corpus_lines"]
out = []
w = out.append

def arm(n): return arms.get(n)
def fmt(v, s="%s"): return "—" if v is None else s % v

w("# Ten arms on seventy pull requests\n")
w("Every arm is the same seventy SWE-bench Verified instances, the same model")
w("(`qwen3-coder-30b-a3b-instruct` pinned to one provider), the same harness commit, and")
w("`--second-chance` on, except where the arm is about removing it. Each withholds exactly")
w("one thing from the agent. The harness measures the same quantities either way, so the")
w("arms differ only by what the agent was given.\n")
w("Every comparison below is **paired**: the same instance in two arms, read as a")
w("flip table rather than two totals. On seventy instances with this much run-to-run")
w("movement, totals are not readable and pairing is not optional.\n")

w("## What flipped\n")
w("![fail-to-pass by arm](charts/f2p.svg)\n")
w("| # | arm | withheld | YES | net | up | down | p |")
w("|---|---|---|---:|---:|---:|---:|---:|")
for n in order:
    a = arm(n)
    net = a["yes"] - arms["1"]["yes"]
    star = " ★" if a["p"] <= 0.05 and n != "1" else ""
    w("| %s | `%s` | %s | **%d** | %s | %d | %d | %s%s |" % (
        n, a["label"], a["removed"], a["yes"],
        "—" if n == "1" else "%+d" % net, a["up"], a["down"],
        "—" if n == "1" else "%.3f" % a["p"], star))
w("")
sig = [n for n in order if n != "1" and arms[n]["p"] <= 0.05]
w("**%s of nine comparisons clear p ≤ 0.05**: %s.\n" % (
    {0:"None",1:"One",2:"Two",3:"Three"}.get(len(sig), str(len(sig))),
    ", ".join("arm %s (`%s`)" % (n, arms[n]["label"]) for n in sig) or "none"))
w("Everything else sits between −5 and +2 with p from 0.30 to 1.00. Those are not small")
w("effects that need more data to confirm; on this corpus they are indistinguishable from")
w("re-running the same configuration twice.\n")

w("## How the failures failed\n")
w("![failure modes](charts/failures.svg)\n")
w("The verdict count says how many arms lost. This says what they lost to, and it is where")
w("the instruments separate.\n")
w("| # | arm | fails after the fix | passes at base | never ran | other |")
w("|---|---|---:|---:|---:|---:|")
for n in order:
    a = arm(n); y = a["why"]
    other = sum(v for k, v in y.items() if k not in ("broken", "passes_at_base", "collects_nothing"))
    w("| %s | `%s` | %s | %d | %d | %d |" % (
        n, a["label"],
        "**%d**" % y.get("broken", 0) if y.get("broken", 0) >= 20 else y.get("broken", 0),
        y.get("passes_at_base", 0), y.get("collects_nothing", 0), other))
w("")

w("## Changed-line coverage, paired\n")
w("![paired coverage](charts/coverage.svg)\n")
w("Only instances that passed in **both** arms, so the comparison is about test quality")
w("rather than how many tests survived. An arm that produced fewer but easier tests scores")
w("better on any unpaired coverage figure, which is exactly the trap here.\n")
w("| # | arm | paired n | with | without | fell | rose | p |")
w("|---|---|---:|---:|---:|---:|---:|---:|")
for n in order[1:]:
    a = arm(n)
    if not a["paired_n"]: continue
    w("| %s | `%s` | %d | %s%% | %s%% | %d | %d | %.2f |" % (
        n, a["label"], a["paired_n"], fmt(a["paired_base"]), fmt(a["paired_arm"]),
        a["cov_fell"], a["cov_rose"], a["cov_p"]))
w("")

w("## What each arm cost\n")
w("![cost against fail-to-pass](charts/cost.svg)\n")
w("| # | arm | agent | judge | total | tokens | actions | per YES |")
w("|---|---|---:|---:|---:|---:|---:|---:|")
for n in order:
    a = arm(n); tot = a["cost"] + a["jcost"]
    w("| %s | `%s` | $%.2f | $%.2f | **$%.2f** | %.1fM | %d | $%.3f |" % (
        n, a["label"], a["cost"], a["jcost"], tot, a["tokens"]/1e6, a["actions"],
        tot / a["yes"] if a["yes"] else 0))
w("")
pathlib.Path(sys.argv[2]).write_text("\n".join(out) + "\n")
print("wrote", sys.argv[2], "(%d lines)" % len(out))

# ---- sections that need the cross-arm numbers -------------------------------
X = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
if X:
    out = []
    w = out.append
    v, vb = X["verify"], X["verify_broken"]
    w("## Isolating `verify`\n")
    w("Arm 9 is a four-way change: `verify` is a dependency of the coverage tool, the")
    w("mutation tool and the tool duty, so withholding it withholds all four and leaves the")
    w("agent no instruments at all. Arm 10 withholds the other three and keeps `verify`, so")
    w("**the pair differs by that one tool**.\n")
    w("| | fail-to-pass | up | down | p |")
    w("|---|---:|---:|---:|---:|")
    w("| arm 10 → arm 9, removing `verify` | %d → %d (%+d) | %d | %d | **%.3f** |" %
      (v["from"], v["to"], v["to"] - v["from"], v["up"], v["down"], v["p"]))
    w("")
    w("On the verdict count that is suggestive and short of significant, with %d instances"
      % (v["up"] + v["down"]))
    w("discordant. But the verdict is the wrong place to look: a broken test only changes a")
    w("verdict when that instance would otherwise have passed, and most would not have. The")
    w("mechanism is where the evidence is.\n")
    w("| paired on *did this instance produce a test that fails after the fix?* | |")
    w("|---|---:|")
    w("| broken with `verify` (arm 10) | %d |" % vb["a10"])
    w("| broken without it (arm 9) | **%d** |" % vb["a9"])
    w("| became broken when `verify` was removed | **%d** |" % vb["became"])
    w("| stopped being broken | %d |" % vb["fixed"])
    w("| McNemar | **p = %.4f** |" % vb["p"])
    w("")
    w("**This is the firmest result in the series.** And the reason is structural, not a")
    w("matter of the model trying harder. The agent works in a checkout at base and has")
    w("never seen the fix; when it runs its own test there, a correct test and a broken one")
    w("look identical, because both fail. Only `verify` applies the patch and runs the test")
    w("on both sides. It is the single channel through which the agent can learn that its")
    w("test fails for the wrong reason, and that fact cannot be handed over any other way")
    w("without also telling it what the fix does.\n")

    w("## Where a single arm was not enough\n")
    w("Arm 8 withholds two instruments at once, which makes some comparisons available")
    w("twice. Twice is the minimum needed to notice when a result does not hold.\n")
    w("**The coverage tool.** Arm 6 looked like a finding and did not survive re-asking:\n")
    w("| pair | n | coverage fell | rose | p |")
    w("|---|---:|---:|---:|---:|")
    for r in X["coverage_reps"]:
        w("| %s | %d | %d | %d | %.2f |" % (r["pair"], r["n"], r["fell"], r["rose"], r["p"]))
    w("")
    w("The first row was reported as a result when it was found. The second asks the same")
    w("question of a different set of instance-pairs and answers three and three. The")
    w("direction has never reversed -- no arm has ever shown coverage *rising* when the tool")
    w("was removed -- but five points was one arm's number, not an established effect.\n")
    w("**The mutation tool.** Two independent tests, both null:\n")
    w("| pair | up | down | p |")
    w("|---|---:|---:|---:|")
    for r in X["mutation_reps"]:
        w("| %s | %d | %d | %.2f |" % (r["pair"], r["up"], r["down"], r["p"]))
    w("")
    pathlib.Path(sys.argv[2]).write_text(pathlib.Path(sys.argv[2]).read_text() + "\n".join(out) + "\n")
    print("appended cross-arm sections")
