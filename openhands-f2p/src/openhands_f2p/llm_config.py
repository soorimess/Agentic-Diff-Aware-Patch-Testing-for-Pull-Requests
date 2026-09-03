"""One place the model connection is configured, shared by every caller.

Extracted from agent.py when a second caller appeared. Everything here was learned by
hitting it: the proxy has to be an explicit httpx client rather than an environment
variable, litellm keeps a separate client for its async path, `auto` api_mode resolves
gpt-5-mini to an endpoint that hangs, and litellm's own 300s timeout overrides the
client's.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

import httpx
from pydantic import SecretStr


def gateway_refusal() -> str | None:
    """One cheap call to find out whether the gateway will serve us at all.

    Worth a second at startup. A LiteLLM key that has spent its budget answers 429 with
    `budget_exceeded`, which litellm classifies as a rate limit -- so the SDK backs off
    and retries it ten times, and each instance sits for twenty minutes before failing
    with nothing written. Four did. A budget is not a transient condition and no amount
    of waiting clears it, so it is better found before the first container starts.

    Returns a message to die with, or None if the gateway is willing.
    """
    key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    base = os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    if not key or not base:
        return None                     # nothing to check against; let the run report it
    model = (os.getenv("LLM_MODEL") or "gpt-5-mini").split("/")[-1]
    # Three attempts, because one flaky proxy hiccup made the probe return "willing"
    # and the run went on to spend forty minutes pulling an image for a gateway that
    # was never going to answer.
    r = None
    for _ in range(3):
        try:
            with httpx.Client(proxy=os.getenv("LLM_PROXY") or None, timeout=45.0) as c:
                r = c.post(f"{base.rstrip('/')}/chat/completions",
                           headers={"Authorization": f"Bearer {key}"},
                           json={"model": model, "max_completion_tokens": 16,
                                 "messages": [{"role": "user", "content": "ping"}]})
            break
        except httpx.HTTPError:
            time.sleep(2)
    if r is None:
        return None                     # unreachable, not refusing; let the run report it
    if r.status_code != 429:
        return None
    detail = (r.json().get("error") or {}).get("message", r.text)[:200] \
        if r.headers.get("content-type", "").startswith("application/json") else r.text[:200]
    if "budget" not in detail.lower():
        return None                     # an ordinary rate limit; retrying does clear that
    return (f"the model gateway is refusing every request: {detail.strip()}\n"
            f"This is a spent budget on the key in .env, not a transient limit -- "
            f"retrying cannot clear it. Top the key up, or point LLM_BASE_URL and "
            f"LLM_API_KEY at another gateway, then run again. Nothing was started.")


def configure_llm(completions_dir: Path | None = None,
                  usage_id: str = "f2p-agent",
                  model: str | None = None,
                  timeout: int | None = None):
    """Build the LLM without putting the proxy into the environment.

    litellm is given an explicit httpx client instead, so HTTP_PROXY and friends stay
    unset. That keeps the LLM's route to the model and the sandbox's lack of a route
    genuinely separate, rather than one leaking into the other.
    """
    from openhands.sdk import LLM

    key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key:
        raise SystemExit("no LLM_API_KEY (or OPENAI_API_KEY) -- see .env.example")
    proxy = os.getenv("LLM_PROXY")
    if proxy:
        import litellm
        # Both clients: litellm keeps a separate one for the async path, and setting
        # only the sync one leaves half the calls going out without the proxy, which
        # presents as a 300-second timeout rather than an error.
        # Separate connect and read timeouts, and TCP keepalive on the pool.
        #
        # A single `timeout=600` is not enough. Suspending the machine leaves the
        # sockets half-open: the peer is gone but nothing tells this end, so a request
        # issued on a pooled connection can hang past every application timeout. Three
        # runs sat silent for fifty-one minutes after a laptop sleep with their last
        # model call an hour behind them, and had to be killed.
        #
        # A short connect timeout makes a dead peer fail in seconds rather than never,
        # and expiring pooled connections means the next attempt opens a fresh socket
        # instead of reusing a corpse.
        limits = httpx.Limits(max_keepalive_connections=4, keepalive_expiry=30.0)
        clock = httpx.Timeout(connect=20.0, read=600.0, write=60.0, pool=30.0)
        litellm.client_session = httpx.Client(proxy=proxy, timeout=clock, limits=limits)
        litellm.aclient_session = httpx.AsyncClient(proxy=proxy, timeout=clock,
                                                    limits=limits)

    native = os.getenv("LLM_NATIVE_TOOL_CALLING")
    extra = ({} if native is None
             else {"native_tool_calling":
                   native.lower() not in ("0", "false", "no", "off")})
    # An explicit model wins, then the environment. The judge passes one so that the
    # step which decides whether two tests mean the same thing is not done by the same
    # model that wrote one of them -- and it is a single call per instance, so a larger
    # model costs almost nothing here.
    model = model or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-5-mini"
    # 'chat' rather than 'auto'. Auto resolves gpt-5-mini to the Responses API, which
    # is a different litellm entry point -- and against this gateway it hung for the
    # full 300-second timeout. The chat-completions path is the one measured working.
    api_mode = os.getenv("LLM_API_MODE") or "chat"
    # Raw prompt and response per call, on disk. Off by default in the SDK, and it is
    # the only place the *exact* bytes sent to the model can be read back -- our own
    # transcript records the parsed events, which is a summary of them.
    log_kwargs = ({"log_completions": True,
                   "log_completions_folder": str(completions_dir)}
                  if completions_dir else {})
    return LLM(usage_id=usage_id, model=model,
               base_url=os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or None,
               api_key=SecretStr(key), api_mode=api_mode,
               max_output_tokens=int(os.getenv("LLM_MAX_OUTPUT_TOKENS") or 16000),
               # litellm's own timeout wins over the httpx client's, and it defaults to
               # 300s -- which a request carrying several test logs will exceed.
               # The agent needs a long timeout: its requests carry test logs and it
               # retries inside one conversation. A single judgement call does not, and
               # leaving it at 900s meant one stuck call froze a five-instance run for
               # fifteen minutes with nothing on screen to say why.
               # 600 rather than 900: the agent's requests carry test logs and need
               # room, but a wedged call should surface inside ten minutes, not fifteen.
               timeout=timeout or int(os.getenv("LLM_TIMEOUT") or 600),
               # The SDK's defaults -- five attempts, backing off to a minute -- give up
               # after roughly three minutes of refusals. That is not enough against a
               # shared gateway: three agents running at once rate-limited four
               # instances into BROKEN, each having written nothing, and each of them
               # succeeded on its own later. Waiting is cheap here and a lost run is
               # not, so the ceiling is raised rather than the concurrency lowered.
               num_retries=int(os.getenv("LLM_NUM_RETRIES") or 10),
               retry_max_wait=int(os.getenv("LLM_RETRY_MAX_WAIT") or 120),
               **log_kwargs, **extra), model, proxy


