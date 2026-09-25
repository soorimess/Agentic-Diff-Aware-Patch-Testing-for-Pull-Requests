# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import os
import sys

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_keeps_non_dot_cwd_first_entry(monkeypatch):
    """When the first sys.path entry is neither '', '.' nor cwd it must be kept.

    Previously pylint.unconditionally removed the first sys.path entry which
    could remove extension-added paths. This test ensures that an arbitrary
    first entry is not removed by modify_sys_path().
    """
    # Ensure PYTHONPATH won't trigger the other branches in modify_sys_path
    monkeypatch.setenv("PYTHONPATH", "")

    original = list(sys.path)
    try:
        custom = "some_unique_path_for_test_7277"
        # Put the custom entry at the front
        sys.path.insert(0, custom)

        modify_sys_path()

        # After the fix, the custom first entry must remain. Before the fix
        # pylint popped the first element unconditionally and this assertion
        # would fail.
        assert sys.path[0] == custom
    finally:
        # Restore sys.path to avoid affecting other tests
        sys.path[:] = original


def test_modify_sys_path_removes_empty_dot_and_cwd_first_entry(monkeypatch):
    """If the first path is '', '.' or the cwd it must be removed.

    This exercises the branch that only removes the first sys.path entry when
    it is a representation of the current working directory.
    """
    monkeypatch.setenv("PYTHONPATH", "")

    original = list(sys.path)
    try:
        for value in ("", ".", os.getcwd()):
            # restore original before each iteration
            sys.path[:] = original[:]
            sys.path.insert(0, value)

            modify_sys_path()

            # The leading entry should have been removed by modify_sys_path()
            assert sys.path[0] != value
    finally:
        sys.path[:] = original
