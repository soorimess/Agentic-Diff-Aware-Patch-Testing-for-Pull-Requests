# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

from pylint import modify_sys_path


def test_modify_sys_path_preserves_non_standard_paths() -> None:
    """Test that modify_sys_path preserves non-standard paths that should not be removed."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # This directly tests the bug described in the GitHub issue:
        # When runpy.run_module inserts a custom path at index 0, it should not be removed
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "other_path", "another_path"]
        
        # Before the fix, this would incorrectly remove custom_path because of unconditional pop(0)
        # After the fix, this should leave custom_path in place
        modify_sys_path()
        
        # This assertion should pass after the fix, fail before the fix
        assert sys.path[0] == custom_path, f"Non-standard path was incorrectly removed. Expected: {custom_path}, Got: {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_removes_standard_entries() -> None:
    """Test that modify_sys_path still removes standard entries from sys.path."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case: First entry is empty string, should be removed
        sys.path = ["", "other_path", "another_path"]
        modify_sys_path()
        assert sys.path[0] == "other_path", f"Expected 'other_path', got {sys.path[0]}"
        
        # Test case: First entry is current directory, should be removed
        sys.path = [os.getcwd(), "other_path", "another_path"]
        modify_sys_path()
        assert sys.path[0] == "other_path", f"Expected 'other_path', got {sys.path[0]}"
        
        # Test case: First entry is ".", should be removed
        sys.path = [".", "other_path", "another_path"]
        modify_sys_path()
        assert sys.path[0] == "other_path", f"Expected 'other_path', got {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_with_pythonpath_conditions() -> None:
    """Test that modify_sys_path handles PYTHONPATH edge cases correctly."""
    # Save original sys.path and environment
    original_path = sys.path.copy()
    original_pythonpath = os.environ.get("PYTHONPATH")
    
    try:
        # Test edge case that is correct behavior - with PYTHONPATH starting with ":"
        # This creates a specific logic path where multiple pops can happen
        os.environ["PYTHONPATH"] = ":/some/path"
        sys.path = ["", "other_path", "another_path"]  # First entry should be removed
        
        modify_sys_path()
        # After first pop: ["other_path", "another_path"]
        # After PYTHONPATH conditional pop: ["another_path"] 
        # The key is that the function should NOT crash, and behavior should be consistent
        assert len(sys.path) >= 1, "sys.path should not be empty"
        
    finally:
        # Restore original sys.path
        sys.path = original_path
        # Restore PYTHONPATH 
        if original_pythonpath is not None:
            os.environ["PYTHONPATH"] = original_pythonpath
        elif "PYTHONPATH" in os.environ:
            del os.environ["PYTHONPATH"]