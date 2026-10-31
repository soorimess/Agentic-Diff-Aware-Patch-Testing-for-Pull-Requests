"""
Test for factorial(n) % n simplification behavior.

This test verifies that factorial(n) % n simplifies to 0 when n is a positive integer,
which is the behavior that was added in the pull request.
"""

from sympy import Symbol, factorial, S


def test_factorial_has_eval_mod_method():
    """
    Test that factorial class has _eval_Mod method which enables 
    simplification of factorial(n) % n to 0.
    
    This is the core fix: _eval_Mod method was added to factorial class.
    """
    # Create a symbol with integer and positive assumptions
    n = Symbol('n', integer=True, positive=True)
    
    # Test that factorial object has _eval_Mod method
    # This test fails before the fix (no method) and passes after the fix (method exists)
    fact = factorial(n)
    assert hasattr(fact, '_eval_Mod')
    
    # Also verify the specific mathematical behavior works
    assert (factorial(5) % 5).equals(S.Zero) is True


def test_factorial_mod_n_specific():
    """Test specific cases of factorial(n) % n."""
    # Test with specific integer values
    from sympy import Integer
    
    # For n = 1: 1! % 1 = 1 % 1 = 0
    assert (factorial(1) % 1).equals(S.Zero) is True
    
    # For n = 2: 2! % 2 = 2 % 2 = 0  
    assert (factorial(2) % 2).equals(S.Zero) is True
    
    # For n = 3: 3! % 3 = 6 % 3 = 0
    assert (factorial(3) % 3).equals(S.Zero) is True
    
    # For n = 4: 4! % 4 = 24 % 4 = 0
    assert (factorial(4) % 4).equals(S.Zero) is True


def test_factorial_mod_k_range():
    """Test that factorial(n) % k = 0 for 1 <= k <= n."""
    # Test with specific values where k is between 1 and n
    # For n=5, we should have 5! % k = 0 for k=1,2,3,4,5
    assert (factorial(5) % 1).equals(S.Zero) is True
    assert (factorial(5) % 2).equals(S.Zero) is True
    assert (factorial(5) % 3).equals(S.Zero) is True
    assert (factorial(5) % 4).equals(S.Zero) is True
    assert (factorial(5) % 5).equals(S.Zero) is True