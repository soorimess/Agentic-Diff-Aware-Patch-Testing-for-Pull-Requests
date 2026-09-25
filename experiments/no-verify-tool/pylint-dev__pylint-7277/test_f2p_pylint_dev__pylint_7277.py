# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the specific bug in pylint issue #7277.

This test reproduces the behavior where pylint incorrectly removes the first
item from sys.path - this affects cases when the first item is not ""
or "." or os.getcwd().
"""

import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_removes_wrong_first_item():
    """Test that modify_sys_path doesn't remove non-standard first items from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a custom path entry that should NOT be removed
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Call the function
        modify_sys_path()
        
        # Check that our custom path is still there (bug: it would be removed)
        assert custom_path in sys.path, f"Custom path {custom_path} was incorrectly removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_standard_first_item():
    """Test that modify_sys_path does remove standard first items from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a standard path entry that SHOULD be removed
        sys.path.insert(0, "")  # Empty string at start
        
        # Call the function
        modify_sys_path()
        
        # Check that the empty string was removed
        assert "" not in sys.path, "Empty string path should be removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_with_current_dir():
    """Test that modify_sys_path removes current working directory when it's first."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add current working directory at start (should be removed)
        cwd = os.getcwd()
        sys.path.insert(0, cwd)
        
        # Call the function
        modify_sys_path()
        
        # Check that the current working directory was removed
        assert cwd not in sys.path, "Current working directory should be removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_with_dot():
    """Test that modify_sys_path removes '.' when it's first."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add '.' at start (should be removed)
        sys.path.insert(0, ".")
        
        # Call the function
        modify_sys_path()
        
        # Check that '.' was removed
        assert "." not in sys.path, "'. should be removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_preserves_multiple_entries():
    """Test that modify_sys_path only affects the first item when it's not standard."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a custom path entry that should NOT be removed
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Add another entry that should be preserved
        sys.path.insert(1, "/another/path")
        
        # Call the function
        modify_sys_path()
        
        # Check that our custom path is still there (bug: it would be removed)
        assert custom_path in sys.path, f"Custom path {custom_path} was incorrectly removed"
        assert "/another/path" in sys.path, "Other paths should be preserved"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_with_pythonpath_start():
    """Test that modify_sys_path handles PYTHONPATH with colon at beginning correctly."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a custom path entry that should NOT be removed
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Set PYTHONPATH to have ':' prefix for special handling
        with patch.dict(os.environ, {'PYTHONPATH': ':/some/other/path'}):
            # Call the function
            modify_sys_path()
            
            # Check that our custom path is still there
            assert custom_path in sys.path, f"Custom path {custom_path} was incorrectly removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path