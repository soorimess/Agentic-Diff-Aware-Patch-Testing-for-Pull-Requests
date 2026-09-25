"""
Regression test for issue #7277:
pylint removes first item from sys.path when running from runpy.

This test ensures that pylint only removes the first item from sys.path
when it's safe to do so (i.e., when it's "", ".", or os.getcwd()).
"""
# pylint: disable=protected-access,missing-function-docstring

import os
import sys
from unittest import mock

import pytest

from pylint import modify_sys_path


def test_modify_sys_path_safe_entries_removed():
    """Test that modify_sys_path removes safe entries like '', '.', and cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case 1: Empty string as first entry (should be removed)
        sys.path = ["", "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 2: Current directory as first entry (should be removed)
        cwd = os.getcwd()
        sys.path = [cwd, "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"]
        
        # Reset path
        sys.path = original_path
        
        # Test case 3: "." as first entry (should be removed)
        sys.path = [".", "/some/other/path"]
        modify_sys_path()
        assert sys.path == ["/some/other/path"]
        
    finally:
        # Restore original path
        sys.path = original_path


def test_modify_sys_path_unsafe_entries_preserved():
    """Test that modify_sys_path preserves unsafe entries that shouldn't be removed."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test case: Custom path that shouldn't be removed (this is the bug scenario)
        custom_path = "/this/is/a/custom/path"
        sys.path = [custom_path, "/some/other/path"]
        modify_sys_path()
        # This should now NOT remove the custom path since it's not a safe entry
        # BEFORE the fix, this would have failed because it would remove any first entry
        assert sys.path == [custom_path, "/some/other/path"]
        
    finally:
        # Restore original path
        sys.path = original_path


def test_modify_sys_path_with_runpy_simulation():
    """Test simulating the exact scenario from bug report."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Simulate what happens in runpy scenario:
        # Some user code added to sys.path, then pylint modifies it
        custom_path = "/custom/user/path"  # This gets added by user code
        cwd = os.getcwd() 
        
        # This arrangement simulates runpy.run_module with alter_sys=True 
        # where a custom path gets first in sys.path
        sys.path = [custom_path, cwd, "/some/other/path"]
        
        modify_sys_path()
        
        # The custom path should be preserved - This tests the core bug
        # Before fix: custom_path would get removed by the blind pop(0)
        # After fix: custom_path should be preserved 
        assert sys.path[0] == custom_path  # Should preserve custom path
        # The cwd should still be there in the right place
        assert sys.path[1] == cwd  
        assert "/some/other/path" in sys.path
        
    finally:
        # Restore original path
        sys.path = original_path


def test_modify_sys_path_preserves_first_safe_entry():
    """Test that when first entry IS safe, it gets removed correctly."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Test a case where first entry is safe (empty string)
        sys.path = ["", "/some/other/path"]
        modify_sys_path()
        # Should remove the empty string entry
        assert sys.path == ["/some/other/path"]
        
    finally:
        # Restore original path
        sys.path = original_path