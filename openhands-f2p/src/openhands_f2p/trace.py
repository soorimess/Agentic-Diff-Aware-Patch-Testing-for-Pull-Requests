"""Read back everything a run left behind, in the order it happened.

Four sources, in increasing rawness:

  tool_log.json     one entry per tool call -- the command, its exit code, its output.
                    Written by our executors, so it is what actually reached the
                    container rather than what the model asked for.
  trajectory.json   the same events in OpenHands' format, for the visualizer at
                    trajectory-visualizer.vercel.app
  completions/      raw prompt and response bytes per LLM call. The only place the
                    exact request can be read back.

    uv run python -m openhands_f2p.trace 5             # summary of the flow
    uv run python -m openhands_f2p.trace 5 --full      # untruncated observations
    uv run python -m openhands_f2p.trace 5 --tools     # just the tool calls
    uv run python -m openhands_f2p.trace 5 --llm 3     # the raw 3rd LLM exchange
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openhands_f2p.prs import pick

OUT = Path(__file__).resolve().parents[3] / "out"


def _load(d: Path, name: str):
    f = d / name
    return json.loads(f.read_text()) if f.exists() else None


def _clip(text: str, n: int, full: bool) -> str:
    text = (text or "").strip()
    if full or len(text) <= n:
        return text
    return text[:n] + f"  ... [+{len(text) - n} chars]"


def summarise(instance_id: str, full: bool = False, tools_only: bool = False,
              llm_index: int | None = None) -> int:
    d = OUT / instance_id
    if not d.exists():
        print(f"no run recorded at out/{instance_id}/ -- run the agent on it first")
        return 1

    result = _load(d, "result.json")
    tool_log = _load(d, "tool_log.json") or []
    traj = _load(d, "trajectory.json") or []

    print("=" * 78)
    print(f"{instance_id}")
    if result:
        print(f"  verdict   {result['f2p']} -- {result['why']}")
        print(f"  model     {result.get('model')}   status {result.get('agent_status')}")
        print(f"  actions   {result.get('actions')}")
        a = result.get("audit") or {}
        iso = a.get("isolation", {})
        print(f"  isolation dns={iso.get('dns_resolves')} git={iso.get('git_present')} "
              f"network_attempts={a.get('network_attempts')} "
              f"stray_writes={a.get('files_written_outside_test')}")

    # raw LLM traffic
    comps = sorted((d / "completions").glob("*.json")) if (d / "completions").exists() else []
    print(f"  sources   tool_log={len(tool_log)} calls, trajectory={len(traj)} events, "
          f"completions={len(comps)} files")

    if llm_index is not None:
        if not comps:
            print("\nno completion logs -- rerun the agent now that logging is on")
            return 1
        i = max(0, min(llm_index - 1, len(comps) - 1))
        print(f"\n--- raw LLM exchange {i + 1}/{len(comps)}: {comps[i].name} ---")
        print(_clip(comps[i].read_text(), 6000, full))
        return 0

    print(f"\n--- {len(tool_log)} tool calls, in order " + "-" * 40)
    for i, e in enumerate(tool_log, 1):
        if e["tool"] == "run":
            head = f"$ {e['command']}"
            body = f"exit {e['returncode']}\n{_clip(e.get('output', ''), 400, full)}"
        elif e["tool"] == "write_file":
            head = f"write {e['path']} ({e.get('lines', '?')} lines)"
            body = _clip(e.get("content", ""), 400, full)
        else:
            head = f"run_tests {e.get('target')}"
            body = (f"exit {e.get('returncode')}  outcomes={e.get('outcomes')}\n"
                    + _clip(e.get("output", ""), 400, full))
        print(f"\n[{i:2d}] {head}")
        for line in body.splitlines():
            print(f"     {line}")

    if tools_only:
        return 0

    test = next((p for p in d.glob("test_f2p_*.py")), None)
    if test:
        print(f"\n--- the test it wrote: {test.name} " + "-" * 30)
        print(_clip(test.read_text(), 2000, full))

    for label, name in (("before the fix", "before_fix.log"),
                        ("after the fix", "after_fix.log")):
        log = d / name
        if log.exists() and log.read_text().strip():
            print(f"\n--- verification, {label} " + "-" * 38)
            print(_clip(log.read_text(), 1200, full))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("which", nargs="?", default="all", help="1..5, an id, or 'all'")
    p.add_argument("--full", action="store_true", help="do not truncate")
    p.add_argument("--tools", action="store_true", help="tool calls only")
    p.add_argument("--llm", type=int, metavar="N", help="print the Nth raw LLM exchange")
    args = p.parse_args()
    rc = 0
    for pr in pick(args.which):
        rc |= summarise(pr["id"], args.full, args.tools, args.llm)
    return rc


if __name__ == "__main__":
    sys.exit(main())
