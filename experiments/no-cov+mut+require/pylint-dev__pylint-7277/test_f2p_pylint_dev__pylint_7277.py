# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression tests for the sys.path modification issue in pylint."""

import os
import sys
from unittest.mock import patch

from pylint import modify_sys_path


def test_modify_sys_path_preserves_non_special_paths():
    """Test that modify_sys_path preserves non-special first entries in sys.path."""
    # Backup original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a non-special path at the beginning
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path
        modify_sys_path()
        
        # The custom path should still be there, not removed
        assert sys.path[0] == custom_path, f"Expected {custom_path} to remain in sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_special_paths():
    """Test that modify_sys_path removes special first entries in sys.path."""
    # Backup original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a special path at the beginning
        cwd = os.getcwd()
        sys.path.insert(0, "")  # empty string is special
        
        # Call modify_sys_path
        modify_sys_path()
        
        # The empty string should be removed
        assert sys.path[0] != "", "Empty string should be removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the specific scenario mentioned in the bug report."""
    # Backup original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate the scenario from the bug report:
        # sys.path.insert(0, "something")
        custom_path = "something"
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path as it would be called when run from runpy
        modify_sys_path()
        
        # The custom path should still be at the front - this is the expected behavior
        # that was broken before the fix
        assert sys.path[0] == custom_path, f"Expected {custom_path} to remain in sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_with_dot_path():
    """Test that modify_sys_path removes the '.' path."""
    # Backup original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a '.' path at the beginning
        sys.path.insert(0, ".")
        
        # Call modify_sys_path
        modify_sys_path()
        
        # The '.' should be removed
        assert sys.path[0] != ".", "Dot path should be removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path