# Regression test for pylint issue #6903
# Ensure that _query_cpu() never returns 0 when cgroup cpu.shares yields
# a fractional CPU (e.g. 2/1024 -> 0). The correct behavior is to
# treat a fractional available CPU as at least 1.

from io import StringIO
import builtins
from pathlib import Path

import pytest

from pylint.lint.run import _query_cpu


def test_query_cpu_never_zero_for_small_cpu_shares(monkeypatch):
    """Simulate a cgroup environment where cpu.cfs_quota_us is -1 and
    cpu.shares is small (2). Historically this produced 0; it should
    be treated as 1.
    """

    # Make Path.is_file return True only for the cgroup files we care about
    def fake_is_file(self):
        p = str(self)
        if p in (
            "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
            "/sys/fs/cgroup/cpu/cpu.shares",
            "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
        ):
            return True
        return False

    monkeypatch.setattr(Path, "is_file", fake_is_file)

    # Keep reference to the real open to delegate unknown paths
    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        # Emulate the files read by _query_cpu
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return StringIO("-1")
        if path == "/sys/fs/cgroup/cpu/cpu.shares":
            return StringIO("2")
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            # not used for this scenario but present if checked
            return StringIO("100000")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)

    # Under the old (buggy) implementation this would return 0. The
    # correct behavior is to return at least 1.
    val = _query_cpu()
    assert val == 1, "_query_cpu() must treat fractional cpu as at least 1"
