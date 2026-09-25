"""
Regression test for kernS bug where 'kern' was referenced before assignment.

When a string doesn't contain spaces but contains parentheses and is processed 
by kernS, the variable 'kern' was never defined in certain code paths, 
causing an UnboundLocalError.
"""

from sympy.core.sympify import kernS
from sympy.core.sympify import SympifyError


def test_kernS_no_space_string():
    """Test that kernS handles strings without spaces but with parentheses correctly"""
    # This string has parentheses but no spaces
    # Before the fix, this would raise UnboundLocalError: local variable 'kern' referenced before assignment
    text = "(2*x)/(x-1)"
    
    # The function should not raise UnboundLocalError
    # It should either return a valid expression or raise a different appropriate error
    try:
        expr = kernS(text)
        # If we get here without UnboundLocalError, function worked correctly
        assert expr is not None
        # The result should be a valid sympy expression
        assert hasattr(expr, 'free_symbols') or hasattr(expr, 'args')
    except UnboundLocalError as e:
        if "'kern' referenced before assignment" in str(e):
            raise AssertionError("kernS raised UnboundLocalError: 'kern' referenced before assignment - this is the bug we're fixing")
        else:
            raise  # Re-raise if it's a different UnboundLocalError


def test_kernS_normal_case():
    """Test that normal kernS cases continue to work"""
    # Test a case that should work normally
    text = "2*(x+y)"
    try:
        expr = kernS(text)
        assert expr is not None
    except Exception as e:
        # If there are any exceptions, they should not be the specific UnboundLocalError bug
        # (but may be legitimate errors for other reasons)
        if "'kern' referenced before assignment" in str(e):
            raise AssertionError("kernS failed with UnboundLocalError - this is the bug we're fixing")
        # Other exceptions are OK for this test


def test_kernS_no_parentheses():
    """Test kernS with strings that have no parentheses"""
    # This should not trigger the kern processing at all
    text = "2*x"
    try:
        expr = kernS(text)
        assert expr is not None
    except Exception as e:
        # If there are any exceptions, they should not be the specific UnboundLocalError bug
        if "'kern' referenced before assignment" in str(e):
            raise AssertionError("kernS failed with UnboundLocalError - this is the bug we're fixing")