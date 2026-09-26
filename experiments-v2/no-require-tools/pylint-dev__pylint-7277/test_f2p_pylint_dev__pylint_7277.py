# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the bug where pylint removes first item from sys.path when running from runpy."""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_only_removes_safe_entries():
    """Test that modify_sys_path only removes the first item if it's safe to do so.
    
    The bug was that pylint unconditionally removed the first item from sys.path.
    It should only remove it if it's "", ".", or os.getcwd().
    """
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Test 1: First item is "" (should be removed)
        sys.path = ["", "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
        # Test 2: First item is "." (should be removed)
        sys.path = [".", "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
        # Test 3: First item is current working directory (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
        # Test 4: First item is something else (should NOT be removed)
        # This is the main bug - it was removing this incorrectly before the fix
        sys.path = ["some_other_path", "other_path"]
        modify_sys_path()
        # This assertion should pass after the fix, fail before the fix
        assert sys.path == ["some_other_path", "other_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_preserves_user_import_paths():
    """Test that user-added paths are preserved (core issue from bug report)."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Simulate the exact scenario from the bug report:
        # User adds a path to sys.path, then runs pylint via runpy
        user_path = "/some/user/important/path"
        sys.path.insert(0, user_path)
        
        # This should NOT remove user_path because it's not "", ".", or cwd
        modify_sys_path()
        
        # The user path should still be there (this is the bug - it was being removed)
        assert user_path in sys.path, f"User path {user_path} was incorrectly removed from sys.path"
        
        # The first item should be the user path (not removed)
        assert sys.path[0] == user_path
        
    finally:
        # Restore original sys.path
        sys.path = original_sys_path