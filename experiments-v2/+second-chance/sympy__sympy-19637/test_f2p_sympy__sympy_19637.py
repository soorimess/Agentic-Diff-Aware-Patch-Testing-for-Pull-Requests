"""
Test for kernS bug fix: 'kern' referenced before assignment
"""
from sympy.core.sympify import kernS


def test_kernS_no_spaces_bug():
    """
    Test that kernS doesn't raise UnboundLocalError when input has no spaces
    but has parentheses and is not quoted.
    
    This is a regression test for the bug where 'kern' was referenced before 
    assignment when the input string contained parentheses but no spaces.
    """
    # This input should trigger the bug in the old code:
    # - has parentheses 
    # - no spaces
    # - not quoted
    text = "(2*x)/(x-1)"
    
    # Before the fix, this would raise UnboundLocalError: local variable 'kern' referenced before assignment
    # After the fix, this should work correctly
    result = kernS(text)
    
    # The result should be a valid sympy expression
    assert result is not None


def test_kernS_with_spaces():
    """
    Test that kernS works correctly when input has spaces.
    This ensures we don't break existing functionality and that the kern 
    variable gets properly defined and used.
    """
    # Input with spaces should work normally and define kern variable
    text = "(2 * x) / (x - 1)"
    
    result = kernS(text)
    
    # The result should be a valid sympy expression
    assert result is not None