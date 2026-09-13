# Regression test for issue pylint-dev/pylint#6903
# Ensure fractional cpu shares (as in Kubernetes cgroups) do not lead
# to a returned CPU count of 0.

from __future__ import annotations

import builtins
import io
from pathlib import Path

import pytest

from pylint.lint import run as run_module


def test_cpu_count_never_zero_for_fractional_k8s_shares(monkeypatch):
    """Simulate k8s/cgroup files that specify a fractional CPU (cpu.shares < 1024).

    The old implementation computed int(cpu_shares / 1024) which can be 0 for
    small values (e.g. 2). This lead to a cpu count of 0 returned by
    _cpu_count() and caused multiprocessing to fail. After the fix the value
    must never be 0 in this situation.
    """
    # Patch Path.is_file to make the module believe cgroup files exist.
    orig_is_file = Path.is_file

    def _is_file(self: Path) -> bool:  # noqa: D401 - small helper
        p = str(self)
        if p in (
            "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
            "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
            "/sys/fs/cgroup/cpu/cpu.shares",
        ):
            return True
        return orig_is_file(self)

    monkeypatch.setattr(Path, "is_file", _is_file)

    # Patch builtins.open to return desired contents for the cgroup files.
    orig_open = builtins.open

    def _open(path, *args, **kwargs):
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            # -1 indicates not useful for quota-based determination (as in AWS/K8s)
            return io.StringIO("-1")
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return io.StringIO("100000")
        if path == "/sys/fs/cgroup/cpu/cpu.shares":
            # Small value that when divided by 1024 yields 0 if truncated to int
            return io.StringIO("2")
        return orig_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", _open)

    # Now call the function under test. In the buggy implementation this
    # would return 0; we assert it is >= 1.
    cpu_count = run_module._cpu_count()
    assert cpu_count >= 1, "_cpu_count() returned 0 for fractional cpu.shares"
