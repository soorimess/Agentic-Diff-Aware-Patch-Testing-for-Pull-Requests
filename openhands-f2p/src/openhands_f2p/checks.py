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


def _norm(path: str | None) -> str:
    """A repository-relative path: `/testbed/a/b.py` and `./a/b.py` are `a/b.py`."""
    p = (path or "").strip()
    if p.startswith("/testbed/"):
        p = p[len("/testbed/"):]
    while p.startswith("./"):
        p = p[2:]
    return p


def audit(box: E.Sandbox, tool_log: list, test_file: str) -> dict:
    """What the agent actually did, checked rather than assumed.

    Network attempts are read off the tool log rather than the whole transcript: an
    earlier version scanned every event and flagged the test file the agent wrote,
    because in a repo about HTTP the string `requests.get("http` appears innocently.
    """
    tried_network = [e["command"] for e in tool_log
                     if e["tool"] == "run" and NETWORK.search(e.get("command", ""))]
    # Compared as paths, not strings. The test file written as `/testbed/tests/x.py` or
    # `./tests/x.py` is the test file, and the raw comparison listed it as a write
    # "outside the test" in most of the 296 runs across the ten arms that reported one --
    # which made the field useless as a guard statistic. `testbed/tests/x.py` without the
    # leading slash is *not* normalised away: from /testbed it really does land in a
    # stray `testbed/` directory, and that is worth seeing.
    target = _norm(test_file)
    wrote_elsewhere = sorted({_norm(e["path"]) for e in tool_log
                              if e["tool"] == "write_file" and _norm(e.get("path")) != target})
    # The test itself, written first under another directory and then moved to where it
    # is scored: same name, no longer on disk. It was listed as a stray write.
    name = target.rsplit("/", 1)[-1]
    moved_from = [p for p in wrote_elsewhere
                  if p.rsplit("/", 1)[-1] == name and not box.exists(p)]
    wrote_elsewhere = [p for p in wrote_elsewhere if p not in moved_from]
    # Against the snapshot taken before the agent started, not against the checkout's
    # own git -- that was deleted by `strip_git`, which made the previous version of this
    # line structurally dead: it asked `git status`, always got "not a repository", and
    # always reported a clean tree however much the agent had changed. It could not have
    # caught anything.
    #
    # This also covers what the tool log cannot. `files_written_outside_test` sees
    # `write_file` calls; an agent editing source with `sed -i` or a shell redirect is
    # invisible to it. The tree is not.
    status = [(code, p) for code, p in box.tree_status() if _norm(p) != target]
    touched = [p for _, p in status]
    # Added against modified, because only one of them can void the measurement. A file
    # that did not exist at base is present in the before run and the after run alike, so
    # it cannot manufacture a flip; a file that did exist and now differs can, and if it
    # is library source it makes the before run a fact about something other than the
    # pull request.
    added = sorted(p for code, p in status if code in ("??", "A"))
    altered = sorted(p for code, p in status if code not in ("??", "A"))
    # Of the writes outside the test, which were new files the agent made for itself --
    # a reproduction script, a debug print -- and which touched something that was
    # already in the checkout. Only the second can put the measurement in doubt; the
    # first is how an agent thinks, and counting them together hid the one in the other.
    #
    # Asked of the base snapshot, not inferred from what is added now. Inferring it
    # filed `/tmp/fix.patch` -- outside the checkout, never in the snapshot -- as an edit
    # to a pre-existing file, and would have done the same to a scratch file the agent
    # created and then deleted.
    existed = box.tracked(wrote_elsewhere)
    return {"network_attempts": tried_network,
            "files_written_outside_test": wrote_elsewhere,
            "test_moved_from": moved_from,
            "scratch_files": [p for p in wrote_elsewhere if p not in existed],
            "preexisting_written": [p for p in wrote_elsewhere if p in existed],
            "isolation": box.audit_isolation(),
            "tree_changed": touched,
            "tree_added": added,
            "tree_altered": altered,
            "vcs": "clean apart from the test" if not touched
                   else (f"{len(added)} file(s) added"
                         + (f", {len(altered)} pre-existing file(s) changed: "
                            f"{', '.join(altered[:5])}" if altered else "")
                        )[:300]}


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
