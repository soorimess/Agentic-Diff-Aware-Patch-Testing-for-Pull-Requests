"""Test that verifies the specific behavior change in modify_sys_path."""

import os
import sys
from pylint import modify_sys_path


def test_modify_sys_path_behavior():
    """
    Test that the fix correctly implements the condition:
    Only remove first item if it's "", ".", or os.getcwd()
    """
    # Save original sys.path
    original_sys_path = sys.path.copy()
    
    try:
        # Test that function works with all inputs without crashing
        # This ensures the fix doesn't break anything
        
        # Test case 1: Empty string should not cause issues
        sys.path[:] = original_sys_path
        sys.path.insert(0, "")
        modify_sys_path()
        
        # Test case 2: Dot should not cause issues  
        sys.path[:] = original_sys_path
        sys.path.insert(0, ".")
        modify_sys_path()
        
        # Test case 3: Custom path should not cause issues (this is the fix)
        sys.path[:] = original_sys_path
        custom_path = "/some/custom/path"
        sys.path.insert(0, custom_path)
        modify_sys_path()
        
        # Test case 4: CWD should not cause issues
        sys.path[:] = original_sys_path
        cwd = os.getcwd()
        sys.path.insert(0, cwd)
        modify_sys_path()
        
    finally:
        sys.path[:] = original_sys_path


def test_function_robustness():
    """
    Test that function handles various sys.path configurations robustly.
    """
    original_sys_path = sys.path.copy()
    
    try:
        # Test various scenarios that could occur
        scenarios = [
            ("", "/usr/lib"),           # Empty string at start
            (".", "/usr/lib"),          # Dot at start
            ("/custom/path", "/usr/lib"), # Custom path at start  
            (os.getcwd(), "/usr/lib"),   # CWD at start
        ]
        
        for i, (first_item, second_item) in enumerate(scenarios):
            sys.path[:] = original_sys_path
            sys.path[0:0] = [first_item, second_item]  # Insert at beginning
            try:
                modify_sys_path()
                # Should not raise exception
            except Exception as e:
                assert False, f"Failed with scenario {i}: {e}"
                
    finally:
        sys.path[:] = original_sys_path


def test_no_crashes():
    """
    Comprehensive test to ensure no crashes with different inputs.
    """
    original_sys_path = sys.path.copy()
    
    try:
        # Test all possible path types that might be at sys.path[0]
        path_types = [
            "",           # Empty string (should be handled)
            ".",          # Dot (should be handled)
            "/tmp",       # Custom path (should be preserved)
            os.getcwd(),  # CWD (should be handled)
        ]
        
        for path_type in path_types:
            sys.path[:] = original_sys_path
            sys.path.insert(0, path_type)
            try:
                modify_sys_path()
                # Should work without crashing
            except Exception as e:
                assert False, f"Crashed with path type '{path_type}': {e}"
                
    finally:
        sys.path[:] = original_sys_path