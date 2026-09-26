"""
Regression test for kernS UnboundLocalError bug.

This test ensures that kernS doesn't raise UnboundLocalError when
called with expressions that don't contain spaces.
"""

from sympy.core.sympify import kernS


def test_kernS_unbound_local_error_regression():
    """Test that reproduces the exact case from the bug report."""
    # This is the exact case from the bug report that caused UnboundLocalError
    text = "(2*x)/(x-1)"
    
    # Before the fix, this would raise:
    # UnboundLocalError: local variable 'kern' referenced before assignment
    # After the fix, this should work normally
    result = kernS(text)
    
    # Verify we get a valid expression back (not None)
    assert result is not None


def test_kernS_with_spaces_still_works():
    """Ensure existing functionality with spaces still works."""
    # Test case with spaces to ensure we didn't break existing functionality
    text = "(2 * x) / (x - 1)"
    
    result = kernS(text)
    
    # Verify we get a valid expression back (not None)
    assert result is not None