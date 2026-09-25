# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint removing first item from sys.path incorrectly."""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

import pytest


def test_modify_sys_path_removes_safe_entries():
    """Test that modify_sys_path removes safe entries like '', '.', and cwd from sys.path."""
    # Save original sys.path and restore it after test
    original_path = sys.path.copy()
    
    try:
        # Test case 1: sys.path starts with "" (empty string) - should be removed
        sys.path = ["", "/some/path", "/another/path"]
        # We test actual modify_sys_path function that was changed in this PR
        from pylint import modify_sys_path
        
        modify_sys_path()
        assert sys.path == ["/some/path", "/another/path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_preserves_custom_entries():
    """Test that modify_sys_path preserves non-standard entries in sys.path (the bug scenario)."""
    # Save original sys.path and restore it after test
    original_path = sys.path.copy()
    
    try:
        # In the bug report scenario: someone adds a custom module path to sys.path
        # This simulates a pylint extension adding paths for custom libraries 
        custom_path = "/custom/extension/path/added/by/extension"
        sys.path.insert(0, custom_path)  # This puts custom_path at beginning
        
        # The issue: before the fix, this would unconditionally pop sys.path[0]
        # So even if custom_path was a valid path that needed to be preserved,
        # pylint would remove it and break extension functionality
        
        from pylint import modify_sys_path
        modify_sys_path()
        
        # Before the fix this would fail - custom_path would be removed
        # After the fix this passes - custom_path should be preserved  
        assert sys.path[0] == custom_path, (
            f"Custom path {custom_path} was incorrectly removed from sys.path. " 
            f"Got: {sys.path[0]}"
        )
        
        # Also make sure it's still in the correct position
        assert custom_path in sys.path
        assert sys.path.index(custom_path) == 0
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_preserves_safe_entries_which_should_be_removed():
    """Test that safe entries are still removed as intended."""
    # Save original sys.path and restore it after test
    original_path = sys.path.copy()
    
    try:
        # Test legitimate cases that should be removed
        cwd = os.getcwd()
        
        # Test with empty string prefix
        sys.path = ["", "/some/path", "/another/path"]
        from pylint import modify_sys_path
        modify_sys_path()
        assert sys.path == ["/some/path", "/another/path"]
        
        # Test with current directory prefix (same case)
        sys.path = [cwd, "/some/path", "/another/path"]
        modify_sys_path()
        assert sys.path == ["/some/path", "/another/path"]
        
        # Verify python's "." (current dir) is also correctly removed
        sys.path = [".", "/some/path", "/another/path"]
        modify_sys_path()
        assert sys.path == ["/some/path", "/another/path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path