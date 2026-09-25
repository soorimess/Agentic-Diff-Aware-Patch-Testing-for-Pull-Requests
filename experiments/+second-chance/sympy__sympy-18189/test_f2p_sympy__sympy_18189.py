from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine results are not affected by symbol order with permute=True"""
    n, m = symbols('n m', integer=True)
    
    # Test equation: n^4 + m^4 = 2^4 + 3^4 = 16 + 81 = 97
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n) with permute=True, we get all permutations
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m) with permute=True, we should get the same set of solutions
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # These should be equal - the order shouldn't matter
    assert result1 == result2, f"Results differ: {result1} vs {result2}"

def test_diophantine_permute_full_solutions():
    """Test that we get all expected solutions when permute=True"""
    n, m = symbols('n m', integer=True)
    
    # Test equation: n^4 + m^4 = 2^4 + 3^4 = 97
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # All solutions with syms=(n,m) and permute=True
    result = diophantine(eq, syms=(n,m), permute=True)
    
    # Expected solutions: all 8 sign combinations of (2,3) and (-2,-3) 
    # which satisfy 2^4 + 3^4 = 16 + 81 = 97
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), 
                (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result == expected, f"Expected {expected}, got {result}"