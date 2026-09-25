"""Regression test for pylint bug where first sys.path item was always removed.

This test checks that modify_sys_path only removes the first entry from sys.path
when it's an empty string, '.', or the current working directory.
"""

import os
import sys
from pylint import modify_sys_path


def test_modify_sys_path_preserves_non_special_paths():
    """Test that modify_sys_path preserves custom paths that are not special."""
    # Store original sys.path 
    original_sys_path = sys.path.copy()
    
    try:
        # Add custom path entry - this should NOT be removed by modify_sys_path
        custom_path = "/some/custom/path"  
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path - this should NOT remove our custom path 
        modify_sys_path()
        
        # Verify that our custom path is still there (this would fail in buggy version)
        # We assert that custom path is still at index 0
        assert sys.path[0] == custom_path, f"Custom path {custom_path} should not be removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path


def test_modify_sys_path_removes_empty_string():
    """Test that empty string entries are removed."""  
    # Store original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Add empty string to beginning - this SHOULD be removed
        sys.path.insert(0, "")
        
        # Call modify_sys_path - this SHOULD remove the empty string
        modify_sys_path()
        
        # Verify that empty string was removed
        assert sys.path[0] != "", "Empty string should have been removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path


def test_modify_sys_path_removes_current_dir():
    """Test that current directory entries are removed."""  
    # Store original sys.path  
    original_sys_path = sys.path.copy()
    
    try:
        # Add current directory to beginning - this SHOULD be removed
        sys.path.insert(0, ".")
        
        # Call modify_sys_path - this SHOULD remove the "." path
        modify_sys_path()
        
        # Verify that "." was removed
        assert sys.path[0] != ".", "Current directory '.' should have been removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path


def test_modify_sys_path_removes_cwd():
    """Test that current working directory entries are removed when added."""
    # Store original sys.path
    original_sys_path = sys.path.copy() 
    
    try:
        # Get the current working directory and ensure it's added to the front  
        cwd = os.getcwd()
        
        # Because regular Python will have cwd already in sys.path, we first remove it then add it again
        # to make a clean environment for testing.
        try:
            # First, ensure current directory is not at front (remove if needed)
            if sys.path[0] == cwd:
                sys.path.pop(0)
        except IndexError:
            pass
            
        # Add cwd to beginning - this SHOULD be removed  
        sys.path.insert(0, cwd)
        
        # Call modify_sys_path - this SHOULD remove our cwd path
        modify_sys_path()
        
        # Verify that cwd was removed (it's not at index 0 anymore)
        assert sys.path[0] != cwd, f"CWD {cwd} should have been removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_sys_path