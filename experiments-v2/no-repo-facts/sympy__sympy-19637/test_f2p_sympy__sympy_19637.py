"""
Test for the kernS UnboundLocalError bug.

This test reproduces the bug where kernS raises UnboundLocalError
when called with a string that contains parentheses but no spaces,
because the variable 'kern' is referenced before assignment.
"""

from sympy.core.sympify import kernS


def test_kernS_unboundlocalerror():
    """Test that kernS doesn't raise UnboundLocalError for strings without spaces."""
    # This specific case should trigger the bug:
    # - contains parentheses (so enters main logic)
    # - no spaces (so kern never gets defined)
    # - should not raise UnboundLocalError after fix
    text = "(2*x)/(x-1)"
    # This should not raise UnboundLocalError
    result = kernS(text)
    # The result should be the sympified expression
    assert result is not None


def test_kernS_with_spaces():
    """Test that kernS works normally with spaces."""
    # This case should work normally (has spaces)
    text = "2 * x"
    result = kernS(text)
    assert result is not None