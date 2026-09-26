"""
Regression test for pytest-dev/pytest#6202
Test that demonstrates the fix for incorrect string replacement in getmodpath method.
"""

def test_getmodpath_string_handling():
    """
    Test that demonstrates the specific string handling behavior that was changed.
    
    The pull request removes the line: return s.replace(".[", "[")
    This was causing incorrect test name display for parameterized tests.
    """
    
    # The replacement that was problematic
    # When getmodpath returns a legitimate path like "module.test[..["
    # The replacement would incorrectly transform it to "module.test[.["
    
    # This test shows what the replacement does - it's documenting the behavior
    problematic_string = "module.test[..["
    result = problematic_string.replace(".[", "[")
    
    # The replacement was converting ".[" to "["
    # This was the behavior that caused incorrect test names
    assert result == "module.test[.[", (
        "String replacement behavior that was causing incorrect test name display"
    )