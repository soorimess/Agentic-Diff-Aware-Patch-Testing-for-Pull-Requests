# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the sys.path modification bug.

This test ensures that pylint only removes the first item from sys.path
when it's one of: "", ".", or os.getcwd().
"""

from __future__ import annotations

import os
import sys

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_preserves_custom_paths():
    """Test that custom paths at the beginning of sys.path are not removed.
    
    This is the core bug: when running via runpy, a custom path gets inserted
    at the beginning of sys.path, and pylint was removing it regardless of 
    whether it was safe to do so.
    """
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # This simulates the problematic case from the bug report:
        # When runpy.run_module() is used, custom paths can be inserted at the beginning
        custom_path = "/some/custom/path/that/should/not/be/removed"
        sys.path = [custom_path, "some_other_path"]
        
        # Before the fix, this would remove the first item regardless of what it is
        # After the fix, this should preserve the first item since it's not "", ".", or cwd
        modify_sys_path()
        
        # The fix should preserve the custom path
        assert sys.path[0] == custom_path
        assert len(sys.path) == 2
        assert sys.path[1] == "some_other_path"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_removes_safe_entries():
    """Test that safe entries (empty string, dot, or cwd) are still removed."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test that "" is still removed (this was working before)
        sys.path = ["", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
        
        # Reset path
        sys.path = original_path
        
        # Test that "." is still removed (this was working before)
        sys.path = [".", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
        
        # Reset path
        sys.path = original_path
        
        # Test that cwd is still removed (this was working before)
        cwd = os.getcwd()
        sys.path = [cwd, "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path