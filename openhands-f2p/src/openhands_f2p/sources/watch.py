"""Scan finished runs for every failure signature found so far, so none repeats unseen.

    uv run python -m openhands_f2p.sources.watch ../chaco-outs/base [--json]

Read-only. Each finished run (a directory with result.json) is checked against the
harness, environment and logic problems the ChaCo audits found (2026-10-09..11). A hit
is not a verdict on the run; it is a reason to read that trajectory before more runs
start. `--json` prints machine-readable findings.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# (name, severity, where, pattern). `where`: "tools" (text the agent was shown), "logs"
# (verdict test runs), "child" (the process log), "prompt" (first prompt), "test" (final
# test file). severity: "stop" = a harness/environment bug, fix before more runs;
# "read" = read the trajectory; "note" = informational.
SIGNATURES = [
    ("env-import-of-new-test", "stop", "tools",
     r"ModuleNotFoundError: No module named '[\w.]+\.tests?\.test_f2p"),
    ("meson-rebuild", "stop", "tools", r"meson-python: building|re-building the \w+ meson"),
    ("meson-rebuild-failed", "stop", "tools", r"CalledProcessError: Command '\['/usr/local/bin/ninja'"),
    ("illegal-instruction", "stop", "tools", r"Illegal instruction"),
    ("missing-package", "stop", "tools",
     r"No module named '(matplotlib|pylatexenc|seaborn|PIL|pyarrow|numba|jinja2)'"),
    ("collection-incompatible", "stop", "tools", r"object has no attribute 'runTest'"),
    ("harness-exception", "stop", "child", r"Traceback \(most recent call last\)"),
    ("patch-apply-failure", "stop", "child", r"could not apply patch|'--3way' outside a repository"),
    ("old-prompt", "stop", "prompt", r"BEFORE a bug was fixed|The bug report:"),
    ("exec-timeout", "read", "tools", r"timed out after \d+s"),
    ("masks-new-api-error", "read", "test",
     r"except\s*\(?\s*(TypeError|ImportError|AttributeError|ModuleNotFoundError)[^:]*:\s*\n\s*"
     r"(pass|self\.skipTest|pytest\.skip|return)"),
    ("skips-itself", "read", "test", r"self\.skipTest\(|pytest\.skip\("),
    ("patch-clipped", "note", "prompt", r"hunks are not shown, to keep this short"),
]


def _shown(run: Path) -> str:
    try:
        log = json.loads((run / "tool_log.json").read_text())
    except (OSError, ValueError):
        return ""
    return "\n".join(str(e.get("shown") or "") for e in log)


def _prompt(run: Path) -> str:
    try:
        traj = json.loads((run / "trajectory.json").read_text())
    except (OSError, ValueError):
        return ""
    text = json.dumps(traj)[:400000]
    return text.encode().decode("unicode_escape", errors="ignore")


def scan(run: Path) -> dict:
    r = json.loads((run / "result.json").read_text())
    texts = {
        "tools": _shown(run),
        "logs": "".join((run / f).read_text(errors="replace")
                        for f in ("before_fix.log", "after_fix.log") if (run / f).exists()),
        "child": (run / "child.log").read_text(errors="replace") if (run / "child.log").exists() else "",
        "prompt": _prompt(run),
        "test": "".join(p.read_text(errors="replace") for p in run.glob("test_f2p_*.py")),
    }
    hits = []
    for name, sev, where, pat in SIGNATURES:
        m = re.search(pat, texts[where])
        if m:
            hits.append({"signature": name, "severity": sev,
                         "evidence": texts[where][max(0, m.start() - 80):m.end() + 80]
                         .replace("\n", " ")[:240]})
    # Structural checks.
    why = r.get("why") or ""
    if r.get("f2p") == "BROKEN":
        hits.append({"signature": "broken", "severity": "stop", "evidence": why[:200]})
    if r.get("f2p") == "NO" and re.search(r"still failing after the fix \(\['[^']+\.py'\]\)", why):
        hits.append({"signature": "file-level-error-after-fix", "severity": "read",
                     "evidence": why[:200]})
    if (r.get("actions") or 0) >= 120:
        hits.append({"signature": "near-cap", "severity": "read",
                     "evidence": f"{r.get('actions')} actions"})
    try:
        log = json.loads((run / "tool_log.json").read_text())
    except (OSError, ValueError):
        log = []
    tools = [e.get("tool") for e in log]
    first_flip = next((i for i, e in enumerate(log)
                       if e.get("tool") == "verify" and e.get("flipped")), None)
    before = [e for i, e in enumerate(log) if e.get("tool") == "coverage"
              and (first_flip is None or i < first_flip)]
    # Since 2026-10-12 `coverage` refuses before the flip; a measured call there means
    # the gate did not hold. Refusals are counted only.
    measured = sum(1 for e in before if "error" not in e)
    if measured:
        hits.append({"signature": "coverage-before-flip", "severity": "stop",
                     "evidence": f"{measured} coverage calls measured before any flip"})
    if len(before) - measured >= 4:
        hits.append({"signature": "coverage-refused", "severity": "note",
                     "evidence": f"{len(before) - measured} coverage calls refused before "
                                 f"the flip, {tools.count('verify')} verify calls"})
    try:
        injected = json.loads((run / "injected_messages.json").read_text())
    except (OSError, ValueError):
        injected = []
    refusals = sum(1 for m in injected if "refused" in json.dumps(m).lower())
    if refusals >= 6:
        hits.append({"signature": "refusal-loop", "severity": "read",
                     "evidence": f"{refusals} refusals"})
    tp = r.get("test_path") or ""
    pr = json.loads((run / "pr.json").read_text()) if (run / "pr.json").exists() else {}
    srcs = [ln.split(" b/", 1)[-1] for ln in (pr.get("patch") or "").splitlines()
            if ln.startswith("diff --git ") and ln.endswith(".py")]
    if srcs and tp.startswith("scipy/") and not any(
            tp.split("/")[1] == s.split("/")[1] for s in srcs if s.startswith("scipy/")):
        hits.append({"signature": "test-far-from-change", "severity": "read",
                     "evidence": f"{tp} for {srcs[:2]}"})
    mut = r.get("mutation") or {}
    dev = mut.get("developer") or {}
    if mut.get("measured") and dev.get("killed") is None and \
            "pass on the fixed code" in str(dev.get("why")) and not (pr.get("FAIL_TO_PASS") in (None, "[]")):
        hits.append({"signature": "developer-unmeasured", "severity": "read",
                     "evidence": str(dev.get("why"))[:160]})
    cov = r.get("changed_line_coverage") or {}
    if cov.get("unimported_files"):
        hits.append({"signature": "unimported-changed-files", "severity": "note",
                     "evidence": ", ".join(cov["unimported_files"][:3])})
    return {"id": run.name, "f2p": r.get("f2p"), "actions": r.get("actions"),
            "why": why[:120], "hits": hits}


def main() -> int:
    root = Path(sys.argv[1])
    rows = [scan(d) for d in sorted(root.iterdir())
            if d.is_dir() and (d / "result.json").exists()]
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
        return 0
    stops = 0
    for row in rows:
        sev = {h["severity"] for h in row["hits"]}
        mark = "STOP" if "stop" in sev else "read" if "read" in sev else "ok"
        stops += mark == "STOP"
        print(f"{mark:5s} {row['f2p']:6s} {row['id']:30s} {row['actions']!s:>4} | {row['why'][:70]}")
        for h in row["hits"]:
            print(f"        [{h['severity']}] {h['signature']}: {h['evidence'][:160]}")
    print(f"\n{len(rows)} finished; {stops} with a stop-level signature")
    return 1 if stops else 0


if __name__ == "__main__":
    sys.exit(main())
