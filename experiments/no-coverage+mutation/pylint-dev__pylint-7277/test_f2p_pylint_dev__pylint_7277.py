# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint issue #7277.

This test ensures that pylint doesn't incorrectly remove items from sys.path
that are not the empty string, current directory, or current working directory.
"""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_preserves_non_standard_paths() -> None:
    """Test that modify_sys_path preserves non-standard paths at the beginning of sys.path.
    
    This addresses a bug where pylint was unconditionally removing the first item
    from sys.path, even when it wasn't one of the standard paths to be removed.
    """
    # Save original sys.path 
    original_path = sys.path[:]
    
    try:
        # Test case: simulate what happens when an extension adds a custom path
        # and pylint gets run via runpy (which can result in non-standard 
        # items at the beginning of sys.path)
        custom_path = "/some/custom/lib"
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path - this should NOT remove our custom path
        # because it's not "", ".", or os.getcwd()
        modify_sys_path()
        
        # Verify that our custom path is still present in sys.path
        # (the bug was that it would be removed even when it shouldn't be)
        # In the FIXED version, only "", ".", or cwd should be removed from the beginning
        assert custom_path in sys.path, (
            f"Custom path {custom_path} was incorrectly removed from sys.path. "
            f"sys.path after modify_sys_path: {sys.path}"
        )
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_standard_paths() -> None:
    """Test that modify_sys_path still removes standard paths from sys.path."""
    # Test with empty string at the beginning (should be removed)
    original_path = sys.path[:]
    try:
        sys.path.insert(0, "")
        modify_sys_path()
        assert sys.path[0] != "", "Empty string path should be removed from sys.path"
    finally:
        sys.path[:] = original_path
        
    # Test with current directory at the beginning (should be removed)  
    original_path = sys.path[:]
    try:
        sys.path.insert(0, ".")
        modify_sys_path()
        assert sys.path[0] != ".", "Current directory path should be removed from sys.path"
    finally:
        sys.path[:] = original_path
        
    # Test with current working directory at the beginning (should be removed)
    original_path = sys.path[:]
    try:
        sys.path.insert(0, os.getcwd())
        modify_sys_path()
        assert sys.path[0] != os.getcwd(), "Current working directory should be removed from sys.path"
    finally:
        sys.path[:] = original_path