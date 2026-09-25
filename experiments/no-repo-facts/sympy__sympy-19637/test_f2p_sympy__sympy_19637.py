"""
Regression test for kernS UnboundLocalError bug.

This test verifies that kernS doesn't raise UnboundLocalError for strings with 
parentheses but no spaces, which was fixed in pull request 19637.
"""

from sympy.core.sympify import kernS


def test_kernS_no_unboundlocal_error():
    """
    Test that kernS doesn't raise UnboundLocalError for strings with 
    parentheses but no spaces.
    
    Previously this would cause:
    UnboundLocalError: local variable 'kern' referenced before assignment
    """
    # The exact case mentioned in the bug report
    text = "(2*x)/(x-1)"
    
    # This should not raise UnboundLocalError
    result = kernS(text)
    assert result is not None

    # Additional test cases to ensure the fix works broadly  
    test_cases = [
        "(x+y)",
        "(a-b)",  
        "(x*y)",
        "((a+b)/(c-d))",
        "(-x)"
    ]
    
    for case in test_cases:
        # These should all work without UnboundLocalError
        result = kernS(case)
        assert result is not None, f"Failed on input: {case}"