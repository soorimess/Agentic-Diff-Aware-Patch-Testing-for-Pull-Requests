from sympy.solvers.diophantine import diophantine
from sympy.abc import m, n

def test_diophantine_permute_order():
    """Test that diophantine with permute=True returns consistent results regardless of symbol order."""
    # This is the exact example from the bug report
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - should return all permutations
    result1 = diophantine(eq, syms=(m,n), permute=True)
    expected1 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Test with syms=(n,m) - should return the same set of results
    result2 = diophantine(eq, syms=(n,m), permute=True)
    expected2 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Both should be equal and contain all permutations
    assert result1 == expected1, f"Expected {expected1}, got {result1}"
    assert result2 == expected2, f"Expected {expected2}, got {result2}"
    assert result1 == result2, f"Results should be equal regardless of symbol order: {result1} != {result2}"