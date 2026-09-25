"""
Regression test for diophantine permute behavior.

Tests that diophantine function with permute=True gives the same results
regardless of symbol order.
"""
from sympy import symbols, diophantine

def test_diophantine_permute_order_independence():
    """Test that diophantine with permute=True gives same result regardless of syms order."""
    n, m = symbols('n m')
    
    # The equation n**4 + m**4 - 2**4 - 3**4 = 0
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - this should produce all permutations
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) - this should produce the same set of solutions 
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should give the same result (this was broken before the fix)
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # The core assertion - both should give same result to ensure consistent behavior
    assert result1 == result2, f"Results differ based on symbol order: result1 = {result1}, result2 = {result2}"
    
    # Verify both give the full expected solution set 
    assert result1 == expected, f"result1 = {result1}, expected = {expected}"
    assert result2 == expected, f"result2 = {result2}, expected = {expected}"


def test_diophantine_permute_specific_bug():
    """Test the specific bug: syms=(n,m) should not return only (3, 2)"""
    n, m = symbols('n m')
    
    # The equation n**4 + m**4 - 2**4 - 3**4 = 0
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # The bug manifests as syms=(n,m) only returning one solution instead of all
    result = diophantine(eq, syms=(n,m), permute=True)
    
    # This should return all 8 sign and value permutations, not just (3, 2)
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # The bug was that result only contained {(3, 2)}
    assert result == expected, f"Expected all 8 permutations: {expected}, but got: {result}"
    
    # Verify that the specific solution (3, 2) is included (it's one of the 8)
    assert (3, 2) in result, "Result should contain (3, 2) as one of the solutions"
    
    # Verify we get all 8 solutions, not just one
    assert len(result) == 8, f"Result should contain 8 solutions, got {len(result)}: {result}"