from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine results are consistent regardless of symbol order with permute=True."""
    n, m = symbols('n m')
    
    # Test case from the bug report
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) 
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) 
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should return the same set of solutions
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result1 == expected, f"Expected {expected} for syms=(m,n), got {result1}"
    assert result2 == expected, f"Expected {expected} for syms=(n,m), got {result2}"

def test_diophantine_permute_consistency():
    """Test that diophantine permute functionality works correctly."""
    n, m = symbols('n m')
    
    # More general test case - this should work correctly with permute
    eq = n**2 + m**2 - 5  # Solutions: (±1,±2) and (±2,±1)
    
    # Test permute=True
    result = diophantine(eq, permute=True)
    
    # Should return all permutations of sign combinations 
    expected = {(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)}
    
    assert result == expected, f"Expected {expected} for permute=True, got {result}"
    
    # Test with syms order change
    result1 = diophantine(eq, syms=(m,n), permute=True)
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    assert result1 == expected, f"Expected {expected} for syms=(m,n) with permute, got {result1}"
    assert result2 == expected, f"Expected {expected} for syms=(n,m) with permute, got {result2}"