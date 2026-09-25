# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the sys.path modification bug in pylint.

This test verifies that pylint only removes the first item from sys.path when it is 
"", ".", or os.getcwd(), but not when it's a custom path added by the user.
"""

import os
import sys

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_preserves_user_added_paths():
    """Test that modify_sys_path does not remove user-added paths from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test exact bug scenario: a user/extension adds a path that gets removed
        # This simulates what happens during runpy.run_module
        user_added_path = "something"  # User/extension path that should NOT be removed
        sys.path = [user_added_path, "/some/path", "/another/path"]
        
        # The bug: unconditionally removes first element (incorrect)
        # The fix: only removes first element if it's "", ".", or cwd
        modify_sys_path()
        
        # Bug behavior: the user's path gets removed
        # Fixed behavior: the user's path should remain
        assert sys.path[0] == user_added_path, (
            f"User-added path '{user_added_path}' was incorrectly removed from sys.path. "
            f"This would break importing libraries added by pylint extensions."
        )
        
    finally:
        # Always restore the original path
        sys.path = original_path


def test_modify_sys_path_removes_safe_paths():
    """Test that modify_sys_path still removes safe paths like "", ".", and cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: sys.path starts with "", should be removed (safe)
        sys.path = ["", "/some/path", "/another/path"]
        modify_sys_path()
        # Check it was removed exactly as designed 
        assert sys.path == ["/some/path", "/another/path"]
        
        # Restore original
        sys.path = original_path.copy()
        
        # Test case 2: sys.path starts with ".", should be removed (safe)
        sys.path = [".", "/some/path", "/another/path"]
        modify_sys_path()
        # Check it was removed exactly as designed 
        assert sys.path == ["/some/path", "/another/path"]
        
        # Restore original
        sys.path = original_path.copy()
        
        # Test case 3: sys.path starts with cwd, should be removed (safe)
        cwd = os.getcwd()
        sys.path = [cwd, "/some/path", "/another/path"]
        modify_sys_path()
        # Check it was removed exactly as designed 
        assert sys.path == ["/some/path", "/another/path"]
        
    finally:
        # Always restore the original path
        sys.path = original_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the exact scenario from the bug report using runpy conditions."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # This mimics the exact problem from bug report:
        # When runpy.run_module('pylint', run_name="__main__", alter_sys=True) 
        # is executed, the system state is such that the user path is prepended to sys.path
        # The bug is that pylint's modify_sys_path removes that user path unconditionally
        
        # In practice this happens during runpy execution
        # Before running pylint, some library adds paths to sys.path
        user_added_path = "user_library_path"  # The path added by an extension
        sys.path.insert(0, user_added_path) 
        
        # Make sure we are properly set up
        assert sys.path[0] == user_added_path
        
        # Run the function that caused the bug
        # This function used to unconditionally do "sys.path.pop(0)"
        modify_sys_path() 
        
        # In the buggy version, this would remove user_added_path, breaking imports
        # In fixed version, this should preserve user_added_path
        assert sys.path[0] == user_added_path, (
            "User-added path was removed by modify_sys_path, causing import failures."
        )
        
    finally:
        sys.path = original_path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])