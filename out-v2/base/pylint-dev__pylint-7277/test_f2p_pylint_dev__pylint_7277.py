# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for the bug where pylint removes first item from sys.path when running from runpy."""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_removes_safe_paths():
    """Test that modify_sys_path removes safe paths (empty string, dot, or cwd)."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test with empty string as first path (should be removed)
        sys.path = ["", "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"], "Empty string path should be removed"
        
        # Test with dot as first path (should be removed)
        sys.path = [".", "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"], "Dot path should be removed"
        
        # Test with cwd as first path (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"], "CWD path should be removed"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_preserves_unsafe_paths():
    """Test that modify_sys_path preserves unsafe paths that are not empty, dot, or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test with custom path as first path (should NOT be removed)
        custom_path = "/custom/path/that/should/not/be/removed"
        sys.path = [custom_path, "/some/other/path"]
        modify_sys_path()
        assert sys.path == [custom_path, "/some/other/path"], "Custom path should be preserved"
        
        # Test with another custom path
        custom_path2 = "/another/custom/path"
        sys.path = [custom_path2, "/some/other/path"]
        modify_sys_path()
        assert sys.path == [custom_path2, "/some/other/path"], "Another custom path should be preserved"
        
        # Test with a path that looks like a module path but isn't safe
        module_path = "/some/module/path"
        sys.path = [module_path, "/some/other/path"]
        modify_sys_path()
        assert sys.path == [module_path, "/some/other/path"], "Module path should be preserved"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_preserves_paths_when_running_from_runpy():
    """Test the specific bug case: when running from runpy, custom paths should be preserved."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate the runpy scenario: sys.path has a custom path as first item
        # This is the exact scenario from the bug report
        custom_path = "/some/custom/path/added/by/extension"
        sys.path = [custom_path, "/usr/lib/python3.8", "/usr/local/lib/python3.8"]
        
        # This should NOT remove the custom path
        modify_sys_path()
        assert sys.path[0] == custom_path, "Custom path from runpy should be preserved"
        assert len(sys.path) == 3, "All paths should be preserved"
        
    finally:
        # Restore original sys.path
        sys.path = original_path