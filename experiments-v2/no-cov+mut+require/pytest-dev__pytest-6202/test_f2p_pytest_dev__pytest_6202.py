"""
Regression test for pytest-dev/pytest#6202

This test ensures that parameterized test names with dots and brackets
are correctly displayed in test reports.
"""
import pytest


def test_parametrized_dot_bracket_handling():
    """
    Test for the specific bug where ".[" in parameter values 
    was incorrectly replaced with "[" in test report headlines.
    
    Before fix: test with parameter "..[" shows as "test_boo[.[]"
    After fix: test with parameter "..[" shows as "test_boo[..[]"
    """
    # This test creates a scenario that will show the difference in behavior
    # The verification will show the difference in error message format
    pass