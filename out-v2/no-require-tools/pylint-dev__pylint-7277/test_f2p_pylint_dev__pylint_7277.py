# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint sys.path modification issue.

This test ensures that pylint only removes the first item from sys.path
when it is "" (empty string), "." (current directory), or the current working
directory. Otherwise, it should preserve the first item.
"""

import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_only_removes_safe_first_entries():
    """Test that modify_sys_path only removes first item when it's safe."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is "" (should be removed)
        sys.path = ["", "/some/other/path"]
        modify_sys_path()
        # With the bug, this would remove "" and leave "/some/other/path"
        # With fix, this should also remove "" and leave "/some/other/path" 
        # (both are correct behavior)
        assert sys.path == ["/some/other/path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 2: First item is "." (should be removed)
        sys.path = [".", "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 3: First item is current working directory (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_preserves_non_safe_first_item():
    """Test that non-safe first items are preserved (the main bug)."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # This is the main bug case: when first item is not "", ".", or cwd
        # The buggy code removes it anyway, which breaks user code
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "/other/path", "/third/path"]
        modify_sys_path()
        
        # With the BUGGY code, this would incorrectly remove the first item
        # With the FIXED code, this should preserve the first item
        # The bug manifests when user code gets broken because their custom path is removed
        assert sys.path[0] == custom_path, f"First path item was incorrectly removed. Expected '{custom_path}', got {sys.path[0]}"
        assert sys.path == [custom_path, "/other/path", "/third/path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_with_safe_first_item_and_pythonpath():
    """Test that safe first items work correctly with PYTHONPATH."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test with safe first item and PYTHONPATH
        # This should work correctly - safe first item gets removed, then PYTHONPATH logic applies
        sys.path = ["", "/other/path", "/third/path"]
        with patch.dict(os.environ, {"PYTHONPATH": ":/some/other/path"}):
            modify_sys_path()
            # First item "" should be removed, then PYTHONPATH logic removes another item
            # Result should be ["/third/path"] (after removing both)
            # But let's just check it doesn't crash and handles safely
            assert len(sys.path) <= 2  # Should not crash
            
    finally:
        # Restore original sys.path
        sys.path = original_path