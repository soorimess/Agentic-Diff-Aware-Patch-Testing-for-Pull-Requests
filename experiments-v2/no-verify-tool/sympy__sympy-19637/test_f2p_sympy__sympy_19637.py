"""
Test for kernS bug where 'kern' is referenced before assignment.

This test reproduces the UnboundLocalError that occurs when kernS
is called with a string that contains no spaces, causing the kern
variable to be undefined when hit = kern in s is executed.
"""

from sympy.core.sympify import kernS


def test_kernS_no_spaces_does_not_raise_unboundlocalerror():
    """Test that kernS with no spaces in string does not raise UnboundLocalError."""
    # This string has no spaces, so the 'if " " in s:' block is skipped
    # but hit = kern in s is still executed, causing UnboundLocalError
    text = "(2*x)/(x-1)"
    # This should not raise UnboundLocalError - the bug we're testing for
    result = kernS(text)
    # If we get here without exception, the function worked
    assert result is not None


def test_kernS_with_spaces_works_normally():
    """Test that kernS with spaces works normally."""
    # This string has spaces, so kern variable should be defined
    text = "(2 * x) / (x - 1)"
    # This should work normally
    result = kernS(text)
    assert result is not None