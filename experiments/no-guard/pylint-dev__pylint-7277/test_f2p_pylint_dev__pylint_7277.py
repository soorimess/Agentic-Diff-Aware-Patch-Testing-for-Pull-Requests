# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint issue with sys.path modification."""

import os
import sys
from pathlib import Path

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_removes_safe_paths():
    """Test that modify_sys_path removes safe paths (empty string, dot, or cwd)."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Test case 1: First path is an empty string (should be removed)
        sys.path = ["", "other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["other_path", "another_path"]
        
        # Test case 2: First path is a dot (should be removed)  
        sys.path = [".", "other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["other_path", "another_path"]
        
        # Test case 3: First path is current working directory (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "other_path", "another_path"]
        modify_sys_path()
        assert sys.path == ["other_path", "another_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_preserves_unsafe_paths():
    """Test that modify_sys_path preserves unsafe paths (not empty string, dot, or cwd)."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Test case: First path is a custom path (should not be removed)
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "other_path", "another_path"]
        modify_sys_path()
        # Before fix: this would remove custom_path incorrectly
        # After fix: this should preserve custom_path
        assert sys.path == [custom_path, "other_path", "another_path"]
        
        # Test case: First path is a custom path with subdirectories
        custom_path2 = "/usr/local/lib/python3.9/site-packages"
        sys.path = [custom_path2, "other_path", "another_path"]
        modify_sys_path()
        assert sys.path == [custom_path2, "other_path", "another_path"]
        
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the specific scenario reported in the bug - runpy usage."""
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Simulate the scenario from the bug report:
        # When using runpy.run_module, sys.path gets modified
        # The first item in the path after runpy usage might be a custom path
        custom_path = "something"  # This is from the bug report example
        sys.path.insert(0, custom_path)
        
        # Ensure we don't have the benign paths that should get removed
        # If we did, it would interfere with our test
        # We'll test what happens when runpy.adds paths, and the first one 
        # is not a safe one
        
        original_length = len(sys.path)
        modify_sys_path()
        
        # Before fix: the custom_path would be incorrectly removed
        # After fix: the custom_path should be preserved
        assert len(sys.path) == original_length, "Length should not change when first path is not safe"
        assert sys.path[0] == custom_path, "Custom path should not be removed when it's not safe"
        
    finally:
        # Restore original sys.path
        sys.path = original_sys_path