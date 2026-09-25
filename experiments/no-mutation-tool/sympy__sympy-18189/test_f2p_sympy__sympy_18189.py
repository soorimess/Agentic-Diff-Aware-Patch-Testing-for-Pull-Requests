from sympy import symbols, diophantine

# Test for regression of diophantine permute=True bug
# When syms order changes with permute=True, results should be consistent

def test_diophantine_permute_order_dependence():
    """Test that diophantine with permute=True gives consistent results regardless of syms order."""
    n, m = symbols('n m')
    
    # The equation: n**4 + m**4 - 2**4 - 3**4 = 0
    # This should have solutions where n**4 + m**4 = 2**4 + 3**4 = 16 + 81 = 97
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - should get all permutations
    sol1 = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) - should get the same set but with different ordering
    sol2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should produce the same set of solutions, just with potentially different tuple ordering
    # The solutions should include: (3,2), (-3,2), (3,-2), (-3,-2) and all permutations
    expected_solutions = {
        (-3, -2), (-3, 2), (-2, -3), (-2, 3), 
        (2, -3), (2, 3), (3, -2), (3, 2)
    }
    
    # Both should match the expected solutions
    assert sol1 == expected_solutions, f"sol1 = {sol1}, expected = {expected_solutions}"
    assert sol2 == expected_solutions, f"sol2 = {sol2}, expected = {expected_solutions}"

def test_diophantine_permute_bug_demo():
    """Demonstrate the specific bug: different syms order gives different results."""
    n, m = symbols('n m')
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # As per the bug report, with syms=(m,n) we get 8 solutions
    sol_mn = diophantine(eq, syms=(m,n), permute=True)
    
    # With syms=(n,m) we get only 1 solution (the bug)
    sol_nm = diophantine(eq, syms=(n,m), permute=True)
    
    # This shows the problem: they should return the same solution set
    # Before the fix: sol_mn would have 8 elements, sol_nm would have 1
    # After the fix: both should have 8 elements
    
    # The bug is that sol_nm has only 1 element instead of 8
    assert len(sol_mn) == 8, f"Expected 8 solutions for (m,n) order, got {len(sol_mn)}"
    assert len(sol_nm) == 8, f"Expected 8 solutions for (n,m) order, got {len(sol_nm)}"
    
    # Both should contain the same core solutions
    expected_core = {(3, 2), (-3, 2), (3, -2), (-3, -2)}
    assert expected_core.issubset(sol_mn), "Missing core solutions in sol_mn"
    assert expected_core.issubset(sol_nm), "Missing core solutions in sol_nm"

if __name__ == "__main__":
    test_diophantine_permute_order_dependence() 
    test_diophantine_permute_bug_demo()
    print("All tests passed!")