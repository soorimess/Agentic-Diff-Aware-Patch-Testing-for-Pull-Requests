"""
Regression test for kernS UnboundLocalError bug.

The bug happens when kernS is called with a string that does not contain spaces.
In this case, the variable 'kern' is never initialized, but is later referenced
in the 'hit = kern in s' line.
"""

from sympy.core.sympify import kernS


def test_kernS_unbound_local_error():
    """Test that kernS doesn't raise UnboundLocalError for strings without spaces."""
    # This is the exact case from the bug report that caused UnboundLocalError
    text = "(2*x)/(x-1)"
    # Before the fix, this would raise UnboundLocalError: local variable 'kern' referenced before assignment
    # After the fix, this should work normally  
    try:
        result = kernS(text)
        # If we get here without exception, it's working correctly
        assert True  # Test passes if no exception raised
    except UnboundLocalError as e:
        if "kern" in str(e):
            raise AssertionError("UnboundLocalError still occurs: " + str(e))
        else:
            raise  # Re-raise if it's a different UnboundLocalError


def test_kernS_with_spaces():
    """Test that kernS still works correctly with spaces (which goes through the moved line)."""
    # Test with spaces - this should work both before and after fix 
    # and will exercise the fixed `hit = kern in s` path
    text = "(2*x) / (x-1)"
    try:
        result = kernS(text)
        # If we get here without exception, it's working correctly
        assert True  # Test passes if no exception raised
    except UnboundLocalError as e:
        if "kern" in str(e):
            raise AssertionError("UnboundLocalError still occurs: " + str(e))
        else:
            raise  # Re-raise if it's a different UnboundLocalError


def test_kernS_edge_cases():
    """Test various edge cases that could cause kern variable issues."""
    # These strings don't contain spaces but could potentially 
    # cause issues if kern gets defined in some paths
    test_cases = [
        "x",
        "x+y", 
        "x*y",
        "x**2",
        "(x+1)",
        "sin(x)",
        "log(x+1)",
        "sqrt(x)",
        "1",
        "2.5",
    ]
    
    for text in test_cases:
        # These should not raise UnboundLocalError
        try:
            result = kernS(text)
            # If we get here without exception, it's working correctly
            assert True  # Test passes if no exception raised
        except UnboundLocalError as e:
            if "kern" in str(e):
                raise AssertionError(f"UnboundLocalError still occurs for {text}: {e}")
            else:
                raise  # Re-raise if it's a different UnboundLocalError