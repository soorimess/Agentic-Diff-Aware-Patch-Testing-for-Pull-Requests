from sympy import symbols, diophantine

# Test for the bug where diophantine results differ based on symbol order when permute=True
def test_diophantine_permute_order():
    # Using the exact example from the bug report
    n, m = symbols('n, m')
    
    # Test with syms=(m,n) - should return all 8 solutions
    result1 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) - should return all 8 solutions but previously returned only 1
    result2 = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True)
    
    # Both should return the same set of solutions (8 solutions)
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result1 == expected, "First symbol order should give all solutions"
    assert result2 == expected, "Second symbol order should also give all solutions"
    
    # Verify that the two results are equal (they should be the same set)
    assert result1 == result2, "Results should be identical regardless of symbol order"