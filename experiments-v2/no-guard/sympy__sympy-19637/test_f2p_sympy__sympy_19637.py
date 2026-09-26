"""
Regression test for kernS UnboundLocalError bug.

The bug occurs when kernS is called with a string that contains no spaces.
In this case, the 'kern' variable is never defined but is still referenced
in the 'hit = kern in s' line.
"""

from sympy.core.sympify import kernS


def test_kernS_no_spaces():
    """Test that kernS doesn't raise UnboundLocalError with no spaces in input."""
    # This should not raise UnboundLocalError - the main bug case
    expr = kernS("(2*x)/(x-1)")
    # The result should be a valid sympy expression
    assert expr is not None