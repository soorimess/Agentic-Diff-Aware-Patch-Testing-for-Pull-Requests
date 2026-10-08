# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the bug where pylint removes first item from sys.path when running from runpy."""

import os
import sys
from unittest import mock

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_removes_unsafe_first_item():
    """Test that modify_sys_path only removes the first item if it's safe (empty, '.', or cwd)."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is safe (empty string) - should be removed
        sys.path = ["", "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 2: First item is safe (current directory) - should be removed
        cwd = os.getcwd()
        sys.path = [cwd, "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 3: First item is safe (dot) - should be removed
        sys.path = [".", "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 4: First item is NOT safe - should NOT be removed (this is the bug)
        # This is the case that would break when running from runpy
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "some_other_path", "another_path"]
        original_sys_path = sys.path.copy()
        modify_sys_path()
        # The bug is that this would incorrectly remove the custom path
        # After the fix, it should NOT remove it
        assert sys.path == original_sys_path, (
            "First item in sys.path should NOT be removed if it's not '', '.', or cwd"
        )
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_with_pythonpath():
    """Test modify_sys_path behavior with PYTHONPATH modifications."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test with PYTHONPATH starting with colon
        with mock.patch.dict(os.environ, {"PYTHONPATH": ":/some/path"}):
            sys.path = ["", "/some/path", "some_other_path"]
            modify_sys_path()
            # Should remove first item (empty string) and second item (/some/path) 
            # because PYTHONPATH starts with ":"
            assert sys.path == ["some_other_path"]
            
        # Reset path
        sys.path = original_path
        
        # Test with PYTHONPATH ending with colon
        with mock.patch.dict(os.environ, {"PYTHONPATH": "/some/path:"}):
            sys.path = ["/some/path", "some_other_path", "another_path"]
            modify_sys_path()
            # Should remove second item because PYTHONPATH ends with ":"
            assert sys.path == ["/some/path", "another_path"]
            
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_runpy_scenario():
    """Test the specific scenario from the bug report using runpy."""
    # This simulates what happens when runpy.run_module('pylint', ...) is called
    # The bug occurs when sys.path[0] is not one of the safe values
    
    original_path = sys.path.copy()
    
    try:
        # Simulate the problematic case from the bug report
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)  # This is what runpy does
        
        # Check that our original path has the custom path at the front
        assert sys.path[0] == custom_path
        
        # Call modify_sys_path - this is where the bug manifests
        modify_sys_path()
        
        # After the fix, the custom path should still be there
        # (the bug would remove it)
        assert sys.path[0] == custom_path, (
            "Custom path should not be removed from sys.path when running from runpy"
        )
        
    finally:
        # Restore original sys.path
        sys.path = original_path