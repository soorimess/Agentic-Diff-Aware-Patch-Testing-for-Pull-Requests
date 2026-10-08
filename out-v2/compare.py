"""Compare two experiment folders of out-v2 on the same 36 PRs.

    python3 out-v2/compare.py base no-second-chance

Writes `out-v2/compare/<a>-vs-<b>.md` and prints it.

The comparison metric for coverage (user, 2026-10-04): covered lines / all executable
changed lines, pooled over the PRs that are YES in *both* runs -- one denominator for both
sides. Each run's own figure is the mean of its per-PR coverage over its YES PRs (that is
what RUNS.md leads with); it is shown too, but two runs with different YES sets are not
compared on it.

Two rows guard against a misreading: the pooled figures again without the one PR that
moves the gap most (a single PR flipped base vs no-require-tools), and how many runs the
verify loop refused that still ended YES without a restart.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str) -> dict[str, dict]:
    out = {}
    for f in sorted((HERE / name).glob("*/result.json")):
        out[f.parent.name] = json.loads(f.read_text())
    return out


def cov(r: dict) -> dict | None:
    c = r.get("changed_line_coverage") or {}
    return c if r.get("f2p") == "YES" and c.get("measured") else None


def pooled(rows: list[dict], key: str = "") -> tuple[int, int]:
    hit = tot = 0
    for c in rows:
        c = (c.get(key) or {}) if key else c
        if c.get("covered") is None or not c.get("executable_changed_lines"):
            continue
        hit += c["covered"]
        tot += c["executable_changed_lines"]
    return hit, tot


def pct(h: int, t: int) -> str:
    return f"{100 * h / t:.1f}% ({h}/{t})" if t else "--"


def first_verdict(r: dict) -> str:
    sc = r.get("second_chance") or {}
    return sc.get("first_verdict") or r.get("f2p", "?")


def main(a: str, b: str) -> str:
    A, B = load(a), load(b)
    ids = sorted(set(A) | set(B))
    common = [i for i in ids if i in A and i in B]
    yes_a = [i for i in common if A[i].get("f2p") == "YES"]
    yes_b = [i for i in common if B[i].get("f2p") == "YES"]
    both = [i for i in common if i in yes_a and i in yes_b]
    rescued = lambda R: [i for i in R if (R[i].get("second_chance") or {}).get("first_verdict")
                         and R[i].get("f2p") == "YES"]

    # Coverage: the comparison number, on the PRs YES in both.
    both_a = [cov(A[i]) for i in both if cov(A[i]) and cov(B[i])]
    both_b = [cov(B[i]) for i in both if cov(A[i]) and cov(B[i])]
    n_cov = len(both_a)
    own = lambda R, ys: [cov(R[i])["percent"] for i in ys if cov(R[i])]
    mean = lambda xs: f"{sum(xs) / len(xs):.1f}% over {len(xs)}" if xs else "--"

    # Mutation, same PRs, where both measured on the same held-out pool.
    def mut(R, side, ids=None):
        k = t = 0
        for i in (both if ids is None else ids):
            m = R[i].get("mutation") or {}
            s = m.get(side) or {}
            if m.get("measured") and m.get("total") and s.get("killed") is not None:
                k += s["killed"]
                t += m["total"]
        return k, t
    mut_ids = [i for i in both if all(
        (R[i].get("mutation") or {}).get("measured") and (R[i].get("mutation") or {}).get("total")
        for R in (A, B))]

    # One PR can carry a pooled figure (seaborn-3069, base vs no-require-tools: 11 of 60
    # lines, 9% vs 100%, flipped the coverage comparison). The PR whose removal moves the
    # gap between the two sides most is named, with both figures recomputed without it.
    def without_most(ids, score):
        def gap(xs):
            (ha, ta), (hb, tb) = score(A, xs), score(B, xs)
            return (hb / tb if tb else 0) - (ha / ta if ta else 0)
        full = gap(ids)
        if len(ids) < 2:
            return None, ids
        move = {i: abs(full - gap([j for j in ids if j != i])) for i in ids}
        drop = max(ids, key=move.get)
        if move[drop] < 1e-9:
            return None, ids                     # no single PR moves it
        return drop, [j for j in ids if j != drop]
    cov_ids = [i for i in both if cov(A[i]) and cov(B[i])]
    cov_score = lambda R, xs: pooled([cov(R[i]) for i in xs])
    cov_drop, cov_rest = without_most(cov_ids, cov_score)
    mut_score = lambda R, xs: mut(R, "agent", xs)
    mut_drop, mut_rest = without_most(mut_ids, mut_score)

    # How often a stop refused for the verify loop ends YES in the same conversation --
    # what `require-tools` adds to the fail-to-pass count (base before the 2026-10-05 reruns: 1 of 11).
    VERIFY_LOOP = {"no_test", "collects_nothing", "passes_at_base", "skipped_at_base",
                   "verify_open"}

    def converted(name, R):
        refused = turned = 0
        for i in common:
            f = HERE / name / i / "injected_messages.json"
            got = json.loads(f.read_text()) if f.is_file() else []
            if any(isinstance(m, dict) and m.get("reason") in VERIFY_LOOP for m in got):
                refused += 1
                sc = R[i].get("second_chance") or {}
                turned += R[i].get("f2p") == "YES" and not sc.get("first_verdict")
        return f"{turned} of {refused}" if refused else "none refused"

    def acts(R):
        return sum(R[i].get("actions") or 0 for i in common)

    def cost(R):
        return sum(((R[i].get("usage") or {}).get("cost_usd") or 0) for i in common)

    def meaningful(R, ys):
        got = [((R[i].get("concept") or {}).get("meaningful") or {}).get("answer") for i in ys]
        judged = [g for g in got if g in ("yes", "no")]
        return f"{judged.count('yes')}/{len(judged)} judged" if judged else "not judged"

    out = [f"# {a} vs {b}", "",
           f"Same {len(common)} PRs, {len(both)} YES in both. Coverage is compared on the "
           f"**{n_cov} of them with coverage measured**: covered / all changed lines, pooled "
           f"(user, 2026-10-04). A pooled figure weights each line, so a PR with many changed "
           f"lines moves it most -- the per-PR differences are listed below.", ""]
    for n in (a, b):
        if (HERE / n / "PICKED.md").is_file():
            out += [f"**Provenance of `{n}`:** picked runs -- per PR the "
                    + ("best" if "best" in n else "worst") + " of several runs of the same "
                    "system and configuration (see its `PICKED.md`). Best against worst shows "
                    "the largest effect possible, not the expected one.", ""]
            continue
        f = HERE / n / "REUSED.md"
        if not f.is_file():
            continue
        best = "Best of two" in f.read_text()
        out += [f"**Provenance of `{n}`:** its runs come from several batches of the same system"
                + (" and some PRs keep the better of two runs, which favours it slightly"
                   if best else "") + " (see its `REUSED.md`).", ""]
    out += ["| | " + a + " | " + b + " |", "|---|---|---|",
            f"| fail-to-pass | **{len(yes_a)}/{len(common)}** | **{len(yes_b)}/{len(common)}** |",
            f"| first attempts alone | {sum(first_verdict(A[i]) == 'YES' for i in common)}/{len(common)} "
            f"| {sum(first_verdict(B[i]) == 'YES' for i in common)}/{len(common)} |",
            f"| rescued by the second chance | {len(rescued(A))} | {len(rescued(B))} |",
            f"| runs refused by the verify loop that still ended YES without a restart "
            f"| {converted(a, A)} | {converted(b, B)} |",
            f"| **coverage, pooled over the {n_cov} PRs YES in both (comparison)** "
            f"| **{pct(*pooled(both_a))}** | **{pct(*pooled(both_b))}** |",
            (f"| same, without `{cov_drop}` (the PR that moves the gap most) "
             f"| {pct(*cov_score(A, cov_rest))} | {pct(*cov_score(B, cov_rest))} |"
             if cov_drop else "| same, without any one PR | no single PR moves the gap | |"),
            f"| same, without import-time lines | {pct(*pooled(both_a, 'excluding_import_time'))} "
            f"| {pct(*pooled(both_b, 'excluding_import_time'))} |",
            f"| coverage, mean of per-PR over own YES (each run's own) "
            f"| {mean(own(A, yes_a))} | {mean(own(B, yes_b))} |",
            f"| mutants caught by the agent's test, pooled over {len(mut_ids)} PRs YES in both "
            f"| {pct(*mut(A, 'agent'))} | {pct(*mut(B, 'agent'))} |",
            (f"| same, without `{mut_drop}` (the PR that moves the gap most) "
             f"| {pct(*mut_score(A, mut_rest))} | {pct(*mut_score(B, mut_rest))} |"
             if mut_drop else "| same, without any one PR | no single PR moves the gap | |"),
            f"| meaningful (judge) | {meaningful(A, yes_a)} | {meaningful(B, yes_b)} |",
            f"| actions, all PRs | {acts(A)} | {acts(B)} |",
            f"| model cost | ${cost(A):.2f} | ${cost(B):.2f} |", ""]

    flips = [i for i in common if A[i].get("f2p") != B[i].get("f2p")]
    out += [f"## Verdicts that differ ({len(flips)})", "",
            f"| PR | {a} | {b} | why {b} |", "|---|---|---|---|"]
    for i in flips:
        def cell(R):
            r = R[i]
            sc = r.get("second_chance") or {}
            tag = " (rescued)" if sc.get("first_verdict") and r.get("f2p") == "YES" else ""
            return f"{r.get('f2p')}{tag}"
        out.append(f"| `{i}` | {cell(A)} | {cell(B)} | {(B[i].get('why') or '')[:90]} |")

    diff = [(i, cov(A[i])["percent"], cov(B[i])["percent"]) for i in both
            if cov(A[i]) and cov(B[i]) and cov(A[i])["percent"] != cov(B[i])["percent"]]
    out += ["", f"## Coverage differences on PRs YES in both ({len(diff)})", "",
            f"| PR | {a} | {b} |", "|---|---|---|"]
    out += [f"| `{i}` | {x:.0f}% | {y:.0f}% |" for i, x, y in diff]
    def mrow(R, i):
        m = R[i].get("mutation") or {}
        return f"{(m.get('agent') or {}).get('killed')}/{m.get('total')}"
    mdiff = [i for i in mut_ids if mrow(A, i) != mrow(B, i)]
    out += ["", f"## Mutation differences on PRs YES in both ({len(mdiff)})", "",
            f"| PR | {a} | {b} |", "|---|---|---|"]
    out += [f"| `{i}` | {mrow(A, i)} | {mrow(B, i)} |" for i in mdiff]
    text = "\n".join(out) + "\n"
    dest = HERE / "compare" / f"{a}-vs-{b}.md"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(text)
    return text


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(main(sys.argv[1], sys.argv[2]))
