# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the sys.path modification behavior fix.

This test ensures the fix for the bug where pylint incorrectly removed
the first item from sys.path regardless of whether it was safe to do so.
"""

import os
import sys

from pylint import modify_sys_path


def test_modify_sys_path_removes_empty_string():
    """Test that modify_sys_path removes empty string from beginning of sys.path."""
    original_sys_path = sys.path[:]
    
    try:
        # Set up sys.path with empty string at the beginning
        sys.path = ["", "some", "other", "paths"]
        
        # Call the function
        modify_sys_path()
        
        # Check that empty string was removed
        assert sys.path == ["some", "other", "paths"]
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_removes_dot():
    """Test that modify_sys_path removes '.' from beginning of sys.path."""
    original_sys_path = sys.path[:]
    
    try:
        # Set up sys.path with '.' at the beginning
        sys.path = [".", "some", "other", "paths"]
        
        # Call the function
        modify_sys_path()
        
        # Check that '.' was removed
        assert sys.path == ["some", "other", "paths"]
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_removes_cwd():
    """Test that modify_sys_path removes current working directory from beginning of sys.path."""
    original_sys_path = sys.path[:]
    cwd = os.getcwd()
    
    try:
        # Set up sys.path with cwd at the beginning
        sys.path = [cwd, "some", "other", "paths"]
        
        # Call the function
        modify_sys_path()
        
        # Check that cwd was removed
        assert sys.path == ["some", "other", "paths"]
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_preserves_custom_path():
    """Test that modify_sys_path preserves custom paths from beginning of sys.path.
    
    This is the main bug fix: in the original code any first item was removed,
    but now it should only remove "", ".", or cwd.
    """
    original_sys_path = sys.path[:]
    
    try:
        # Set up sys.path with custom path at the beginning (this is the bug case)
        custom_path = "/some/custom/path"
        sys.path = [custom_path, "some", "other", "paths"]
        
        # Call the function
        modify_sys_path()
        
        # Check that custom path was NOT removed (this is the fix)
        # In the buggy version: ["some", "other", "paths"] (custom_path removed)
        # In the fixed version: ["/some/custom/path", "some", "other", "paths"] (custom_path preserved)
        assert sys.path[0] == custom_path
        assert len(sys.path) == 4  # Should keep all 4 elements
    finally:
        # Restore original sys.path
        sys.path = original_sys_path


def test_modify_sys_path_preserves_custom_path_simple():
    """Simplified version of the custom path test to clearly show the bug."""
    original_sys_path = sys.path[:]
    
    try:
        # Set up sys.path with custom path at the beginning (this is the bug case)
        custom_path = "/some/custom/path"
        sys.path = [custom_path]
        
        # Call the function
        modify_sys_path()
        
        # In the buggy version this would be [], in the fixed version it should be ["/some/custom/path"]
        assert sys.path == [custom_path]
    finally:
        # Restore original sys.path
        sys.path = original_sys_path