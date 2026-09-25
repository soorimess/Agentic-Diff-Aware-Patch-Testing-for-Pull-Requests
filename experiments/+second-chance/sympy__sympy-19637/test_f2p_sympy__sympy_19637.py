"""
Test for kernS UnboundLocalError bug fix.
This tests that kernS doesn't raise UnboundLocalError for strings without spaces.
"""

from sympy.core.sympify import kernS


def test_kernS_no_space_no_unboundlocalerror():
    """
    Test that kernS doesn't raise UnboundLocalError when there are no spaces in string.
    This was a bug where 'kern' was referenced before assignment.
    """
    # This string has no spaces, which triggered the UnboundLocalError 
    # in the old buggy implementation
    text = "(2*x)/(x-1)"
    
    # This should not raise UnboundLocalError
    expr = kernS(text)
    
    # Verify it produces a valid expression
    assert expr is not None


def test_kernS_with_space_no_unboundlocalerror():
    """
    Test that kernS doesn't raise UnboundLocalError when there ARE spaces in string.
    This ensures we don't break the original working code path.
    """
    # This string has spaces, so the kern logic should be used 
    text = "(2 * x) / (x - 1)"
    
    # This should not raise UnboundLocalError  
    expr = kernS(text)
    
    # Verify it produces a valid expression
    assert expr is not None


def test_kernS_edge_cases():
    """
    Test various edge cases that should work without UnboundLocalError.
    """
    # Edge case 1: No spaces works (this was the original bug)
    expr1 = kernS("x+y")
    assert expr1 is not None
    
    # Edge case 2: Spaces work (existing functionality)
    expr2 = kernS("x * y")
    assert expr2 is not None
    
    # Edge case 3: Complex expressions without spaces
    expr3 = kernS("(x + y) * (z - w)")
    assert expr3 is not None