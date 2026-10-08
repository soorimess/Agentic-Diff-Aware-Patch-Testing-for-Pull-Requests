# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

import os
import sys
from unittest import mock

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_removes_correct_first_item():
    """Test that modify_sys_path only removes first item when it's empty, current dir, or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is "" (empty string) - should be removed
        sys.path = ["", "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_removes_correct_current_dir():
    """Test that modify_sys_path removes current directory from first position."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 2: First item is current directory - should be removed
        cwd = os.getcwd()
        sys.path = [cwd, "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_removes_correct_dot():
    """Test that modify_sys_path removes '.' from first position."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 3: First item is "." - should be removed
        sys.path = [".", "some_other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path", "another_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_preserves_non_standard_first_item():
    """Test that modify_sys_path preserves first item when it's not empty, current dir, or '.'."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 4: First item is a custom path - should NOT be removed
        custom_path = "/custom/path"
        sys.path = [custom_path, "some_other_path", "another_path"]
        modify_sys_path()
        # The custom path should remain
        assert sys.path[0] == custom_path
        assert len(sys.path) == 3  # custom_path + 2 others
    finally:
        sys.path = original_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the specific scenario from the bug report with runpy."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate the runpy scenario where a custom path is added first
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # This should NOT remove the custom path according to the fix
        modify_sys_path()
        
        # The custom path should still be there as first item
        assert sys.path[0] == custom_path
        # Should still have the same number of items (just the custom path is preserved)
        assert custom_path in sys.path
    finally:
        sys.path = original_path