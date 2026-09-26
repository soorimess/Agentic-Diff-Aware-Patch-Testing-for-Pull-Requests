"""Build the comparison: data, charts, README.md, and the page published as the artifact.

    python experiments-v2/comparison/build.py

One text, two renderings. `content()` writes the analysis once, in Markdown, with every
figure read from data.json. README.md is that Markdown; page.html is the same Markdown
converted to HTML with the same chart files inlined. So the README and the artifact
cannot say different things or show different charts -- there is only one of each.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from charts import PALETTE, pfmt  # noqa: E402


def p_(p: float) -> str:
    return pfmt(p).replace("p=", "p = ").replace("p<", "p < ")


def content(d: dict) -> str:
    A = {a["num"]: a for a in d["arms"]}
    b = A["1"]
    P = d["pairs"]
    V1 = d["v1"]
    sig = [a for a in d["arms"] if a["vs_base"] and a["vs_base"]["p"] <= 0.05]
    spend = [a["spend"] for a in d["arms"]]
    judged = sum(a["judged"] for a in d["arms"])
    cov_sig = [a for a in d["arms"] if a["cov_paired"] and a["cov_paired"]["p"] <= 0.05]
    mut_sig = [a for a in d["arms"] if a["mut_paired"] and a["mut_paired"]["p"] <= 0.05]
    jud_sig = [a for a in d["arms"] if a["judge_paired"] and a["judge_paired"]["p"] <= 0.05]
    total_yes = sum(a["yes"] for a in d["arms"])
    v1_first_total = sum(V1[a["dir"]]["first_yes"] for a in d["arms"])
    s = d["patch_sizes"]
    top5 = sum(s[:5])
    c6, c78, c4, c810 = (P["coverage_reps"][k] for k in ("base→6", "7→8", "base→4", "8→10"))
    L = []
    w = L.append

    w("# Ten Arms, Take Two\n")
    w("The same seventy SWE-bench Verified pull requests and the same ten configurations as "
      "the first series, rerun on the rebuilt system. An agent writes a test that must fail "
      "before a bug fix and pass after it; each arm withholds one thing from it; every run is "
      "scored four ways — fail-to-pass, changed-line coverage, mutation kill rate and a "
      "judge's reading. What does each tool do to each score?\n")
    w("## The series at a glance\n")
    w(f"| | |\n|---|---|\n"
      f"| runs | **700**, one attempt per instance and arm — no best-of-two retry |\n"
      f"| fail-to-pass at baseline | **{b['yes']}/70** (v1: {V1['+second-chance']['first_yes']} "
      f"first attempt, {V1['+second-chance']['yes']} best of two) |\n"
      f"| fail-to-pass, all ten arms | **{total_yes}/700** (v1 first attempts: {v1_first_total}) |\n"
      f"| removals that moved fail-to-pass at p ≤ 0.05 | **{len(sig)} of 9** |\n"
      f"| removals that moved coverage at p ≤ 0.05 | **{len(cov_sig)} of 9** |\n"
      f"| paired mutation / judge comparisons at p ≤ 0.05 | {len(mut_sig)} of 9 / {len(jud_sig)} of 9 |\n"
      f"| spend per arm, agent and judge | ${min(spend):.2f}–${max(spend):.2f} |\n")
    w("![The four scores, arm by arm](charts/scoreboard.svg)\n")
    w("Fail-to-pass is a count. The coverage and mutation columns are movements, not "
      "percentages: on the instances that passed in both the base and the arm, how many got "
      "worse and how many got better when the feature was removed. A global average cannot be "
      "read across arms, because each arm averages over a different set of passing tests. The "
      "judge column is a distribution from one judge on a five-level scale.\n")
    w(f"**In one paragraph.** Each score answers to a different part of the system. "
      f"Fail-to-pass answers to `verify`: withholding it with the three features that need it "
      f"costs {b['yes'] - A['9']['yes']} instances ({p_(A['9']['vs_base']['p'])}), and nothing "
      f"else separates from the base. Coverage answers to the coverage tool and the duty to "
      f"act on it: every arm without one of them covers less of the change on the same "
      f"instances, {len(cov_sig)} of 9 at p ≤ 0.05, and the one arm that keeps both — "
      f"−mutation — does not move. Mutation and the judge move for nothing. The second chance "
      f"converted {b['sc_own_yes']} of the {b['sc_own']} runs it refused.\n")

    w("## 01 What changed since the first series\n")
    w("The first series ran the older harness. Reading its 700 trajectories found defects "
      "that changed verdicts, all fixed before this one (the full list is in "
      "`docs/bugs-from-700-runs.md`):\n")
    w("- **Every stop is checked**, not just the first: a refused stop used to go through "
      "on the second try. A test that cannot be scored is refused at most twice in a row.\n"
      "- **django's runner collects only `TestCase` methods**, and the briefing now says so.\n"
      "- **`verify`'s lines agree with its headline**, and a negative verdict is no longer "
      "sent as a tool error.\n"
      "- **A test that asserts the fix's source text is refused.** Six such YES were counted "
      "in the first series.\n"
      "- **Sampling temperature 0.3**, and `coverage` installed from a wheel fetched on the "
      "host, so the container never has a network.\n"
      "- **Each removal removes one thing.** Arms without the guard or the duty are no longer "
      "told those exist; the −repo-facts prompt no longer points at the repository root; the "
      "−second-chance arm stops refusing exactly where the base does.\n"
      "- **A run cut off by the gateway is BROKEN, not scored**, and the verdict scores the "
      "file the agent ended with.\n")
    w("Each of these was found by reading runs, first on five evaluation instances with all "
      "ten arms, then on the first two arms of this series, and fixed once before the full "
      "700 started. After that the code was frozen.\n")
    w("### One attempt, no retry\n")
    w("The first series retried every failure once and kept the better run. That retry "
      "measured the noise — 29% of failures passed on an unchanged re-run — but retrying only "
      "failures is one-sided: it gives a failure a second chance and never gives a success "
      "a chance to fail, which lifts every arm and compresses the differences. This series "
      "reports one attempt per instance. Runs that the OpenRouter key's monthly limit cut off "
      "partway (347, all BROKEN, none scored) were run again from scratch; that replaces an "
      "outage, not a verdict.\n")
    w(f"Every comparison is **paired**: the same instance in two arms, tested with "
      f"McNemar's exact test or a sign test. Between two arms, {d['churn'][0]} to "
      f"{d['churn'][1]} of the 70 instances change verdict in the two directions at once.\n")

    w("## 02 Fail-to-pass\n")
    w("![Fail-to-pass per arm](charts/f2p.svg)\n")
    rows = ["| # | arm | withheld | YES | net | up | down | p | v1 first | v1 best of two |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for a in d["arms"]:
        v = a["vs_base"]; o = V1[a["dir"]]
        rows.append(f"| {a['num']} | `{a['label']}` | {a['removed']} | **{a['yes']}** | "
                    + (f"{a['yes'] - b['yes']:+d} | {v['up']} | {v['down']} | {p_(v['p'])} |"
                       if v else "— | — | — | — |") + f" {o['first_yes']} | {o['yes']} |")
    w("\n".join(rows) + "\n")
    w(f"One removal clears p ≤ 0.05: the verify bundle (arm 9, {A['9']['yes'] - b['yes']:+d}). "
      f"−cov −mut is the nearest on the other side, {A['8']['yes'] - b['yes']:+d} at "
      f"{p_(A['8']['vs_base']['p'])}. Everything else sits within a few instances of the base "
      f"in both directions — the size of the gap between two runs of the same configuration.\n")
    w("### Against the first series\n")
    w("![Fail-to-pass, v1 against v2](charts/v1v2.svg)\n")
    reach = [a for a in d["arms"] if a["yes"] >= V1[a["dir"]]["yes"]]
    w(f"Every arm scores higher than its first-series first attempt, and {len(reach)} of ten "
      f"reach the first series' best of two in a single attempt. The largest gain is −repo-facts, "
      f"{V1['no-repo-facts']['first_yes']} → {A['5']['yes']}: that arm's prompt had told the "
      f"agent something false about where to put its test, and the cost the first series "
      f"attributed to the briefing (−11, p = 0.027) is gone "
      f"({A['5']['yes'] - b['yes']:+d}, {p_(A['5']['vs_base']['p'])}).\n")
    w("### How the failures failed\n")
    w("![What the failures were](charts/failures.svg)\n")
    w(f"\"Still fails after the fix\" is {b['why'].get('broken', 0)} in the base and "
      f"{A['9']['why'].get('broken', 0)} in the arm without verify: a test that does not work "
      f"looks like a correct one to an agent working at the base commit, and only verify runs "
      f"it on the fixed code. \"Passes before the fix\" ranges {min(a['why'].get('passes_at_base', 0) for a in d['arms'])}–"
      f"{max(a['why'].get('passes_at_base', 0) for a in d['arms'])} and follows no feature.\n")

    w("## 03 Coverage\n")
    w("Changed-line coverage asks whether the test went near the code the fix changed: run "
      "the generated test under coverage, look only at the executable lines the pull request "
      "adds, and report the fraction that ran. The harness computes it after the verdict; the "
      "agent never sees a percentage.\n")
    w("### Paired, instance by instance\n")
    w("![Coverage, paired against the base](charts/cov_paired.svg)\n")
    w(f"On instances that passed in both arms, each bar counts how many covered less (left) "
      f"or more (right) with the feature removed. {len(cov_sig)} of nine clear p ≤ 0.05, and "
      f"they are exactly the arms that lose the coverage tool or the duty to act on it:\n")
    rows = ["| removal | pairs | covered less | covered more | p |", "|---|---:|---:|---:|---:|"]
    for a in d["arms"][1:]:
        c = a["cov_paired"]
        rows.append(f"| {a['num']} {a['removed']} | {c['n']} | {c['fell']} | {c['rose']} | {p_(c['p'])} |")
    w("\n".join(rows) + "\n")
    w("The same removal can be asked twice, and here it replicates:\n")
    w("| pair asking the same question | pairs | fell | rose | p |\n|---|---:|---:|---:|---:|\n"
      f"| coverage tool: base → arm 6 | {c6['n']} | {c6['fell']} | {c6['rose']} | {p_(c6['p'])} |\n"
      f"| coverage tool: arm 7 → arm 8 | {c78['n']} | {c78['fell']} | {c78['rose']} | {p_(c78['p'])} |\n"
      f"| the duty: base → arm 4 | {c4['n']} | {c4['fell']} | {c4['rose']} | {p_(c4['p'])} |\n"
      f"| the duty: arm 8 → arm 10 | {c810['n']} | {c810['fell']} | {c810['rose']} | {p_(c810['p'])} |\n")
    w(f"The effect is real and it is small, and the corpus explains why. Base covers "
      f"{b['cov_pooled']}% of the changed lines its passing tests could reach; −coverage "
      f"covers {A['6']['cov_pooled']}%. Most fixes are tiny — the median adds "
      f"{sorted(s)[len(s) // 2]} executable lines — so most passing tests reach every changed "
      f"line with or without help. The tool matters on the minority where a line gets missed, "
      f"and there every paired difference points the same way.\n")
    w(f"> **The −coverage arms still hear a yes or no.** `verify` measures coverage itself "
      f"and says whether every changed line ran; the arms without the coverage tool receive "
      f"that as often as the base ({A['6']['reach_hint_runs']} runs in −coverage, "
      f"{b['reach_hint_runs']} in the base). What they lose is *which* lines and the code on "
      f"them. The drop above is the value of that detail, not of coverage feedback as a whole.\n")
    w("### Three numbers that do not rank the arms alike\n")
    w("![Three coverage numbers that do not rank the arms alike](charts/coverage3.svg)\n")
    rows = ["| # | arm | YES | mean per test | pooled | lines covered | share of "
            f"{d['corpus_lines']} | of the five largest |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]
    for a in d["arms"]:
        rows.append(f"| {a['num']} | `{a['label']}` | {a['yes']} | {a['cov_mean']}% | "
                    f"{a['cov_pooled']}% | {a['cov_lines']} | {a['cov_share']}% | "
                    f"{a['big5_yes']} of 5 |")
    w("\n".join(rows) + "\n")
    w(f"![The corpus is lopsided](charts/patches.svg)\n")
    w(f"The seventy fixes add {d['corpus_lines']} executable lines, and the five largest hold "
      f"{top5} of them ({round(100 * top5 / d['corpus_lines'])}%). Unpaired averages reward "
      f"passing fewer, and the corpus share is hostage to those five; the paired table is the "
      f"one to read.\n")

    w("## 04 Mutation score\n")
    w("Plausible wrong versions of the fix are generated from the real patch and both tests "
      "run against each. Only mutants the maintainer's test kills enter the denominator, and "
      "the gated rate is the share of those the generated test also kills.\n")
    rows = ["| # | arm | scored | gated mutants | killed | gated rate | raw rate |",
            "|---|---|---:|---:|---:|---:|---:|"]
    for a in d["arms"]:
        rows.append(f"| {a['num']} | `{a['label']}` | {a['mut_scored']} | {a['mut_gated_n']} | "
                    f"{a['mut_gated_k']} | {a['mut_rate']}% | {a['mut_raw']}% |")
    w("\n".join(rows) + "\n")
    w("![Mutation, paired against the base](charts/mut_paired.svg)\n")
    rates = [a["mut_rate"] for a in d["arms"]]
    w(f"The series spans {min(rates)}%–{max(rates)}%, and paired against the base "
      f"{'no row clears p ≤ 0.05' if not mut_sig else ', '.join('arm ' + a['num'] for a in mut_sig) + ' clear p ≤ 0.05'} "
      f"— including −mutation, the arm without the tool. The strongest lean is −coverage, "
      f"{A['6']['mut_paired']['fell']} lower and {A['6']['mut_paired']['rose']} higher "
      f"({p_(A['6']['mut_paired']['p'])}): a test that reaches more of the change also notices "
      f"more wrong versions of it, but not significantly. A surviving mutant names a behaviour "
      f"one test does not pin; between arms, at seventy instances, the score does not resolve.\n")

    w("## 05 The judge\n")
    w(f"A second model reads the generated test beside the maintainer's and answers three "
      f"questions a passing verdict cannot. It runs only after the verdict, and it is the only "
      f"step that opens the maintainer's test. {judged} passing tests were judged on one "
      f"five-level prompt.\n")
    w("| level | concept | issue coverage | readability |\n|---:|---|---|---|\n"
      "| 1 | different | none | reject |\n| 2 | tangential | minor only | poor |\n"
      "| 3 | narrower | main only | acceptable |\n| 4 | close | nearly complete | good |\n"
      "| 5 | equivalent | complete | exemplary |\n")
    w("![Judge verdicts, five levels, one judge](charts/judge.svg)\n")
    rows = ["| # | arm | judged | concept 1–5 | issue 1–5 | readability 1–5 | "
            "concept vs base: lower / higher | p |",
            "|---|---|---:|---|---|---|---|---:|"]
    for a in d["arms"]:
        jp = a["judge_paired"]
        rows.append(f"| {a['num']} | `{a['label']}` | {a['judged']} | "
                    f"{' · '.join(map(str, a['concept']))} | {' · '.join(map(str, a['issue']))} | "
                    f"{' · '.join(map(str, a['read']))} | "
                    + (f"{jp['fell']} / {jp['rose']} | {p_(jp['p'])} |" if jp else "— | — |"))
    w("\n".join(rows) + "\n")
    w(f"The judge's picture is the same in every arm: most passing tests are *narrower* than "
      f"the maintainer's and cover the main behaviour only, and readability is mostly "
      f"acceptable, spread from poor to good. No removal moves the concept level at p ≤ 0.05. What the judge measures — "
      f"how close a test is to the one a maintainer would write — is not something any of "
      f"these tools was built to change.\n")

    w("## 06 Do the four scores agree?\n")
    rows = ["| removal | fail-to-pass | coverage fell / rose | mutation fell / rose | "
            "judge lower / higher |", "|---|---|---|---|---|"]
    for a in d["arms"][1:]:
        v, c, m, j = a["vs_base"], a["cov_paired"], a["mut_paired"], a["judge_paired"]
        rows.append(f"| {a['num']} {a['removed']} | {a['yes'] - b['yes']:+d} {p_(v['p'])} | "
                    f"{c['fell']} / {c['rose']} {p_(c['p'])} | {m['fell']} / {m['rose']} "
                    f"{p_(m['p'])} | {j['fell']} / {j['rose']} {p_(j['p'])} |")
    w("\n".join(rows) + "\n")
    w("They do not have to agree, and they don't: they answer to different tools. `verify` "
      "moves fail-to-pass; the coverage tool and the duty move coverage; nothing here moves "
      "mutation or the judge. A tool can be worth keeping for one score and invisible to the "
      "rest.\n")

    vb = P["verify_broken"]
    w("## 07 verify\n")
    w(f"| removal | fail-to-pass | tests still failing after the fix |\n|---|---|---|\n"
      f"| base → arm 9 (verify and the three that need it) | {b['yes']} → {A['9']['yes']}, "
      f"{A['9']['vs_base']['up']} up / {A['9']['vs_base']['down']} down, {p_(A['9']['vs_base']['p'])} | "
      f"{b['why'].get('broken', 0)} → {A['9']['why'].get('broken', 0)} |\n"
      f"| arm 10 → arm 9 (verify alone) | {A['10']['yes']} → {A['9']['yes']}, "
      f"{P['verify_f2p']['up']} up / {P['verify_f2p']['down']} down, {p_(P['verify_f2p']['p'])} | "
      f"{vb['a10']} → {vb['a9']} ({vb['became']} became broken, {vb['fixed']} stopped) |\n")
    w("The agent works at the base commit and has never seen the fix, so when it runs its own "
      "test there, a correct test and a broken one look the same — both fail. verify is the "
      "only channel that applies the patch and runs the test on both sides. Isolated against "
      "arm 10 the direction holds but at this sample size it does not clear on its own; the "
      "bundle does.\n")

    w("## 08 The second chance\n")
    w(f"When the agent stops with a test that cannot score — it passes on the unfixed code, "
      f"collects nothing, or was never written — the second chance refuses the stop and says "
      f"why. In the base arm it refused {b['sc_own']} stops and {b['sc_own_yes']} of those runs "
      f"ended fail-to-pass. Told that its test passes before the fix, the agent recovered "
      f"{b['sc_pab_yes']} times in {b['sc_pab']}.\n")
    sc = d["second_chance_base"]
    w(f"The refusals were right and the agent acted on them. Of the {sc['refused']} refused "
      f"runs, {sc['ended_pab_or_yes']} ended exactly as refused (the test passed on the unfixed "
      f"code) or converted; {sc['with_diagnosis']} carried the diagnosis of which mistake the "
      f"test was making; after the first refusal the agent rewrote its test "
      f"{sc['writes_min']}–{sc['writes_max']} times (median {sc['writes_median']:g}) and called "
      f"`verify` again in {sc['verified_after']} of them. What it could not do was work out "
      f"what the fix changes. None of the defects still pending from reading the 700 runs "
      f"explains this: one refused run met a false source-text refusal, and it too ended with "
      f"a test that passes on the unfixed code.\n")
    w(f"Removing it reads {A['2']['yes'] - b['yes']:+d} ({p_(A['2']['vs_base']['p'])}), which "
      f"looks like the feature hurts. It cannot: until the agent first tries to stop, the two "
      f"arms receive the same prompt byte for byte, the same tools and the same code, and the "
      f"second chance only ever refuses a test that is not fail-to-pass, so it can add a pass "
      f"and never remove one. Its contribution is the {b['sc_own_yes']} it converted; the rest "
      f"of the gap is two independent samples of the same process diverging before it ever "
      f"acts. The finding is that a test aimed at the wrong behaviour almost never recovers, "
      f"refused or not.\n")

    w("## 09 What removal is worth\n")
    w("![What each arm cost against what it produced](charts/cost.svg)\n")
    rows = ["| # | arm | agent | judge | total spend | tokens | actions | per YES |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]
    for a in d["arms"]:
        rows.append(f"| {a['num']} | `{a['label']}` | ${a['cost_final']:.2f} | ${a['jcost']:.2f} | "
                    f"**${a['spend']:.2f}** | {a['tokens'] / 1e6:.1f}M | {a['actions']} | "
                    f"${a['spend'] / a['yes']:.3f} |")
    w("\n".join(rows) + "\n")
    w(f"−cov −mut keeps verify and the duty, drops both instruments, and reaches {A['8']['yes']} "
      f"for ${A['8']['spend']:.2f} against the base's {b['yes']} for ${b['spend']:.2f} — the "
      f"cheapest arm that loses no fail-to-pass, at the price of coverage "
      f"({A['8']['cov_paired']['fell']} covered less, {p_(A['8']['cov_paired']['p'])}).\n")

    w("## 10 What is wrong with this evidence\n")
    w("- **One attempt is one sample.** In the first series 29% of failures passed on an "
      "unchanged re-run; an arm's count here is noisy by several instances, which is why "
      "only paired tests are reported.\n"
      f"- **Three verdicts were re-scored offline.** A django status printed on a later line "
      f"than its test name was dropped by the output parser; the fixed parser re-read the "
      f"saved logs (−coverage and −cov −mut −duty django-16454 YES → NO, −repo-facts "
      f"django-16136 NO → YES). The re-scored YES has no coverage, mutation or judge figure.\n"
      "- **Known, not yet fixed, reached the agent.** Reading all 700 runs found a handful of "
      "cases where a tool told the agent something wrong — the same parser shape inside "
      "`verify`, a source-text refusal on a test that writes a fixture, a verify on another "
      "file closing the loop — each in a few runs spread across arms. They are listed in "
      "`docs/bugs-from-700-runs.md` and left for the next series.\n"
      "- **The −coverage arms keep verify's yes/no** about whether every changed line ran "
      "(section 03).\n"
      "- **The mutation score is asymmetric by construction**: held-out half when the agent "
      "holds the tool, whole pool when it does not.\n"
      f"- **The coverage denominator is an approximation.** The {d['corpus_lines']}-line corpus "
      f"is counted statically from each fix.diff.\n")

    w("## 11 What the series establishes\n")
    w(f"| tool | moves | evidence |\n|---|---|---|\n"
      f"| verify | fail-to-pass | {A['9']['yes'] - b['yes']:+d} with its dependants, "
      f"{p_(A['9']['vs_base']['p'])}; still-failing tests {b['why'].get('broken', 0)} → "
      f"{A['9']['why'].get('broken', 0)} |\n"
      f"| the coverage tool | coverage | {c6['fell']} / {c6['rose']} ({p_(c6['p'])}), again "
      f"{c78['fell']} / {c78['rose']} without the mutation tool |\n"
      f"| the duty to act on the tools | coverage | {c4['fell']} / {c4['rose']} ({p_(c4['p'])}), "
      f"again {c810['fell']} / {c810['rose']} ({p_(c810['p'])}) |\n"
      f"| the mutation tool | nothing measured | fail-to-pass {A['7']['yes'] - b['yes']:+d}, "
      f"mutation {A['7']['mut_paired']['fell']} / {A['7']['mut_paired']['rose']} |\n"
      f"| the second chance | {b['sc_own_yes']} conversion in {b['sc_own']} refusals | "
      f"identical to −second-chance until the first stop |\n"
      f"| the testing briefing | nothing measured in v2 | {A['5']['yes'] - b['yes']:+d}; the v1 "
      f"effect came from a misleading prompt |\n"
      f"| the source guard | an integrity check | {A['3']['yes'] - b['yes']:+d}; invisible to "
      f"every score by design |\n")
    w("---\n")
    w("Every figure here is computed from the run directories by `data.py`; the charts are "
      "drawn by `charts.py`; `build.py` writes this README and the published page from one "
      "text. Significance is McNemar's exact test on paired flip tables, or a sign test on "
      "paired movements.\n")
    return "\n".join(L)


# --------------------------------------------------------------------------- markdown
def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href='\2'>\1</a>", s)
    return s


def md_to_html(md: str) -> str:
    """The subset build.py writes: headings, paragraphs, tables, quotes, lists, images."""
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if m := re.match(r"!\[([^\]]*)\]\(([^)]+)\)", ln.strip()):
            svg = (HERE / m.group(2)).read_text()
            out.append(f"<figure class='chart'>{svg}</figure>")
            i += 1; continue
        if m := re.match(r"(#{1,4}) (.*)", ln):
            n = len(m.group(1)); text = m.group(2)
            if k := re.match(r"(\d\d) (.*)", text):
                out.append(f"<h{n}><span class='num'>{k.group(1)}</span>{inline(k.group(2))}</h{n}>")
            else:
                out.append(f"<h{n}>{inline(text)}</h{n}>")
            i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, align, body = rows[0], rows[1], rows[2:]
            right = [a.endswith(":") for a in align]
            th = "".join(f"<th{' class=r' if right[j] else ''}>{inline(c)}</th>" for j, c in enumerate(head))
            tb = "".join("<tr>" + "".join(f"<td{' class=r' if right[j] else ''}>{inline(c)}</td>"
                                         for j, c in enumerate(r)) + "</tr>" for r in body)
            out.append(f"<div class='tw'><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>")
            continue
        if ln.startswith(">"):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip()); i += 1
            out.append(f"<aside class='note'><p>{inline(' '.join(q))}</p></aside>")
            continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip():
                if lines[i].startswith("- "):
                    items.append(lines[i][2:])
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if ln.strip() == "---":
            out.append("<hr>"); i += 1; continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||>|!\[|- )", lines[i]):
            para.append(lines[i]); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def page(md: str) -> str:
    light = "".join(f"--k-{k}:{v[0]};" for k, v in PALETTE.items())
    dark = "".join(f"--k-{k}:{v[1]};" for k, v in PALETTE.items())
    body = md_to_html(md)
    title, _, rest = body.partition("\n")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ten Arms, Take Two</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600&display=swap">
<style>
:root{{--bg:#f6f7f9;--panel:#ffffff;--text:#1b2029;--muted:#5b6472;--line:#dfe3e9;
--accent:#5b4bd6;--accent-soft:#ecebfb;--code:#eef0f4;{light}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0e1116;--panel:#151a21;
--text:#e6eaf0;--muted:#98a1ad;--line:#262d36;--accent:#9d8cff;--accent-soft:#1f1b3a;--code:#1b2129;{dark}}}}}
:root[data-theme="dark"]{{--bg:#0e1116;--panel:#151a21;--text:#e6eaf0;--muted:#98a1ad;--line:#262d36;
--accent:#9d8cff;--accent-soft:#1f1b3a;--code:#1b2129;{dark}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.62 "IBM Plex Sans",system-ui,sans-serif}}
main{{max-width:1040px;margin:0 auto;padding:48px 16px 80px}}
h1{{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:clamp(34px,6vw,54px);line-height:1.05;
letter-spacing:-.01em;margin:0 0 18px;text-wrap:balance}}
h1+p{{font-size:18px;color:var(--muted);max-width:68ch;margin:0 0 28px}}
h2{{font-size:24px;margin:56px 0 12px;padding-top:18px;border-top:1px solid var(--line);text-wrap:balance}}
h3{{font-size:18px;margin:32px 0 8px}}
.num{{font-family:"IBM Plex Mono",monospace;font-size:.7em;color:var(--accent);margin-right:12px;
letter-spacing:.06em;vertical-align:.12em}}
p,li{{max-width:72ch}}
code{{font-family:"IBM Plex Mono",monospace;font-size:.88em;background:var(--code);padding:1px 5px;border-radius:4px}}
.tw{{overflow-x:auto;margin:14px 0 22px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}}
table{{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}}
th,td{{padding:7px 12px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}}
th{{font-weight:600;color:var(--muted);font-size:12px;letter-spacing:.04em;text-transform:uppercase}}
td.r,th.r{{text-align:right}} tr:last-child td{{border-bottom:0}}
figure.chart{{margin:18px 0 22px;padding:16px;background:var(--panel);border:1px solid var(--line);
border-radius:10px;overflow-x:auto}}
figure.chart svg{{display:block;max-width:none;height:auto}}
aside.note{{margin:18px 0;padding:12px 16px;border-left:3px solid var(--accent);background:var(--accent-soft);
border-radius:0 8px 8px 0}} aside.note p{{margin:0}}
hr{{border:0;border-top:1px solid var(--line);margin:48px 0 16px}}
hr+p{{color:var(--muted);font-size:14px}}
a{{color:var(--accent)}}
</style></head><body><main>
{title}
{rest}
</main></body></html>
"""


def main() -> None:
    root = HERE.parents[1]
    data = subprocess.run([sys.executable, str(HERE / "data.py")], capture_output=True,
                          text=True, check=True, cwd=root).stdout
    (HERE / "data.json").write_text(data)
    subprocess.run([sys.executable, str(HERE / "charts.py"), str(HERE / "data.json")],
                   check=True, cwd=root)
    d = json.loads(data)
    md = content(d)
    reading = (HERE / "judge_reading.md")
    md = md.replace("JUDGE_READING", reading.read_text().strip() if reading.exists() else "")
    (HERE / "README.md").write_text(md)
    (HERE / "page.html").write_text(page(md))
    print("wrote README.md and page.html")


if __name__ == "__main__":
    main()
