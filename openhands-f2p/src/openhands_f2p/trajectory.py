"""Export a run in the OpenHands trajectory format, for the trajectory visualizer.

    https://trajectory-visualizer.vercel.app/     (upload out/<id>/trajectory.json)

The visualizer accepts three shapes; we emit the first, which is the canonical OpenHands
one and the one it detects without any wrapper:

    a bare top-level array, where the first element has `action` + `source`
    {"entries": [...]}      its own sample format
    {"history": [...]}      its internal format

Each event is discriminated by two fields together -- `source` and `action`/`observation`
-- and the renderer picks a component from that pair. So a shell command has to be
`{"source": "agent", "action": "run"}` and nothing else will draw as a terminal block.
The mapping we use:

    our `run` tool         -> action/observation "run"     (terminal component)
    our `write_file` tool  -> action/observation "edit"    (diff component)
    our `run_tests` tool   -> action/observation "run"     with the translated command,
                              because what actually executed *was* a shell command and
                              showing the agent's argument instead would hide which
                              runner was chosen
    the task we send       -> action "message", source "user"
    the agent's summary    -> action "finish"
    harness milestones     -> source "environment" with a `key`, which has its own
                              component; these are ours, not the agent's, and labelling
                              them as agent actions would misattribute the work

An observation carries `cause`, the id of the action it answers. The visualizer uses it
to pair them, so ids have to be assigned in one pass and never reused.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from openhands_f2p import swebench_env as E
from openhands_f2p.layout import OUT


def _ts(base: datetime, offset: float) -> str:
    # Fixed precision: `isoformat()` drops the fraction at whole seconds, and "…39Z"
    # sorts after "…39.100000Z" as text.
    return (base + timedelta(seconds=offset)).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# The first line of each prompt piece, mapped to the heading it should render under.
# Matching on content rather than re-reading prompts/ keeps this working on a trajectory
# rebuilt from an out/ directory whose prompt files have since changed.
_PIECE_HEADINGS = (
    ("You are in a checkout of", "Situation"),
    ("A pull request changes how this library behaves", "What to produce"),
    ("The bug report:", "The bug report"),
    ("## What this pull request changes", None),
    ("You have these tools:", "Tools"),
    ("Because the change is given to you", "Tools that read the change"),
    ("- `coverage` \u2014", "The coverage tool"),
    ("Create only", "Rules"),
    ("Run your test with `run_tests`", "Checking your work"),
    ("Two tools can tell you whether you understood", "Closing the loop"),
    ("This is django", "Runner notes"),
    ("This is sympy", "Runner notes"),
    ("This is a pytest project", "Runner notes"),
)


def _as_markdown(task: str) -> str:
    """Put a heading in front of each prompt piece so the prompt is skimmable.

    Pieces already carrying their own `##` heading are left alone; the rest get one, at
    a level below the title so the two do not compete.
    """
    if not task.strip():
        return task
    out = ["# The task sent to the agent", ""]
    for block in task.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            out += [block, ""]
            continue
        heading = next((h for prefix, h in _PIECE_HEADINGS
                        if h and stripped.startswith(prefix)), None)
        if heading:
            out += [f"## {heading}", ""]
        out += [block, ""]
    return "\n".join(out).rstrip() + "\n"


# Tool-call names as the model sends them -> the name in the tool log. Only the real
# tools: a call to an invented name (`sandbox_run_tests`, `sandbox_finish`) never ran.
# Runs before the tools were named after the prompt used the SDK's class-derived names.
# The flow row each tool call leaves, one per call (`on_event` in `agent.run_agent`).
_TOOL_EVENTS = {"RunAction", "WriteAction", "TestAction", "VerifyAction", "CoverageAction",
                "MutationAction"}

_CALL_NAMES = {"sandbox_run": "run", "sandbox_write": "write_file",
               "sandbox_test": "run_tests", "sandbox_verify": "verify",
               "sandbox_coverage": "coverage", "sandbox_mutation": "mutation",
               **{n: n for n in ("run", "write_file", "run_tests", "verify", "coverage",
                                 "mutation")}}


def _describe(tool: str, entry: dict) -> str:
    """Readable body for the tools whose result is structured rather than shell output."""
    if tool == "repo_info":      # historical: runs before the sub-agent was removed
        info = entry.get("info") or {}
        if entry.get("withheld"):
            return "withheld: the output would have echoed the developer's test."
        return "\n".join(
            [f"runner:            {info.get('runner_command', '')}",
             f"write test at:     {info.get('write_your_test_at', '')}",
             f"test directories:  {', '.join(info.get('test_directories') or [])}",
             f"test files:        {info.get('test_file_count')}",
             f"conftest:          {', '.join(info.get('conftest_files') or []) or 'none'}",
             f"style:             {info.get('style')}"])
    if tool == "verify":
        if entry.get("error"):
            return f"could not run: {entry['error']}"
        flipped = entry.get("flipped") or []
        head = ("fail-to-pass: " + ", ".join(n.split("::")[-1] for n in flipped)
                if flipped else "NOT fail-to-pass")
        return (f"{head}\n\nbefore the change: {entry.get('before')}"
                f"\nafter the change:  {entry.get('after')}")
    if tool == "mutation":
        if entry.get("error") or not entry.get("total"):
            return f"no mutants run: {entry.get('error') or entry.get('why', '')}"
        lines = [f"killed {entry.get('killed')} of {entry.get('total')} mutants"]
        lines += [f"  survived: {m}" for m in entry.get("survived") or []]
        return "\n".join(lines)
    res = entry.get("result") or {}
    if not res.get("measured"):
        return f"not measured: {res.get('reason', '')}"
    # Re-rendered, not what the agent saw -- since the coverage tool stopped showing a
    # figure, the model got the missed lines only. Marked so nobody reads the number as
    # something the agent was told.
    lines = [f"[re-rendered from the log; the agent saw only the missed lines] "
             f"{res['percent']}% of changed lines executed "
             f"({res['covered']}/{res['executable_changed_lines']})"]
    for item in res.get("missed_source") or []:
        lines += ["", f"  missed {item['ref']}"]
        lines += [f"      {g}" for g in item["guards"]]
        lines.append(f"    > {item['line']}")
    return "\n".join(lines)


def build(out_dir: Path) -> list[dict[str, Any]]:
    """Turn one run's artifacts into a trajectory the visualizer can read."""
    def load(name, default=None):
        f = out_dir / name
        return json.loads(f.read_text()) if f.exists() else default

    result = load("result.json", {}) or {}
    tool_log = load("tool_log.json", []) or []
    flow_rows = []
    if (out_dir / "flow.jsonl").exists():
        flow_rows = [json.loads(l) for l in (out_dir / "flow.jsonl").read_text().splitlines() if l.strip()]
    task = result.get("task", "")
    # Messages the harness sent after the task -- each refusal of a stop -- keyed by the
    # tool-log position they arrived at. Without these the export showed one user message
    # and an agent that simply carried on, which is how a single-shot refusal went
    # unnoticed through a ten-arm series.
    injected = load("injected_messages.json", []) or []

    # Why the agent called each tool. The model says it in the `content` of the same
    # completion that carried the tool call -- "I'll open numbers.py to inspect
    # Rational.__new__" -- and dropping it left the visualizer showing what happened with
    # no trace of the reasoning that led there. Completion logs are named with a
    # timestamp, so sorting them puts them in call order.
    #
    # Paired per tool, in order: the Nth `sandbox_verify` call is the Nth `verify` entry.
    # Pairing the Nth call of any kind with the Nth log entry, as this did first, drifted
    # after every `think`, `finish` or unparsed call (a tool call with no log entry) and
    # every `guard` revert (a log entry with no tool call), so a thought sat on the wrong
    # action for the rest of the run.
    thoughts: dict[str, list[str]] = {}
    for cf in sorted((out_dir / "completions").glob("*.json")):
        try:
            j = json.loads(cf.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        msg = ((j.get("response") or {}).get("choices") or [{}])[0].get("message") or {}
        if not msg.get("tool_calls"):
            continue
        for call in msg["tool_calls"]:
            tool = _CALL_NAMES.get((call.get("function") or {}).get("name", ""))
            if tool:
                thoughts.setdefault(tool, []).append((msg.get("content") or "").strip())
    repo = (load("pr.json", {}) or {}).get("repo", "")

    # flow.jsonl carries wall-clock offsets; without it everything lands on one second,
    # which makes the timeline useless.
    # Anchored on when the run ended (`ran_at`, written with the result) minus the last
    # flow offset, so each timestamp is the moment it happened. `now()` stamped a rebuilt
    # trajectory after the run's real end -- sympy-24562 "ran to 14:08", recorded 12:28.
    base = datetime.now(timezone.utc)
    ran_at = result.get("ran_at")
    if ran_at and flow_rows:
        try:
            base = (datetime.fromisoformat(ran_at.replace("Z", "+00:00"))
                    - timedelta(seconds=flow_rows[-1].get("t", 0.0)))
        except ValueError:
            pass
    # One flow row per tool call, in call order -- only those. Every agent row was taken
    # before, so `tools registered`, `task sent`, each think, finish and stop check pushed
    # the tool calls after it one row later in time, and the harness's own events (the
    # stop-check probes, the patch applied for a `verify`) could not be placed among them:
    # they were all drawn after the last tool call, a restart's first attempt included.
    offsets = [r["t"] for r in flow_rows
               if r.get("phase") == "agent" and r.get("event") in _TOOL_EVENTS]
    # When each harness message was sent: a refused stop or the restart.
    sent = [r["t"] for r in flow_rows if r.get("phase") == "agent" and (
        r.get("event") == "restart sent"
        or (r.get("event") == "stop check" and str(r.get("detail", "")).startswith("round")))]
    # Placed by time only when both line up with what they time; a run recorded before
    # these rows existed keeps the order it is built in.
    timed = (len(offsets) == sum(1 for e in tool_log if e.get("tool") != "guard")
             and len(sent) == len(injected))
    events: list[dict[str, Any]] = []
    n = 0

    def add(ev: dict[str, Any], offset: float) -> int:
        nonlocal n
        ev["id"] = n
        ev["timestamp"] = _ts(base, offset)
        ev["_t"] = offset
        events.append(ev)
        n += 1
        return ev["id"]

    # --- the task, first ------------------------------------------------------
    #
    # Order matters beyond readability: the uploader decides a file is a trajectory by
    # checking that element [0] has `source` plus `action` or `observation`. An
    # environment event has `source` and `key` and neither of the others, so leading
    # with the container setup makes the whole file unrecognised. This only showed up on
    # the one run that had a flow log to draw setup events from.
    # The prompt is ten pieces joined with blank lines, which the visualizer renders as
    # one undifferentiated wall -- the diff, the rules and the tool list all at body
    # size with nothing to navigate by. Markdown headings give the renderer something to
    # scale, so each piece becomes a section you can skim past. The text is unchanged;
    # only the heading level in front of each piece is added.
    # Stamped just before the first setup event it precedes, not at offset 0: the setup
    # rows carry process offsets, so flask-5014 (base, cap 125) showed 23.6 minutes --
    # its image pull -- between the task and "container up".
    first_setup = next((r["t"] for r in flow_rows
                        if r.get("phase") == "setup" and r.get("event") == "container up"),
                       None)
    add({"source": "user", "action": "message", "message": "task",
         "args": {"content": _as_markdown(task), "images_urls": []}},
        max(first_setup - 0.01, 0.0) if first_setup is not None else 0.0)

    # --- setup, as environment events -----------------------------------------
    for row in flow_rows:
        if row["phase"] != "setup" or row["event"] == "exec":
            continue
        if row["event"] in ("container up", "strip git", "instance", "test path"):
            add({"source": "environment", "key": row["event"],
                 "value": row["detail"], "message": row["detail"]}, row["t"])
        if row["event"] == "test path":
            break

    def say(msg: dict, offset: float) -> None:
        if timed:
            offset = sent[injected.index(msg)]
        add({"source": "user", "action": "message", "message": "harness",
             "args": {"content": msg.get("text", ""), "images_urls": []}}, offset)

    # --- the agent's tool calls ---------------------------------------------
    used: dict[str, int] = {}
    k = 0                                  # tool calls so far; `i` also counts reverts
    prev_offset = None
    for i, entry in enumerate(tool_log):
        offset = offsets[k] if k < len(offsets) else float(k)
        for msg in injected:
            if msg.get("at_tool") == i:
                say(msg, offset)
        tool = entry.get("tool")
        if tool == "guard":
            # The harness undoing an edit to a file that existed at base -- ours, not a
            # call the agent made, so it is not drawn as one.
            # Right after the call that made the edit (the previous one), not inside the
            # next: at the next call's time + 0.05 it sorted between that call and its
            # result (django-13406, base at cap 125: a revert inside a `write_file`, 48 s
            # after the `sed -i` that caused it).
            add({"source": "environment", "key": "guard: reverted",
                 "value": ", ".join(entry.get("reverted") or []),
                 "message": ", ".join(entry.get("reverted") or [])},
                prev_offset + 0.15 if prev_offset is not None else offset - 0.05)
            continue
        k += 1
        prev_offset = offset
        mine = thoughts.get(tool, [])
        why = mine[used.get(tool, 0)] if used.get(tool, 0) < len(mine) else ""
        used[tool] = used.get(tool, 0) + 1

        if tool == "write_file":
            content = entry.get("content", "")
            aid = add({"source": "agent", "action": "edit",
                       "message": f"write {entry.get('path')}",
                       "args": {"path": entry.get("path", ""), "old_content": "",
                                "new_content": content, "thought": why}},
                      offset)
            add({"source": "agent", "observation": "edit", "cause": aid,
                 "message": entry.get("shown") or f"wrote {entry.get('path')}",
                 "content": content,
                 "extras": {"path": entry.get("path", ""),
                            "lines": entry.get("lines")}}, offset + 0.1)
            continue

        # verify and coverage carry no `command` key, so before this they all
        # fell through to the shell branch and rendered as empty terminal boxes -- an
        # action with no command and no output. Each gets the shape that says what it is.
        if tool in ("repo_info", "verify", "coverage", "mutation"):
            label = {"repo_info": "look up this project's test conventions",
                     "verify": f"check fail-to-pass for {entry.get('target', '')}",
                     "coverage": f"list the changed lines "
                                 f"{entry.get('target', '')} never runs",
                     "mutation": f"mutation-test {entry.get('target', '')}"}[tool]
            # What the model was actually handed, when the run recorded it. Older runs
            # did not, and get a re-rendering from the structured result instead.
            body = entry.get("shown") or _describe(tool, entry)
            aid = add({"source": "agent", "action": "run", "message": label,
                       "args": {"command": f"[{tool}] {label}",
                                "is_confirmed": "confirmed", "thought": why}}, offset)
            add({"source": "agent", "observation": "run", "cause": aid,
                 "message": label, "content": body,
                 "extras": {"command": f"[{tool}]", "command_id": aid, "exit_code": 0,
                            "metadata": {"tool": tool}}}, offset + 0.1)
            continue

        # `run` and `run_tests` both end up as shell commands, which is what they are.
        command = entry.get("command") or entry.get("command_used") or ""
        if tool == "run_tests":
            command = entry.get("command") or E.test_command(repo, [entry.get("target", "")])
            thought = why or f"run the repository's own test runner on {entry.get('target')}"
        else:
            thought = why
        aid = add({"source": "agent", "action": "run",
                   "message": command.splitlines()[0][:120] if command else "",
                   "args": {"command": command, "is_confirmed": "confirmed",
                            "thought": thought}}, offset)
        add({"source": "agent", "observation": "run", "cause": aid,
             "message": f"exit {entry.get('returncode')}",
             "content": entry.get("shown") or entry.get("output", ""),
             "extras": {"command": command, "command_id": aid,
                        "exit_code": entry.get("returncode", 0),
                        "metadata": {"tool": tool,
                                     **({"outcomes": entry["outcomes"]}
                                        if entry.get("outcomes") else {})}}},
            offset + 0.1)

    # A refusal the agent answered by stopping again, with no tool call in between,
    # arrives after the last entry in the log. Still shown, in order.
    for msg in injected:
        if msg.get("at_tool", 0) >= len(tool_log):
            say(msg, float(len(tool_log)))

    # --- verification, which is the harness and not the agent ----------------
    last = flow_rows[-1]["t"] if flow_rows else float(len(tool_log))
    for row in flow_rows:
        if row["phase"] not in ("verify", "audit"):
            continue
        add({"source": "environment", "key": f"{row['phase']}: {row['event']}",
             "value": row["detail"], "message": row["detail"]}, row["t"])

    # --- the verdict, as the closing action ----------------------------------
    add({"source": "agent", "action": "finish",
         "message": f"F2P: {result.get('f2p', '?')} -- {result.get('why', '')}",
         "args": {"outputs": {"f2p": result.get("f2p"),
                              "f2p_nodes": result.get("f2p_nodes", []),
                              "actions": result.get("actions"),
                              "model": result.get("model")},
                  "final_thought": result.get("why", ""),
                  "task_completed": "true" if result.get("f2p") == "YES" else "false"}},
        last + 0.2)

    if timed:
        # The task stays first (the uploader keys on it) and the verdict last; everything
        # between goes in the order it happened. Stable, so an observation keeps its place
        # after its action, and ids are renumbered with `cause` following them.
        body = sorted(events[1:-1], key=lambda ev: ev["_t"])
        events = events[:1] + body + events[-1:]
        new_id = {ev["id"]: i for i, ev in enumerate(events)}
        for i, ev in enumerate(events):
            ev["id"] = i
            if "cause" in ev:
                ev["cause"] = new_id[ev["cause"]]
    for ev in events:
        del ev["_t"]
    return events


def write(out_dir: Path) -> Path | None:
    if not (out_dir / "tool_log.json").exists():
        return None
    events = build(out_dir)
    path = out_dir / "trajectory.json"
    path.write_text(json.dumps(events, indent=2))
    return path


def main() -> int:
    import sys

    from openhands_f2p.prs import pick

    root = OUT
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for pr in pick(which):
        p = write(root / pr["id"])
        if p:
            n = len(json.loads(p.read_text()))
            print(f"  {pr['id']:36s} {n:3d} events -> {p.relative_to(root.parent)}")
        else:
            print(f"  {pr['id']:36s} no run recorded yet")
    print("\nupload these at https://trajectory-visualizer.vercel.app/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
