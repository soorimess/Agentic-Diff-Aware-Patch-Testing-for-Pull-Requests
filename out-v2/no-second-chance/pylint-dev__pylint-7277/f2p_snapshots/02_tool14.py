# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for pylint bug where first item from sys.path is removed incorrectly."""

import os
import sys
from unittest.mock import patch

from pylint import modify_sys_path


def test_modify_sys_path_preserves_custom_paths():
    """Test that modify_sys_path preserves custom paths at the beginning of sys.path.
    
    This is a regression test for the bug where pylint would remove the first
    item from sys.path regardless of what it was, causing issues when extensions
    add custom paths to sys.path.
    """
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a custom path at the beginning (this should NOT be removed)
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        
        # Call modify_sys_path
        modify_sys_path()
        
        # The custom path should still be there
        assert sys.path[0] == custom_path, f"Expected {custom_path} at start of sys.path, got {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_empty_path():
    """Test that modify_sys_path still removes empty path when it's at the beginning."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add empty path at the beginning (this SHOULD be removed)
        sys.path.insert(0, "")
        
        # Call modify_sys_path
        modify_sys_path()
        
        # Empty path should be removed
        assert sys.path[0] != "", "Empty path should have been removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_current_dir():
    """Test that modify_sys_path still removes current directory when it's at the beginning."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add current directory at the beginning (this SHOULD be removed)
        current_dir = os.getcwd()
        sys.path.insert(0, current_dir)
        
        # Call modify_sys_path
        modify_sys_path()
        
        # Current directory should be removed
        assert sys.path[0] != current_dir, "Current directory should have been removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_removes_dot():
    """Test that modify_sys_path still removes '.' when it's at the beginning."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add '.' at the beginning (this SHOULD be removed)
        sys.path.insert(0, ".")
        
        # Call modify_sys_path
        modify_sys_path()
        
        # '.' should be removed
        assert sys.path[0] != ".", "Dot should have been removed"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path


def test_modify_sys_path_preserves_non_standard_path():
    """Test that modify_sys_path preserves non-standard paths that are not '', '.', or cwd."""
    # Save original sys.path
    original_path = sys.path.copy()
    
    try:
        # Add a path that's not empty, not '.', not cwd
        # Use a path that's definitely not the current working directory
        test_path = "/tmp/some_test_path"
        sys.path.insert(0, test_path)
        
        # Call modify_sys_path
        modify_sys_path()
        
        # The test path should still be there
        assert sys.path[0] == test_path, f"Expected {test_path} at start of sys.path, got {sys.path[0]}"
        
    finally:
        # Restore original sys.path
        sys.path[:] = original_path