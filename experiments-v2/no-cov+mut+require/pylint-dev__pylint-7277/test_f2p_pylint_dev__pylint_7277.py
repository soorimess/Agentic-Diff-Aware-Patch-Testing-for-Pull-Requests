# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint issue #7277.

This test ensures that pylint does not remove the first item from sys.path
when it is not one of the expected values (empty string, current directory, or cwd).
"""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_removes_first_item_when_expected():
    """Test that modify_sys_path removes the first item when it's empty, '.', or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is empty string - should be removed
        sys.path = ["", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_removes_first_item_when_it_is_current_dir():
    """Test that modify_sys_path removes the first item when it's current directory."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 2: First item is current directory - should be removed
        cwd = os.getcwd()
        sys.path = [cwd, "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_removes_first_item_when_it_is_dot():
    """Test that modify_sys_path removes the first item when it's '.'."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 3: First item is '.' - should be removed
        sys.path = [".", "some_other_path"]
        modify_sys_path()
        assert sys.path == ["some_other_path"]
    finally:
        sys.path = original_path


def test_modify_sys_path_preserves_first_item_when_not_expected():
    """Test that modify_sys_path preserves the first item when it's not empty, '.', or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 4: First item is a custom path - should NOT be removed
        # This is the bug scenario: when runpy adds a custom path to sys.path
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "some_other_path"]
        modify_sys_path()
        # This should NOT remove the first item (this is the bug)
        assert sys.path[0] == custom_path, f"Custom path should be preserved, got {sys.path[0]}"
        assert len(sys.path) == 2, "Should preserve both items"
    finally:
        sys.path = original_path


def test_modify_sys_path_with_runpy_simulation():
    """Test the exact scenario from the bug report."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate what runpy does: insert a custom path at the beginning
        # This simulates the exact scenario from the bug report
        custom_path = "something"
        sys.path.insert(0, custom_path)
        
        # The bug: modify_sys_path unconditionally removes first item
        # The fix: only remove first item if it's "", ".", or cwd
        modify_sys_path()
        
        # After the fix, the custom path should be preserved
        # Before the fix, it would have been removed
        assert sys.path[0] == custom_path, f"Custom path should be preserved, got {sys.path[0]}"
        assert len(sys.path) >= 1, "Should preserve at least the custom path"
    finally:
        sys.path = original_path