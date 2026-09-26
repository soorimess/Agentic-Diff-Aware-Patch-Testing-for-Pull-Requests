# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the sys.path modification behavior in pylint."""

import os
import sys

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_custom_path_not_removed():
    """Test that custom paths at the beginning of sys.path are not removed."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Create a clean sys.path with a custom path at the beginning
        # This simulates the bug scenario: a path added by an extension or runpy
        custom_path = "/this/is/a/custom/path/that/should/not/be/removed"
        
        # Clear sys.path and add our custom path first
        sys.path.clear()
        sys.path.append(custom_path)
        sys.path.append("/some/other/path")
        
        # Call modify_sys_path - this should NOT remove our custom path
        modify_sys_path()
        
        # Check that our custom path is still there (this fails in the buggy version)
        assert sys.path[0] == custom_path, f"Expected {custom_path} at start of sys.path, got {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path