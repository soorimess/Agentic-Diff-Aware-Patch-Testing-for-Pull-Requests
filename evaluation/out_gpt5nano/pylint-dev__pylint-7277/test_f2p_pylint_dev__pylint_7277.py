# Regression test for pylint/pylint#7277: ensure modify_sys_path handles first-entry edge cases

from __future__ import annotations

import sys
import os

import pytest

import pylint  # noqa: F401


def test_modify_sys_path_keeps_non_special_first_entry(monkeypatch) -> None:
    """When the first entry of sys.path is a non-special path (not '', '.', or cwd),
    modify_sys_path should not remove it.
    """
    original_sys_path = list(sys.path)
    try:
        sys.path = ["custom_path", os.path.abspath("/tmp"), ""]
        monkeypatch.setenv("PYTHONPATH", "")
        pylint.modify_sys_path()
        assert sys.path[0] == "custom_path"
    finally:
        sys.path = original_sys_path


def test_modify_sys_path_pop_empty_entry(monkeypatch) -> None:
    """When the first entry is the empty string, it should be popped by modify_sys_path."""
    original_sys_path = list(sys.path)
    try:
        sys.path = ["", os.path.abspath("/tmp"), ""]
        monkeypatch.setenv("PYTHONPATH", "")
        pylint.modify_sys_path()
        # First entry should be popped, new first entry should be /tmp
        assert sys.path[0] == os.path.abspath("/tmp")
    finally:
        sys.path = original_sys_path
