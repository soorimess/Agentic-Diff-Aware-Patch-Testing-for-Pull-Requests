"""Test that verifies the fix for pylint removing first item from sys.path when running from runpy."""

import os
import sys
from unittest import mock

import pytest

# We'll import pylint to test the modify_sys_path function
import pylint
from pylint import modify_sys_path


def test_modify_sys_path_removes_path_when_first_item_is_empty_string():
    """Test that modify_sys_path removes first item when it's empty string (normal case)."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Set up sys.path with empty string as first item (normal case)
        sys.path = ["", "other_path"]
        
        # Call modify_sys_path
        modify_sys_path()
        
        # Verify empty string was removed  
        assert sys.path == ["other_path"]
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_removes_path_when_first_item_is_dot():
    """Test that modify_sys_path removes first item when it's single dot."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Set up sys.path with "." as first item
        sys.path = [".", "other_path"]
        
        # Call modify_sys_path
        modify_sys_path()
        
        # Verify "." was removed
        assert sys.path == ["other_path"]
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_removes_path_when_first_item_is_cwd():
    """Test that modify_sys_path removes first item when it's current working directory."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        cwd = os.getcwd()
        # Set up sys.path with current working directory as first item
        sys.path = [cwd, "other_path"]
        
        # Call modify_sys_path
        modify_sys_path()
        
        # Verify cwd was removed
        assert sys.path == ["other_path"]
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_does_not_remove_custom_path_when_first_item_is_custom_path():
    """Test that modify_sys_path does NOT remove first item when it's a custom path (the bug fix). 
       
       This test specifically addresses the root cause: when a user adds a custom path 
       to sys.path and then runs pylint (e.g., via runpy), that custom path should 
       not be removed unexpectedly."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Set up sys.path where the first item is a completely custom, user-added path
        custom_path = "/some/custom/path/that/should/not/be/removed"
        sys.path = [custom_path, "other_path"]
        
        # Capture the original path for verification before modifying
        original_first_path = sys.path[0]
        
        # Call modify_sys_path - this simulates what happens with `runpy.run_module`
        modify_sys_path()
        
        # The bug fix: custom paths should NOT be removed
        # If they were removed, the path would be truncated
        assert sys.path[0] == original_first_path, f"First path item was unexpectedly removed. Expected: {original_first_path}, Got: {sys.path[0] if sys.path else 'empty'}"
        assert len(sys.path) == 2, f"Expected 2 paths, got {len(sys.path)} - path was unexpectedly modified."
        assert sys.path[0] == custom_path, "Custom path was unexpectedly removed from sys.path"
        
    finally:
        # Restore original sys.path
        sys.path = original_path


def test_modify_sys_path_behavior_with_runpy_scenario():
    """Test scenario from bug report: custom paths added by user get removed by pylint.
    
    When runpy runs pylint, it adds the current directory to sys.path (as first item), 
    but then pylint removes it unless it's "", ".", or os.getcwd()."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        original_cwd = os.getcwd()
        
        # This simulates what happens when user code does:
        # sys.path.insert(0, "something") 
        # and then runpy.run_module('pylint', run_name="__main__", alter_sys=True)
        custom_path = "something"
        sys.path.insert(0, custom_path)
        
        # Ensure it was properly added
        assert sys.path[0] == custom_path, f"Expected {custom_path} to be first path, got {sys.path[0] if sys.path else 'empty'}"
        
        # Capture the current first item before modification
        first_item_before = sys.path[0]
        
        # Call modify_sys_path - this simulates runpy running pylint
        modify_sys_path()
        
        # The assertion; this was the bug - old behavior would remove custom_path
        # But the fix should preserve it
        assert sys.path[0] == first_item_before, f"Custom path was removed. Original: {first_item_before}, After modify_sys_path: {sys.path[0] if sys.path else 'empty'}"
        assert sys.path[0] == custom_path, "The user-added custom path should not be removed by pylint"
        
    finally:
        # Restore original sys.path  
        sys.path = original_path