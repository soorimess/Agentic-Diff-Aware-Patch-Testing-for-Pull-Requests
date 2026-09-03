"""One chronological record of everything that happens to one PR.

The artifacts we already write are each a slice: `tool_log.json` has the agent's
actions but not the container lifecycle, `before_fix.log` has one pytest run but no
idea what preceded it, `result.json` has the verdict but not how it was reached. Piecing
a run together means reading four files and interleaving them by hand.

This is the interleaving, written as it happens: container up, git stripped, every
command with its exit code and duration, the test appearing, both verification runs, the
verdict, the audit, container gone. Two forms of the same thing --

    flow.log     aligned text, meant to be read top to bottom
    flow.jsonl   one object per step, meant to be grepped and counted

Recording is a no-op when nothing is active, so the modules that call `record()` do not
need to know whether they are running under the agent, the oracle, or a bare script.
"""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

_current: "FlowLog | None" = None

# Phase tags, wide enough to align in the text log.
SETUP, AGENT, VERIFY, AUDIT = "setup", "agent", "verify", "audit"


class FlowLog:
    def __init__(self, directory: Path, title: str = ""):
        directory.mkdir(parents=True, exist_ok=True)
        self.text_path = directory / "flow.log"
        self.json_path = directory / "flow.jsonl"
        self.t0 = time.time()
        self.n = 0
        self._text = self.text_path.open("w", encoding="utf-8")
        self._json = self.json_path.open("w", encoding="utf-8")
        if title:
            self._text.write(f"{title}\n{'=' * len(title)}\n\n")
            self._text.write(f"{'t+':>8}  {'#':>3}  {'phase':<7} {'event':<18} detail\n")
            self._text.write(f"{'-' * 96}\n")
            self._text.flush()

    def step(self, phase: str, event: str, detail: str = "",
             duration: float | None = None, **data: Any) -> None:
        self.n += 1
        elapsed = time.time() - self.t0
        dur = f"  [{duration:.1f}s]" if duration is not None else ""
        first, *rest = (detail or "").splitlines() or [""]
        self._text.write(f"{elapsed:8.1f}  {self.n:3d}  {phase:<7} {event:<18} "
                         f"{first}{dur}\n")
        for line in rest[:40]:
            self._text.write(f"{'':8}  {'':3}  {'':7} {'':18} {line}\n")
        if len(rest) > 40:
            self._text.write(f"{'':8}  {'':3}  {'':7} {'':18} "
                             f"... [{len(rest) - 40} more lines]\n")
        self._text.flush()
        row = {"n": self.n, "t": round(elapsed, 2), "phase": phase, "event": event,
               "detail": detail}
        if duration is not None:
            row["duration_s"] = round(duration, 2)
        row.update(data)
        self._json.write(json.dumps(row) + "\n")
        self._json.flush()

    def close(self, summary: str = "") -> None:
        if summary:
            self._text.write(f"{'-' * 96}\n{summary}\n")
        self._text.write(f"\ntotal {time.time() - self.t0:.1f}s, {self.n} steps\n")
        self._text.close()
        self._json.close()


def record(phase: str, event: str, detail: str = "",
           duration: float | None = None, **data: Any) -> None:
    """Log a step, or do nothing if no run is being recorded."""
    if _current is not None:
        _current.step(phase, event, detail, duration, **data)


@contextmanager
def recording(directory: Path, title: str = ""):
    global _current
    previous, _current = _current, FlowLog(directory, title)
    try:
        yield _current
    finally:
        _current.close()
        _current = previous


# ---------------------------------------------------------------------------
# `out/` is committed, so what is written there leaves this machine.
#
# No credential has ever reached it -- the SDK's completion logger does not record
# request headers, and a scan of every file found no key, no gateway host and no proxy
# address. Absolute paths do reach it, though: litellm stack traces and the SDK's own
# error strings carry `/Users/<name>/...`, which is the developer's account name on
# their laptop and has no business in a public repository.
#
# Scrubbing happens on the way out rather than as a cleanup pass, so a future run cannot
# reintroduce what a cleanup already removed.
_HOME = str(Path.home())
_PROJECT = str(Path(__file__).resolve().parents[3])


def scrub(text: str) -> str:
    """Replace this machine's absolute paths with repository-relative markers."""
    if not text:
        return text
    return text.replace(_PROJECT, "<project>").replace(_HOME, "<home>")
