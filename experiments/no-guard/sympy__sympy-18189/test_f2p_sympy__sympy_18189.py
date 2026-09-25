from sympy import diophantine, symbols

def test_diophantine_permute_order_bug():
    """Test that diophantine results are consistent with syms order when permute=True"""
    n, m = symbols('n m')
    
    # This should return all permutations of the solutions regardless of symbol order
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - this produces 8 solutions
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) - this used to only produce 1 solution (the base one)
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should contain the same logical solutions, just ordered differently
    # Before the fix, result2 was {(3, 2)} instead of the full 8 solutions
    assert len(result1) == 8
    assert len(result2) == 8
    
    # The specific results mentioned in the bug report
    expected_solutions = {
        (-3, -2), (-3, 2), (-2, -3), (-2, 3), 
        (2, -3), (2, 3), (3, -2), (3, 2)
    }
    
    # Both should contain the same solutions  
    assert result1 == expected_solutions
    assert result2 == expected_solutions
    
    # Also verify that the solutions are correct by substituting back into equation
    for sol in result1:
        assert eq.subs([(n, sol[0]), (m, sol[1])]) == 0