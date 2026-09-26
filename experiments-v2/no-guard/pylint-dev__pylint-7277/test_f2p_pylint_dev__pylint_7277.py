# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_preserves_custom_paths():
    """Test that modify_sys_path does not remove custom paths from sys.path.
    
    This is a regression test for a bug where pylint would remove the first item
    from sys.path regardless of whether it was one of the special values ("" , ".", 
    or os.getcwd()). This caused issues when extensions added custom paths that 
    should not be removed.
    """
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Add a custom path that is NOT "", ".", or current working directory
        custom_path = "/tmp/some_custom_path_that_should_not_be_removed"
        
        # Insert at the beginning (this should be preserved)
        sys.path.insert(0, custom_path)
        
        # Verify the custom path is at the beginning
        assert sys.path[0] == custom_path
        
        # Call modify_sys_path - this should NOT remove our custom path
        modify_sys_path()
        
        # The custom path should still be in sys.path (not removed)
        # If it was removed, this assertion would fail
        assert custom_path in sys.path, (
            "Custom path was incorrectly removed from sys.path by modify_sys_path"
        )
        
        # The first element should still be our custom path (not removed)
        assert sys.path[0] == custom_path, (
            "Custom path was incorrectly removed - first element changed"
        )
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path


def test_modify_sys_path_removes_special_paths():
    """Test that modify_sys_path still removes special paths correctly."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Test with empty string as first path (should be removed)
        sys.path.insert(0, "")
        assert sys.path[0] == ""
        
        # Call modify_sys_path - this SHOULD remove the empty string
        modify_sys_path()
        
        # Empty string should be removed
        assert "" not in sys.path
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path


def test_modify_sys_path_removes_dot():
    """Test that modify_sys_path removes '.' from sys.path."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Add '.' as first path (should be removed)
        sys.path.insert(0, ".")
        assert sys.path[0] == "."
        
        # Call modify_sys_path - this SHOULD remove the '.'
        modify_sys_path()
        
        # '.' should be removed
        assert "." not in sys.path
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path