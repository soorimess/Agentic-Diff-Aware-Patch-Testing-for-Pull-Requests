# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_should_preserve_custom_paths():
    """Test that modify_sys_path preserves custom paths at the beginning of sys.path.
    
    The bug: modify_sys_path unconditionally removes sys.path[0]
    The fix: only remove sys.path[0] if it's one of ('', '.', cwd)
    """
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a custom path to the beginning of sys.path (simulating runpy behavior)
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path - with the bug, this removes our custom path
        # With the fix, this should preserve our custom path
        modify_sys_path()
        
        # Verify that our custom path is still there (this should pass after fix)
        assert custom_path in sys.path, "Custom path should not be removed by modify_sys_path"
        # The custom path should remain at index 0
        assert sys.path[0] == custom_path, "Custom path should remain at the beginning"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_should_remove_expected_paths():
    """Test that modify_sys_path still removes expected paths like "" and ".".
    
    The function should still remove the first item if it's one of the expected values.
    """
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add an expected path to the beginning of sys.path
        # This should be removed by modify_sys_path
        sys.path.insert(0, "")  # Empty string should be removed
        
        # Call modify_sys_path - this SHOULD remove the empty string
        modify_sys_path()
        
        # Verify that empty string path was removed
        assert "" not in sys.path, "Empty string path should be removed by modify_sys_path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_should_remove_dot_path():
    """Test that modify_sys_path removes '.' path correctly."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a dot path to the beginning of sys.path
        sys.path.insert(0, ".")  # Dot should be removed
        
        # Call modify_sys_path - this SHOULD remove the dot
        modify_sys_path()
        
        # Verify that dot path was removed
        assert "." not in sys.path, "Dot path should be removed by modify_sys_path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path