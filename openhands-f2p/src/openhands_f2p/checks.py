"""What the agent actually did, checked rather than assumed.

Three read-only inspections that run after the agent has stopped: what it tried to reach
on the network, what it wrote outside its test file, whether it ran out of output budget
rather than out of things to say, and what it cost.

Kept apart from the orchestration because none of it decides anything -- every function
here reads a directory or a log and returns a dictionary.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from openhands_f2p import swebench_env as E



# Commands that could actually fetch something, and nothing else. The trailing
# `|https?://` this used to carry matched any URL anywhere in a command -- so an agent
# pasting the issue's own reproduction (`requests.get('http://.example.com')`) into a
# heredoc was flagged as attempting network access. Three separate runs were reported
# as suspicious for quoting the bug they were asked to reproduce. An audit that fires on
# the subject matter trains you to ignore it.
# Only in *command position* -- start of the command, or straight after a shell
# separator. The previous version allowed a match after any whitespace, and `host` and
# `dig` are ordinary English words: an agent printing `getattr(p, 'host', None)` inside a
# heredoc was flagged as attempting DNS. That is the fourth false positive this check has
# produced, each one on the repository's own subject matter, and a check that cries wolf
# four times is a check nobody reads.
NETWORK = re.compile(
    r"(?:^|[;&|`(]\s*|\n\s*|&&\s*|\|\|\s*)"
    r"(curl|wget|nc|ncat|telnet|ssh|scp|rsync|ping|host|dig|"
    r"pip\s+download|pip\s+install|"
    r"git\s+(?:clone|fetch|pull|remote|ls-remote))\b", re.I)


def audit(box: E.Sandbox, tool_log: list, test_file: str) -> dict:
    """What the agent actually did, checked rather than assumed.

    Network attempts are read off the tool log rather than the whole transcript: an
    earlier version scanned every event and flagged the test file the agent wrote,
    because in a repo about HTTP the string `requests.get("http` appears innocently.
    """
    tried_network = [e["command"] for e in tool_log
                     if e["tool"] == "run" and NETWORK.search(e.get("command", ""))]
    wrote_elsewhere = [e["path"] for e in tool_log
                       if e["tool"] == "write_file" and e.get("path") != test_file]
    dirty = box.exec("git status --porcelain 2>/dev/null || echo NO_GIT").output.strip()
    return {"network_attempts": tried_network,
            "files_written_outside_test": wrote_elsewhere,
            "isolation": box.audit_isolation(),
            "vcs": "absent" if "NO_GIT" in dirty else dirty[:300]}


def budget_exhausted(out_dir: Path) -> dict | None:
    """Did the last call end because the output budget ran out, not because the model
    had nothing to say?

    Worth separating. A reasoning model can spend its entire output allowance thinking
    and emit no tool call at all, which looks exactly like a model that cannot call
    tools -- and that misdiagnosis cost time once already, on a model that genuinely
    could not. The distinction is in the response: `finish_reason: length` with
    reasoning_tokens equal to the whole budget means raise the cap, not change the model.
    """
    files = sorted((out_dir / "completions").glob("*.json"))
    if not files:
        return None
    try:
        last = json.loads(files[-1].read_text())
    except (json.JSONDecodeError, OSError):
        return None
    choice = ((last.get("response") or {}).get("choices") or [{}])[0]
    if choice.get("finish_reason") != "length":
        return None
    u = last.get("usage_summary") or {}
    return {"completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": u.get("reasoning_tokens")}


def token_usage(out_dir: Path) -> dict:
    """Totals across every LLM call of this run, from the completion logs.

    Only meaningful because `completions/` is cleared before the run: litellm appends a
    file per call and never prunes it, so a second run on the same PR would otherwise be
    summed together with the first.
    """
    files = sorted((out_dir / "completions").glob("*.json"))
    total = {"llm_calls": len(files), "prompt_tokens": 0, "cache_read_tokens": 0,
             "completion_tokens": 0, "reasoning_tokens": 0, "cost_usd": 0.0,
             "llm_latency_sec": 0.0}
    for f in files:
        try:
            j = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        u = j.get("usage_summary") or {}
        for key in ("prompt_tokens", "cache_read_tokens", "completion_tokens",
                    "reasoning_tokens"):
            total[key] += u.get(key, 0) or 0
        total["cost_usd"] += j.get("cost") or 0.0
        total["llm_latency_sec"] += j.get("latency_sec") or 0.0
    total["cost_usd"] = round(total["cost_usd"], 6)
    total["llm_latency_sec"] = round(total["llm_latency_sec"], 1)
    total["total_tokens"] = total["prompt_tokens"] + total["completion_tokens"]
    return total
