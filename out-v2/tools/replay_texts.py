"""Which runs saw tool text that the 2026-10-06 fixes change? (read from tool_log.json)

    F2P_PRS_FILE=../evaluation/local-36-prs.json uv run python ../out-v2/tools/replay_texts.py <folder>...

- header:    a verify / run_tests output carrying astropy's report header or pytest/pluggy
             runner frames, which `_condense` now drops (the window then shows other lines)
- spawn:     verify / coverage said changed lines never ran, about a test that starts a
             child process (now followed by the child-process note)
- backwards: a "backwards" headline while another test failed on both sides (now named)
- pytester:  a run_tests summary that listed ids of a pytester temp file (now left out)
- dir-filter: a run_tests on a directory whose real ids the 252dd3aa filter dropped
- phantom-id: pytest's `SKIPPED [1] ...` summary read as a test named "[1]"
"""
import json
import sys
from pathlib import Path

from openhands_f2p import verify as V
from openhands_f2p.sandbox_tools import _RUNNER_FRAME

HEADER = ("Running tests with Astropy version", "Internet access disabled")


def scan(d: Path) -> list[str]:
    log = json.loads((d / "tool_log.json").read_text())
    notes, text = set(), ""
    for e in log:
        t = e.get("tool")
        if t == "write_file":
            text = e.get("content") or text
        shown = e.get("shown") or ""
        if t in ("verify", "run_tests"):
            if any(h in shown for h in HEADER) or any(_RUNNER_FRAME.match(l)
                                                       for l in shown.splitlines()):
                notes.add("header")
        if t in ("verify", "coverage") and ("never run under this test" in shown
                                            or "never ran under your test" in shown):
            if V.starts_process(text):
                notes.add("spawn")
        if t == "verify" and shown.startswith("NOT fail-to-pass, and backwards"):
            b, a = e.get("before") or {}, e.get("after") or {}
            inv = {n for n, v in b.items() if v == "PASSED"} & {n for n, v in a.items()
                                                               if v in ("FAILED", "ERROR")}
            if any(v in ("FAILED", "ERROR") and n not in inv for n, v in a.items()):
                notes.add("backwards")
        if t == "run_tests":
            out = e.get("outcomes") or {}
            file = (e.get("target") or "").split("::")[0]
            if file.endswith(".py") and len(V.own_outcomes(out, [file])) != len(out):
                notes.add("pytester")
            # 252dd3aa..: a directory target was filtered against itself -> real ids dropped
            if (not file.endswith(".py") and out
                    and len(V.own_outcomes(out, [file])) != len(out)
                    and "no tests ran" in shown.splitlines()[2:3] + [""] * 0
                    or (not file.endswith(".py") and out
                        and all(k.split("::")[-1] + ":" not in shown for k in list(out)[:3]))):
                notes.add("dir-filter")
        # pytest's skip summary read as a test id "[1]" (fixed 2026-10-06)
        if t in ("verify", "run_tests"):
            ids = list((e.get("outcomes") or {})) + list(e.get("before") or {}) + list(e.get("after") or {})
            if any(k.startswith("[") for k in ids):
                notes.add("phantom-id")
    return sorted(notes)


for folder in sys.argv[1:]:
    hits = {}
    for d in sorted(Path(folder).iterdir()):
        if (d / "tool_log.json").is_file():
            n = scan(d)
            if n:
                hits[d.name] = n
    print(f"== {folder}: {len(hits)} affected")
    for k, v in hits.items():
        print(f"   {k}: {', '.join(v)}")
