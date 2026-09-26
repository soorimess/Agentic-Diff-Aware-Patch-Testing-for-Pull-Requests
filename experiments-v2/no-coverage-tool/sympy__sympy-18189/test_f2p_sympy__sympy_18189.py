from sympy import symbols
from sympy.solvers.diophantine import diophantine

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives consistent results regardless of syms order."""
    n, m = symbols('n m')
    
    # Test equation: n^4 + m^4 - 2^4 - 3^4 = 0
    # This should have solutions with all permutations of signs and values
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n), we get all solutions
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m), we should get the same set of solutions (but in different order)
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should contain the same solutions (just reordered)
    expected_solutions = {
        (-3, -2), (-3, 2), (-2, -3), (-2, 3),
        (2, -3), (2, 3), (3, -2), (3, 2)
    }
    
    # The bug causes result2 to only contain (3, 2) instead of all solutions
    # This test specifically verifies that the permute parameter is respected
    # regardless of the order of symbols in the syms parameter
    assert result1 == expected_solutions
    assert result2 == expected_solutions
    
    # Verify we get all solutions, not just partial ones
    assert len(result1) == 8
    assert len(result2) == 8