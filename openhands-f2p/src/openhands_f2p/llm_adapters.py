"""Adaptations that a configuration value cannot express.

`models.json` covers everything a model needs that is a *value* -- API mode, token
ceiling, timeout. This module holds the one kind of difference that is not: the shape of
the reply.

There is exactly one so far. Through the LiteLLM gateway, gpt-5.5 answers a tool-calling
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
"""
from __future__ import annotations

from openhands.sdk import LLM


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


class MultiChoiceLLM(LLM):
    """An LLM whose gateway may put the tool call somewhere other than `choices[0]`."""

    def _build_completion_result(self, resp):
        i = _tool_call_choice(resp)
        if i:                          # 0 is already right; None means leave it alone
            choices = list(resp["choices"])
            resp.choices = [choices[i]] + choices[:i] + choices[i + 1:]
        return super()._build_completion_result(resp)


def llm_class(picks_first_choice: bool) -> type[LLM]:
    """The class to build, given what the model's profile says about its replies."""
    return LLM if picks_first_choice else MultiChoiceLLM
