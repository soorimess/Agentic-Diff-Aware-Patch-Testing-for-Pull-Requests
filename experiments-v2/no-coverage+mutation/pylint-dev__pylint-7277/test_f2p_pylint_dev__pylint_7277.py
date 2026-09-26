# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint issue #7277.

This test ensures that pylint only removes the first item from sys.path
when it's an empty string, current directory, or the current working directory.
"""

import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_only_removes_special_first_items():
    """Test that modify_sys_path only removes first item when it's empty, '.', or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is empty string (should be removed)
        sys.path = ["", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"], f"Expected ['', 'some_other_path'] to become ['some_other_path'], but got {sys.path}"
        
        # Test case 2: First item is current directory (should be removed)  
        sys.path = [os.getcwd(), "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"], f"Expected [{os.getcwd()}, 'some_other_path'] to become ['some_other_path'], but got {sys.path}"
        
        # Test case 3: First item is '.' (should be removed)
        sys.path = [".", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"], f"Expected ['.', 'some_other_path'] to become ['some_other_path'], but got {sys.path}"
        
        # Test case 4: First item is a custom path (should NOT be removed)
        # This is the main bug - it should NOT remove custom paths
        custom_path = "/custom/path"
        sys.path = [custom_path, "some_other_path"]
        modify_sys_path()
        assert sys.path == [custom_path, "some_other_path"], f"Expected ['/custom/path', 'some_other_path'] to remain unchanged, but got {sys.path}"
        
        # Test case 5: First item is a custom path that's not empty, '.', or cwd (should NOT be removed)
        custom_path = "/another/custom/path"
        sys.path = [custom_path, "some_other_path", "yet_another_path"]
        modify_sys_path()
        assert sys.path == [custom_path, "some_other_path", "yet_another_path"], f"Expected ['/another/custom/path', 'some_other_path', 'yet_another_path'] to remain unchanged, but got {sys.path}"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the specific scenario from the bug report: runpy usage."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate the scenario from the bug report:
        # User adds a path to sys.path
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # This should NOT remove the custom path that was added
        modify_sys_path()
        
        # The custom path should still be there (not removed)
        assert custom_path in sys.path, f"Custom path {custom_path} should still be in sys.path"
        
        # The first item should be the custom path (not removed)
        assert sys.path[0] == custom_path, f"First item should be {custom_path}, but got {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path = original_path