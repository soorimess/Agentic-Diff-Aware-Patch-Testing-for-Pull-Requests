"""
Regression test for kernS bug where 'kern' is referenced before assignment.

This test should fail on the buggy code and pass on the fixed code.
"""
from sympy.core.sympify import kernS

def test_kernS_unbound_local_error():
    """Test that kernS doesn't raise UnboundLocalError when there are no spaces."""
    # This specific input should trigger the bug in the original code
    # The bug occurs when there are parentheses but no spaces in the string
    # so the 'if " " in s:' block doesn't execute, but kern is referenced later
    text = "(2*x)/(x-1)"
    # This should not raise UnboundLocalError: local variable 'kern' referenced before assignment
    result = kernS(text)
    # Just verify it returns a valid expression
    assert result is not None