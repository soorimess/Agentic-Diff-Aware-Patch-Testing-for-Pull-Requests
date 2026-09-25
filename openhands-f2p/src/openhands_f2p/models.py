"""Which model answers, and what it needs, read from `models.json`.

Every model-specific decision used to be a global default in `llm_config.py` with a
comment naming the model it was tuned for: `api_mode="chat"` because `"auto"` resolved
gpt-5-mini to an endpoint that hung for the full 300 seconds, a token ceiling because a
reasoning model spent its whole budget and emitted no tool call, a timeout and a retry
count measured against one gateway. Changing model meant editing environment variables
and hoping.

They are data now, and the data is outside the code: `models.json` at the project root,
or wherever `F2P_MODELS_FILE` points. Adding a model or a gateway is an edit to that file
-- no Python, no reinstall, and a machine can carry its own without touching the repo.

    from openhands_f2p import models
    profile = models.profile_for("gpt-5-mini")

Three things this module owes the file, because a JSON registry has no compiler behind it:

* **Unknown keys are refused.** A typo like `"timout": 900` in a Python dataclass is a
  `TypeError` at import; in JSON it is a value that silently does nothing. Every key is
  checked against the dataclass and an unknown one names itself and the entry it is in.
* **A missing or broken file says where it looked.** Not a `FileNotFoundError` from three
  frames down.
* **Which model runs has no fallback at all.** `--model`, else `default_model` in the
  registry, else the run stops. It never resolves through an environment variable and
  never lands on a literal default: a run that silently swapped the model for a stronger
  one produced a result that looked like a finding.
* **Precedence runs CLI flag, registry, `FALLBACK_LLM_*`, built-in** for everything else
  -- timeouts, retries, token ceilings, API mode. The registry sits
  above the environment on purpose: a variable is global and a profile is per-model, so
  when the variable won, `LLM_TIMEOUT=600` in a `.env` silently overrode the 900 that
  `gpt-5.5` asks for and no profile could be trusted to mean anything. The `FALLBACK_`
  prefix is the rename that made that inversion legible in the file itself. A profile
  field left out is `None`, which is what makes the fallback reachable at all -- a field
  with a real default can never fall through.

What still cannot live here: gpt-5.5 through the LiteLLM proxy answers with two choices --
a text preamble in `choices[0]`, the tool call in `choices[1]` -- and the SDK reads the
first, so the agent records zero actions. No value in a JSON file reaches that; the choice
is made inside the SDK. It is recorded as `picks_first_choice: false` so the failure has a
name, and fixing it means wrapping the SDK's LLM.
"""
from __future__ import annotations

import fnmatch
import json
import os
from dataclasses import dataclass, fields
from pathlib import Path

from openhands_f2p.layout import PROJECT_ROOT

REGISTRY = Path(os.getenv("F2P_MODELS_FILE") or PROJECT_ROOT / "models.json")


@dataclass(frozen=True)
class Provider:
    """Where a model is reached, and under which credentials."""

    name: str
    prefix: str = ""
    """What litellm needs in front of the model id to route it. `litellm_proxy/` for a
    LiteLLM gateway; empty when the id already carries its own."""

    key_env: tuple[str, ...] = ("LLM_API_KEY", "OPENAI_API_KEY")
    base_env: tuple[str, ...] = ("LLM_BASE_URL", "OPENAI_BASE_URL")
    note: str = ""

    def key(self) -> str | None:
        return next((os.getenv(v) for v in self.key_env if os.getenv(v)), None)

    def base_url(self) -> str | None:
        return next((os.getenv(v) for v in self.base_env if os.getenv(v)), None)


# The floor, used when neither the registry nor a FALLBACK_ variable says otherwise.
# These are the values every measurement in this project was taken with.
BUILTIN: dict[str, object] = {
    "api_mode": "chat",
    "max_output_tokens": 32000,
    "native_tool_calling": None,
    "timeout": 600,
    "num_retries": 10,
    "retry_max_wait": 120,
}


def _coerce(raw: str, like: object):
    """A FALLBACK_ variable arrives as text; make it the type the setting wants."""
    if isinstance(like, bool) or (like is None and raw.strip().lower()
                                  in ("true", "false")):
        return raw.strip().lower() not in ("0", "false", "no", "off", "")
    if isinstance(like, int):
        try:
            return int(raw)
        except ValueError:
            raise SystemExit(
                f"  FALLBACK_LLM_* expected a number, got {raw!r}") from None
    return raw


@dataclass(frozen=True)
class ModelProfile:
    match: str
    """A glob against the bare model id: `gpt-5*`, `claude-*`, or an exact name."""

    provider: str = "litellm-proxy"

    # `None` means "this entry does not say", and that is what makes a fallback
    # reachable at all: a field with a real default can never fall through to one.
    # Unspecified resolves to FALLBACK_LLM_<NAME>, then to BUILTIN.
    api_mode: str | None = None
    """`chat` or `responses`. Never `auto`: against this gateway auto resolved gpt-5-mini
    to the Responses API, which hung for the full timeout on every call."""

    max_output_tokens: int | None = None
    native_tool_calling: bool | None = None
    """True forces the native API, False makes the SDK emulate calls through the prompt.
    Unset leaves the SDK's own judgement for that model in place, which is not the same
    as False."""

    timeout: int | None = None
    num_retries: int | None = None
    retry_max_wait: int | None = None

    picks_first_choice: bool = True
    """False for a model whose gateway returns the tool call somewhere other than
    `choices[0]`. Documentation, not yet behaviour -- see the module docstring."""

    salvages_xml_tool_calls: bool = False
    """True for a model that sometimes writes `<function=...>` into the message body
    instead of sending a tool call. `llm_adapters` then parses it back out. qwen3-coder
    does this on every provider that serves it, so a run without this reads as a model
    that cannot call tools rather than one whose reply was not converted."""

    extra_body: dict | None = None
    """Body fields added to every request, for a gateway that reads something outside
    the OpenAI schema. The LiteLLM proxy forwards unknown fields upstream unchanged,
    which is what makes this reach OpenRouter at all -- verified by sending
    `provider.ignore` and watching the `provider` in the reply change.

    This is how a model gets routed away from a bad upstream. `qwen3-coder-30b` is
    served by four of them and they do not behave the same: SiliconFlow returns a
    proper `tool_calls` array, Alibaba writes Qwen's `<function=...>` XML into the
    content instead, and Novita does that too except that the content usually arrives
    empty -- 113 of 244 replies in the first evaluation, each one billed. A model whose
    default route is broken is not a measurement of the model."""

    note: str = ""

    def setting(self, name: str):
        """One setting, resolved: this entry, else `FALLBACK_LLM_<NAME>`, else BUILTIN.

        The command line sits above all three and is applied by the caller, which knows
        which flags exist -- only `--model`, `--judge-model` and `--provider` do.
        """
        chosen = getattr(self, name)
        if chosen is not None:
            return chosen
        raw = os.getenv(f"FALLBACK_LLM_{name.upper()}")
        if raw not in (None, ""):
            return _coerce(raw, BUILTIN[name])
        return BUILTIN[name]

    def qualified(self, model: str) -> str:
        """The id in the form litellm wants, prefix included exactly once.

        Tested for the prefix, not for a slash. A gateway's own model ids may contain
        one -- `qwen/qwen3-14b`, `openrouter/openai/gpt-oss-20b` -- and treating a slash
        as "already qualified" handed those to litellm as provider `qwen`, which is not a
        provider, instead of routing them through the proxy that actually serves them.
        The slash belongs to the model's name on the gateway; the prefix says which
        gateway.
        """
        prefix = BY_PROVIDER[self.provider].prefix
        if not prefix or model.startswith(prefix):
            return model
        return f"{prefix}{model}"


def _build(cls, entry: dict, where: str):
    """One dataclass from one JSON object, refusing anything it does not understand."""
    known = {f.name for f in fields(cls)}
    unknown = sorted(set(entry) - known)
    if unknown:
        raise SystemExit(
            f"  {REGISTRY}: {where} has unknown field(s) {', '.join(unknown)}.\n"
            f"  Known: {', '.join(sorted(known))}")
    kwargs = dict(entry)
    for key in ("key_env", "base_env"):            # lists in JSON, tuples in the dataclass
        if key in kwargs:
            kwargs[key] = tuple(kwargs[key])
    return cls(**kwargs)


def _load() -> tuple[dict, tuple[Provider, ...], tuple[ModelProfile, ...],
                     str, str, int]:
    if not REGISTRY.exists():
        raise SystemExit(
            f"  no model registry at {REGISTRY}\n"
            f"  It ships with the project; set F2P_MODELS_FILE to point elsewhere.")
    try:
        raw = json.loads(REGISTRY.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"  {REGISTRY} is not valid JSON: {exc}") from None
    provs = tuple(_build(Provider, p, f"provider {p.get('name', '?')!r}")
                  for p in raw.get("providers", []))
    profs = tuple(_build(ModelProfile, m, f"model {m.get('match', '?')!r}")
                  for m in raw.get("models", []))
    if not provs or not profs:
        raise SystemExit(f"  {REGISTRY}: needs at least one provider and one model")
    names = {p.name for p in provs}
    for m in profs:
        if m.provider not in names:
            raise SystemExit(
                f"  {REGISTRY}: model {m.match!r} names provider {m.provider!r}, which "
                f"is not defined. Defined: {', '.join(sorted(names))}")
    # No fallback on *which model runs*. A missing default used to resolve through
    # FALLBACK_LLM_MODEL and then to a literal "gpt-5-mini", so a run that forgot
    # --model produced a clean-looking result on a different model than the arm it
    # was being compared against. That happened, cost a run, and read as variance.
    # Everything below is a hard error instead; the numeric settings keep their
    # FALLBACK_ defaults, because those fill in unspecified knobs rather than
    # substituting one model for another.
    if not raw.get("default_model"):
        raise SystemExit(f"  {REGISTRY}: 'default_model' is required. "
                         f"There is no fallback for which model runs -- name it here "
                         f"or pass --model.")
    if not raw.get("default_judge"):
        raise SystemExit(f"  {REGISTRY}: 'default_judge' is required. "
                         f"There is no fallback for which judge runs.")
    return (raw, provs, profs,
            raw["default_model"], raw["default_judge"], _judge_timeout(raw))


def _judge_timeout(raw: dict) -> int:
    """Seconds for the one judge call: registry, else the fallback variable, else 180.

    Deliberately not the judge model's profile `timeout`, which is sized for an agent
    run. One call that reads two tests does not need fifteen minutes to fail in.
    """
    chosen = raw.get("default_judge_timeout")
    if chosen is None:
        chosen = os.getenv("FALLBACK_LLM_JUDGE_TIMEOUT") or 180
    return int(chosen)


_RAW, PROVIDERS, MODELS, DEFAULT_MODEL, DEFAULT_JUDGE, DEFAULT_JUDGE_TIMEOUT = _load()
BY_PROVIDER = {p.name: p for p in PROVIDERS}


def profile_for(model: str) -> ModelProfile:
    """The first profile whose glob matches the bare id."""
    bare = model.split("/")[-1]
    for p in MODELS:
        if fnmatch.fnmatch(bare, p.match):
            return p
    # Only reachable if the file has no `*` entry, which is a registry worth fixing.
    return MODELS[-1]


def _temperature(text: str) -> float:
    """A temperature, or a refusal -- never a silently clamped value."""
    import argparse
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a number: {text!r}") from None
    if not 0.0 <= value <= 2.0:
        raise argparse.ArgumentTypeError(f"{value} is outside 0 to 2")
    return value


def add_arguments(parser: object) -> None:
    """`--model`, `--judge-model` and `--provider`, from the registry, so a profile added
    to the JSON is selectable without touching this file."""
    known = ", ".join(p.match for p in MODELS if "*" not in p.match)
    group = parser.add_argument_group(
        "which model answers",
        f"A name matched against the profile registry in {REGISTRY.name}, which supplies "
        f"the API mode, token ceiling, timeout and retry policy that model needs. These "
        f"flags win over the registry; the registry wins over FALLBACK_LLM_*.")
    group.add_argument("--model", default=None,
                       help=f"the agent's model (default: {DEFAULT_MODEL}, from the "
                            f"registry). Profiled: {known}")
    group.add_argument("--judge-model", default=None,
                       help=f"the model that compares the generated test with the "
                            f"developer's (default: {DEFAULT_JUDGE}, from the registry)")
    group.add_argument("--temperature", type=_temperature, default=None,
                       help="the agent's sampling temperature, 0 to 2. Unset (the "
                            "default) sends none and the provider picks -- which is what "
                            "every run before this flag did. Applies to the agent only; "
                            "the judge is not affected")
    group.add_argument("--provider", default=None, choices=tuple(BY_PROVIDER),
                       help="override the profile's provider, for reaching the same "
                            "model id through a different gateway")


def describe() -> str:
    """The resolved table, which is the one worth printing.

    A profile that leaves a field out is not silent -- it means the fallback variable,
    else the built-in -- so showing the raw entry would show `None` where a run will use
    600. Values the entry itself names are starred; the rest were resolved.
    """
    lines = [f"Model profiles from {REGISTRY}, first match wins.",
             f"Defaults: agent {DEFAULT_MODEL}, judge {DEFAULT_JUDGE}, "
             f"judge timeout {DEFAULT_JUDGE_TIMEOUT}s",
             f"Precedence: CLI flag, this file, FALLBACK_LLM_*, built in. "
             f"* marks a value this file names.\n"]
    for p in MODELS:
        def show(name: str, unit: str = "") -> str:
            star = "*" if getattr(p, name) is not None else ""
            return f"{p.setting(name)}{unit}{star}"
        native = ("SDK default" if p.setting("native_tool_calling") is None
                  else show("native_tool_calling"))
        lines.append(f"  {p.match:14s} {p.provider:14s} api={show('api_mode'):10s} "
                     f"out={show('max_output_tokens'):<7} "
                     f"timeout={show('timeout', 's'):8s}"
                     f"retries={show('num_retries')}  native_tools={native}")
        if p.note:
            lines.append(f"  {'':14s} {p.note}")
        lines.append("")
    lines.append("Providers:")
    for v in PROVIDERS:
        lines.append(f"  {v.name:14s} prefix={v.prefix or '(none)':16s} "
                     f"key from {', '.join(v.key_env)}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(describe())
