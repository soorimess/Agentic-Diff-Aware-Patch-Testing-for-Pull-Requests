# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the bug where pylint removes first item from sys.path when running from runpy."""

import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_removes_first_item_when_empty():
    """Test that modify_sys_path removes the first item when it's empty string (the default)."""
    # Arrange
    original_path = sys.path.copy()
    
    # Set up sys.path so first item is empty string (default behavior)
    sys.path = ["", "some_other_path", "another_path"]
    expected_path = ["some_other_path", "another_path"]
    
    try:
        # Act
        modify_sys_path()
        
        # Assert
        assert sys.path == expected_path
    finally:
        # Cleanup
        sys.path = original_path


def test_modify_sys_path_removes_first_item_when_dot():
    """Test that modify_sys_path removes the first item when it's '.' (current directory)."""
    # Arrange
    original_path = sys.path.copy()
    
    # Set up sys.path so first item is dot
    sys.path = [".", "some_other_path", "another_path"]
    expected_path = ["some_other_path", "another_path"]
    
    try:
        # Act
        modify_sys_path()
        
        # Assert
        assert sys.path == expected_path
    finally:
        # Cleanup
        sys.path = original_path


def test_modify_sys_path_removes_first_item_when_cwd():
    """Test that modify_sys_path removes the first item when it's current working directory."""
    # Arrange
    original_path = sys.path.copy()
    cwd = os.getcwd()
    
    # Set up sys.path so first item is current working directory
    sys.path = [cwd, "some_other_path", "another_path"]
    expected_path = ["some_other_path", "another_path"]
    
    try:
        # Act
        modify_sys_path()
        
        # Assert
        assert sys.path == expected_path
    finally:
        # Cleanup
        sys.path = original_path


def test_modify_sys_path_preserves_first_item_when_not_special():
    """Test that modify_sys_path does NOT remove the first item when it's a custom path."""
    # Arrange
    original_path = sys.path.copy()
    
    # Set up sys.path so first item is a custom path that should NOT be removed
    custom_path = "/custom/path/that/should/not/be/removed"
    sys.path = [custom_path, "some_other_path", "another_path"]
    
    # This should remain unchanged since it's not a special path ("", ".", or cwd)
    expected_path = [custom_path, "some_other_path", "another_path"]
    
    try:
        # Act
        modify_sys_path()
        
        # Assert
        assert sys.path == expected_path
    finally:
        # Cleanup
        sys.path = original_path


def test_modify_sys_path_with_runpy_simulation():
    """Test simulating the exact scenario from the bug report using runpy."""
    # This test verifies the behavior with runpy which was the original trigger
    original_path = sys.path.copy()
    cwd = os.getcwd()
    
    try:
        # Simulate what happens when we run:
        # sys.path.insert(0, "something")
        # runpy.run_module('pylint', run_name="__main__", alter_sys=True)
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # The bug was that modify_sys_path() would remove *any* first item,
        # even custom ones like /some/custom/path
        current_first_item = sys.path[0]
        assert current_first_item == custom_path
        
        # Call the function that was problematic (this mimics what pylint does)
        modify_sys_path()
        
        # Before the fix, this would incorrectly remove custom_path,
        # but after the fix it should preserve custom_path
        # (since it's not "", ".", or cwd)
        expected_path = [custom_path] + original_path[1:]  # custom path at start + rest
        
        # In the fixed version, since custom_path != "", ".", or cwd, it should NOT be removed
        assert sys.path[0] == custom_path
        
    finally:
        # Cleanup
        sys.path = original_path