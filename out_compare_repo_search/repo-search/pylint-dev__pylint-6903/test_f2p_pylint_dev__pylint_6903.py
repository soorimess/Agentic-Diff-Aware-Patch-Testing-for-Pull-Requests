# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# Regression test for pylint-dev/pylint#6903

from __future__ import annotations

import builtins
from io import StringIO
from pathlib import Path

import pytest

from pylint.lint.run import _query_cpu


def test_query_cpu_never_returns_zero(monkeypatch) -> None:
    """When cgroup cpu.shares yields a fraction (<1024) ensure we don't get 0.

    This exercises the situation in some container environments where
    cpu.shares can be very small (e.g. "2") which when divided by 1024
    and cast to int yields 0. Previously _query_cpu() could return 0,
    which later led to multiprocessing.Pool(0) and a crash. The desired
    behavior is to treat 0 as at least 1 CPU.
    """

    # Keep references to the originals so other code continues to work
    orig_is_file = Path.is_file
    orig_open = builtins.open

    def fake_is_file(self) -> bool:
        p = str(self)
        if p == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return False
        if p == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return False
        if p == "/sys/fs/cgroup/cpu/cpu.shares":
            return True
        return orig_is_file(self)

    def fake_open(path, *args, **kwargs):
        # Only intercept reads of the cpu.shares file
        if str(path) == "/sys/fs/cgroup/cpu/cpu.shares":
            return StringIO("2")
        return orig_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "is_file", fake_is_file)
    monkeypatch.setattr(builtins, "open", fake_open)

    try:
        avail = _query_cpu()
    finally:
        # Ensure monkeypatch cleanup in case other tests rely on unchanged behavior
        monkeypatch.setattr(Path, "is_file", orig_is_file)
        monkeypatch.setattr(builtins, "open", orig_open)

    # The regression was that _query_cpu() returned 0 here. It must be at least 1.
    assert avail is not None and avail >= 1
