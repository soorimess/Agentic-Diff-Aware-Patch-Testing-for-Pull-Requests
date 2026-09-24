"""Adaptations that a configuration value cannot express.

`models.json` covers everything a model needs that is a *value* -- API mode, token
ceiling, timeout. This module holds the one kind of difference that is not: the shape of
the reply.

There are two. Through the LiteLLM gateway, gpt-5.5 answers a tool-calling
request with **two** choices -- a short text preamble with `finish_reason: stop` in
`choices[0]`, and the actual tool call with `finish_reason: tool_calls` in `choices[1]`:

    choice[0] finish=stop        "I'll inspect existing Django tests first"   tool_calls=0
    choice[1] finish=tool_calls  None                                         tool_calls=1

The SDK reads `choices[0]` in `_build_completion_result`, finds no tool calls, and treats
the reply as final. The run records zero actions in twelve seconds and reads exactly like
a model that cannot call tools -- which gpt-5.5 plainly can, since the call is sitting in
the next choice. That cost one run to diagnose and would have cost more to anyone who did
not go looking in `completions/`.

The fix is to pick the choice that carries the tool call, and it has to live here because
the choice is made inside the SDK, below anything `configure_llm` can set. A profile says
*that* a model needs it (`picks_first_choice: false`); this says *what* to do.

Deliberately narrow: with one choice, or when none carries a tool call, the parent's
behaviour is untouched, so a model that does not need this cannot be harmed by it.

The second is qwen3-coder, which sometimes answers a tool-calling request by writing
Qwen's own tool syntax into `content` and sending no `tool_calls` at all:

    finish_reason: stop
    content: "I'll start by exploring the codebase.\n\n<function=run>\n<parameter=command>
              \nfind /testbed -name '*.py'\n</parameter>\n</function>\n</tool_call>"

The model did everything right except the serialisation; the provider's adapter did not
convert it. OpenHands sees a reply with no tool call, reads it as the agent finishing,
and the run ends. `sympy-21612` ended that way at action zero, and `pylint-7277` hit it
once in twenty-nine calls and survived only because it happened mid-run. It is not the
provider: Novita produced it constantly, Alibaba produces it always, and SiliconFlow --
which is otherwise correct -- still does it occasionally.

So the reply is repaired here, where the other reply-shape difference already is.
Parsing the XML the model wrote is strictly better than the alternatives: emulated tool
calling would change the protocol for every call to work around a fault in a few, and
asking the gateway's owner to change providers cannot fix a model that emits this on the
provider we want.

Deliberately narrow, the same way: a reply that already carries a tool call is untouched,
and content with no `<function=` in it is untouched. What the salvage cannot do is invent
an argument the model never wrote -- a truncated block yields a call the tool will reject
with its own error, which is the same feedback any malformed call gets.
"""
from __future__ import annotations

import json
import re

from openhands.sdk import LLM

from openhands_f2p import flow


def _tool_call_choice(resp) -> int | None:
    """Index of the first choice carrying a tool call, or None."""
    try:
        choices = resp["choices"]
    except Exception:
        return None
    if not choices or len(choices) < 2:
        return None                    # nothing to choose between
    for i, choice in enumerate(choices):
        message = choice.get("message") if hasattr(choice, "get") else None
        if message is None:
            message = getattr(choice, "message", None)
        calls = (message.get("tool_calls") if hasattr(message, "get")
                 else getattr(message, "tool_calls", None))
        if calls:
            return i
    return None


# `<function=NAME> <parameter=KEY> value </parameter> ... </function>`, Qwen's own tool
# syntax. Non-greedy throughout, and the closing `</function>` is optional because the
# emitter sometimes ends the block with a stray `</tool_call>` instead -- a reply that is
# one tag short of valid is still a reply that says exactly which tool to call with what.
_CALL = re.compile(r"<function=([A-Za-z0-9_.-]+)\s*>(.*?)(?:</function>|</tool_call>|\Z)",
                   re.DOTALL)
_PARAM = re.compile(r"<parameter=([A-Za-z0-9_.-]+)\s*>(.*?)</parameter>", re.DOTALL)


def _trim(value: str) -> str:
    """Drop the one newline the format puts after the tag, and the one before the close.

    Only newlines, and only one at each end. These values carry file contents and shell
    scripts, where interior whitespace is the payload and a `.strip()` would eat the
    indentation of a first line as readily as the delimiter.
    """
    return re.sub(r"\n\Z", "", re.sub(r"\A\n", "", value))


def xml_tool_calls(content: str) -> list[dict]:
    """Tool calls written into the message body, as the API would have delivered them."""
    out = []
    for i, (name, body) in enumerate(_CALL.findall(content or "")):
        args = {key: _trim(val) for key, val in _PARAM.findall(body)}
        out.append({"id": f"salvaged_{i}", "type": "function",
                    "function": {"name": name, "arguments": json.dumps(args)}})
    return out


def strip_xml_tool_calls(content: str) -> str:
    """The prose around the call, which is the part still worth keeping as text."""
    return _CALL.sub("", content or "").replace("</tool_call>", "").strip()


class _PickToolCallChoice:
    """Mixin: the gateway may put the tool call somewhere other than `choices[0]`."""

    def _build_completion_result(self, resp):
        i = _tool_call_choice(resp)
        if i:                          # 0 is already right; None means leave it alone
            choices = list(resp["choices"])
            resp.choices = [choices[i]] + choices[:i] + choices[i + 1:]
        return super()._build_completion_result(resp)


class _SalvageXmlToolCalls:
    """Mixin: the model may write its tool call into `content` instead of `tool_calls`."""

    def _build_completion_result(self, resp):
        from litellm.types.utils import ChatCompletionMessageToolCall, Function
        try:
            message = resp["choices"][0]["message"]
        except Exception:
            return super()._build_completion_result(resp)
        existing = (message.get("tool_calls") if hasattr(message, "get")
                    else getattr(message, "tool_calls", None))
        content = (message.get("content") if hasattr(message, "get")
                   else getattr(message, "content", None)) or ""
        if existing or "<function=" not in content:
            return super()._build_completion_result(resp)
        found = xml_tool_calls(content)
        if not found:
            return super()._build_completion_result(resp)
        message.tool_calls = [
            ChatCompletionMessageToolCall(
                id=c["id"], type="function",
                function=Function(name=c["function"]["name"],
                                  arguments=c["function"]["arguments"]))
            for c in found]
        message.content = strip_xml_tool_calls(content) or None
        # Without this the SDK still sees a reply that "stopped", whatever is attached.
        try:
            resp["choices"][0].finish_reason = "tool_calls"
        except Exception:
            pass
        flow.record(flow.AGENT, "salvaged tool call",
                    ", ".join(c["function"]["name"] for c in found))
        return super()._build_completion_result(resp)


class MultiChoiceLLM(_PickToolCallChoice, LLM):
    """An LLM whose gateway may put the tool call somewhere other than `choices[0]`."""


_ADAPTED: dict[tuple, type[LLM]] = {}


def llm_class(picks_first_choice: bool = True,
              salvages_xml_tool_calls: bool = False) -> type[LLM]:
    """The class to build, given what the model's profile says about its replies.

    Composed rather than enumerated: the two adaptations are independent, a model could
    need both, and each mixin delegates through `super()` so the order of application is
    whatever the MRO says rather than something this function has to get right.
    """
    mixins = tuple(m for m, needed in ((_PickToolCallChoice, not picks_first_choice),
                                       (_SalvageXmlToolCalls, salvages_xml_tool_calls))
                   if needed)
    if not mixins:
        return LLM
    key = tuple(m.__name__ for m in mixins)
    if key not in _ADAPTED:
        _ADAPTED[key] = type("AdaptedLLM", mixins + (LLM,), {})
    return _ADAPTED[key]
