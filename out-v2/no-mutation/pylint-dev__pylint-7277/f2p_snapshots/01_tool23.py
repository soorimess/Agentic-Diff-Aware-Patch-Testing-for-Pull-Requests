# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

from __future__ import annotations

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_only_removes_safe_first_items():
    """Test that modify_sys_path only removes first item when it's safe ("" or "." or cwd)."""
    
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: First item is a custom path (should NOT be removed in the buggy version)
        # But after fix, it should NOT be removed at all
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "/some/other/path", "/another/path"]
        modify_sys_path()
        # After fix, this should NOT remove the first item
        # The first item should still be the custom path
        assert sys.path[0] == custom_path, f"Expected '{custom_path}' but got {sys.path[0]}"
        assert len(sys.path) == 3, f"Expected 3 items, got {len(sys.path)}"
        
        # Reset path
        sys.path = original_path.copy()
        
        # Test case 2: First item is "" (should be removed)
        sys.path = ["", "/some/other/path", "/another/path"]
        modify_sys_path()
        assert sys.path[0] == "/some/other/path", f"Expected '/some/other/path' but got {sys.path[0]}"
        assert len(sys.path) == 2, f"Expected 2 items, got {len(sys.path)}"
        
        # Reset path
        sys.path = original_path.copy()
        
        # Test case 3: First item is "." (should be removed)
        sys.path = [".", "/some/other/path", "/another/path"]
        modify_sys_path()
        assert sys.path[0] == "/some/other/path", f"Expected '/some/other/path' but got {sys.path[0]}"
        assert len(sys.path) == 2, f"Expected 2 items, got {len(sys.path)}"
        
        # Reset path
        sys.path = original_path.copy()
        
        # Test case 4: First item is current working directory (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "/some/other/path", "/another/path"]
        modify_sys_path()
        assert sys.path[0] == "/some/other/path", f"Expected '/some/other/path' but got {sys.path[0]}"
        assert len(sys.path) == 2, f"Expected 2 items, got {len(sys.path)}"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_with_runpy_scenario():
    """Test the specific scenario from the bug report: runpy usage."""
    
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate the scenario from the bug report:
        # sys.path.insert(0, "something")
        # runpy.run_module('pylint', run_name="__main__", alter_sys=True)
        custom_path = "something"
        sys.path.insert(0, custom_path)
        
        # This should NOT remove the custom path we inserted
        modify_sys_path()
        
        # The custom path should still be in sys.path (not removed)
        # This is the bug: it was removing it even though it shouldn't
        assert custom_path in sys.path, f"Custom path '{custom_path}' was incorrectly removed from sys.path"
        
        # The original working directory should still be there if it was there
        # and should be removed if it was the first item
        if "" in sys.path:
            # "" should be removed if it was first
            assert sys.path[0] != "", "Empty string should be removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path = original_path