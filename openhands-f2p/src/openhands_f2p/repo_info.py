"""repo_info as a sub-agent: a second model reads the repository and answers.

Why a sub-agent rather than a string check
------------------------------------------
The first version computed a structural summary and then scanned it for lines of the
developer's test. That is a guard in the weakest sense: it can only catch an exact
substring, so a paraphrase, a renamed variable or a reformatted assertion walks straight
through. And the thing being guarded was a template we wrote, which made the check mostly
theatre -- it was verifying our own output against a leak it could not have contained.

A sub-agent changes the shape of the guarantee. It gets the repository and one narrow
question; the main agent gets only the sub-agent's answer, which is a short structured
document, never repository text. Two independent limits then apply at once:

  * The sub-agent is not given the issue, the diff, or the test patch. It cannot leak
    what it was never shown -- and unlike a regex, that holds for paraphrase too.
  * Its answer is parsed into a fixed set of fields. Anything it says outside them is
    discarded rather than trusted, so a sub-agent that decided to be helpful about the
    bug has no field to be helpful in.

What it is for
--------------
How to run tests *in this project at this version*. Conventions move between releases --
django 2 and django 5 do not lay tests out the same way, and pytest's own repository uses
`testing/` where everyone else uses `tests/`. Asking the checkout beats hardcoding a
table that is right for the versions we happened to look at.
"""
from __future__ import annotations

import json
import re
from typing import Any

from openhands_f2p import llm_config
from openhands_f2p.swebench_env import Sandbox, runner_for

# The only fields that come back. A sub-agent answer is filtered to these, so anything
# it volunteers about the bug has nowhere to land.
FIELDS = ("test_layout", "naming", "structure", "running", "fixtures", "gotchas")

SYSTEM = """You are documenting a Python project's testing conventions for another
engineer who has to add one new test file to it.

You will be given the output of some commands run in the repository. Answer only about
conventions -- where tests live, how files and functions are named, whether tests are
classes or functions, what fixtures or base classes are conventional, how the suite is
invoked, and anything unusual that would trip someone up.

Say nothing about bugs, defects, issues, or what any test ought to assert. You have not
been told what the other engineer is testing and must not speculate.

Reply with JSON only, using exactly these keys, each a short string:
  test_layout, naming, structure, running, fixtures, gotchas
"""


def _gather(box: Sandbox, repo: str, gen_path: str, version: str) -> str:
    """Facts from the checkout for the sub-agent to read. Structure, not source."""
    def sh(cmd: str, limit: int = 1800) -> str:
        return box.exec(cmd, timeout=180).output[:limit]

    parent = gen_path.rsplit("/", 1)[0] if "/" in gen_path else "."
    find_dirs = "find . -type d -name tests -o -type d -name test 2>/dev/null | head -20"
    find_files = ("find . -name 'test_*.py' -o -name '*_test.py' 2>/dev/null | head -25")
    find_conf = "find . -name conftest.py 2>/dev/null | head -10"
    config = ("for f in setup.cfg tox.ini pytest.ini pyproject.toml; do "
              "[ -f $f ] && echo \"--- $f\" && "
              "grep -A6 -iE 'testpaths|python_files|\\[pytest\\]|tool.pytest' $f; done")
    example = sh("find . -name 'test_*.py' 2>/dev/null | head -1").strip()
    example = example.splitlines()[0] if example else ""

    parts = [
        "## project\n" + f"{repo}, version {version}",
        "## test directories\n" + sh(find_dirs),
        "## a sample of test filenames\n" + sh(find_files),
        f"## files already in {parent}\n" + sh(f"ls -1 {parent} 2>/dev/null | head -25"),
        "## conftest.py locations\n" + (sh(find_conf) or "(none)"),
        "## pytest/tox configuration\n" + (sh(config) or "(none found)"),
        "## how the suite is invoked here\n" + runner_for(repo)["cmd"],
    ]
    if example:
        parts.append(f"## the first 60 lines of {example}, for style\n"
                     + sh(f"sed -n '1,60p' {example} 2>/dev/null", 2500))
    return "\n\n".join(parts)


def _parse(text: str) -> dict[str, str]:
    """Take only the known fields, as strings. Everything else is dropped."""
    match = re.search(r"\{.*\}", text or "", re.S)
    if not match:
        return {}
    try:
        raw = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw, dict):
        return {}
    return {k: str(raw[k])[:600] for k in FIELDS if raw.get(k)}


def describe(box: Sandbox, repo: str, gen_path: str, version: str) -> dict[str, Any]:
    """Ask a sub-agent how testing works in this project, at this version."""
    from openhands.sdk.llm import Message, TextContent

    facts = _gather(box, repo, gen_path, version)
    llm, model, _ = llm_config.configure_llm(
        usage_id="f2p-repo-info",
        model=__import__("os").getenv("LLM_REPO_INFO_MODEL") or None,
        timeout=int(__import__("os").getenv("LLM_REPO_INFO_TIMEOUT") or 180))
    reply = llm.completion([
        Message(role="system", content=[TextContent(text=SYSTEM)]),
        Message(role="user", content=[TextContent(text=facts)]),
    ])
    content = reply.message.content
    text = content if isinstance(content, str) else "".join(
        getattr(c, "text", "") for c in (content or []))
    fields = _parse(text)
    return {"model": model, "fields": fields,
            "runner_command": runner_for(repo)["cmd"],
            "write_your_test_at": gen_path,
            "facts_chars": len(facts),
            "raw_reply_chars": len(text)}


def render(info: dict[str, Any]) -> str:
    labels = {"test_layout": "Where tests live", "naming": "Naming",
              "structure": "Test structure", "running": "Running the suite",
              "fixtures": "Fixtures and base classes", "gotchas": "Things that trip people up"}
    lines = [f"Runner for this project:  {info['runner_command']}",
             f"Write your test at:       {info['write_your_test_at']}", ""]
    fields = info.get("fields") or {}
    if not fields:
        lines.append("(the conventions sub-agent returned nothing usable; fall back to "
                     "reading an existing test with `run`)")
        return "\n".join(lines)
    for key in FIELDS:
        if fields.get(key):
            lines += [f"{labels[key]}:", f"  {fields[key]}", ""]
    return "\n".join(lines).rstrip()
