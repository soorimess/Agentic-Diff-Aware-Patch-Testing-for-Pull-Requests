# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the sys.path modification behavior in pylint."""

from __future__ import annotations

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_should_not_remove_custom_paths_added_by_extensions() -> None:
    """Test that modify_sys_path does not remove custom paths added by extensions.
    
    This test reproduces the exact scenario from the bug report:
    When using pylint extension which bundles the libraries, the extension 
    adds them to sys.path depending on user settings. Pylint removes the first 
    entry from sys path causing it to fail to load.
    """
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Reproduce the exact scenario from the bug report
        custom_path = "something"  # This simulates what an extension might add
        sys.path.insert(0, custom_path)
        
        # Store what we expect to see after modify_sys_path
        expected_first_item = custom_path
        
        # Call the function that has the bug
        modify_sys_path()
        
        # With the BUGGY implementation, this will fail because custom_path gets removed
        # With the FIXED implementation, this should pass because custom_path should remain
        assert sys.path[0] == expected_first_item, (
            f"Custom path {custom_path} was incorrectly removed from sys.path. "
            f"Expected first item to be {expected_first_item}, but got {sys.path[0] if sys.path else 'empty'}"
        )
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_should_remove_empty_string() -> None:
    """Test that modify_sys_path correctly removes empty string from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Empty string should be removed (this is correct behavior)
        sys.path = ["", "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_should_remove_current_directory() -> None:
    """Test that modify_sys_path correctly removes current directory from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Current directory should be removed (this is correct behavior)
        cwd = os.getcwd()
        sys.path = [cwd, "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_should_remove_dot() -> None:
    """Test that modify_sys_path correctly removes dot from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Dot should be removed (this is correct behavior)
        sys.path = [".", "other_path"]
        modify_sys_path()
        assert sys.path == ["other_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path