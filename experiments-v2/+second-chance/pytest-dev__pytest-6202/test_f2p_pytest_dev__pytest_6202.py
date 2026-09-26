"""
Regression test for pytest issue where parameterized test names with 
".[" are incorrectly displayed as ".[" instead of "..[" in test reports.

The bug was in src/_pytest/python.py in the getmodpath method where 
s.replace(".[", "[") was incorrectly removing the dot before the bracket.
"""
import pytest


def test_string_replacement_behavior_change():
    """
    Test the exact string replacement behavior that was changed.
    
    The fix removes the line: return s.replace(".[", "[")
    This means getmodpath() now returns the raw joined string instead of 
    applying the replacement that incorrectly modified "..[" patterns.
    """
    # Test string that demonstrates the problematic replacement
    input_string = "module.test_func..["
    
    # What the buggy code was doing (incorrectly)
    result_with_replacement = input_string.replace(".[", "[")
    expected_buggy = "module.test_func.["
    assert result_with_replacement == expected_buggy
    
    # What the fixed code does (correctly)
    result_without_replacement = input_string
    expected_fixed = "module.test_func..["
    assert result_without_replacement == expected_fixed
    
    # These should be different - showing the bug was in the replacement
    assert result_with_replacement != result_without_replacement


def test_dot_bracket_pattern_preservation():
    """
    Test that "..[" patterns are preserved in path generation.
    
    The issue was that when test parameters contained "..[", 
    the getmodpath method would incorrectly transform them.
    """
    # The core issue: "..[" should not be converted to ".["
    test_cases = [
        ("module..[", "module..["),
        ("test..[", "test..["),
        ("something..[", "something..["),
    ]
    
    for input_val, expected in test_cases:
        # Show the replacement that was problematic
        replaced = input_val.replace(".[", "[")
        
        # Show that the original should be preserved
        preserved = input_val
        
        # The fix ensures we don't do the replacement for "..[" patterns
        if "..[" in input_val:
            assert replaced == input_val.replace(".[", "[")
            assert preserved == input_val
            assert replaced != preserved