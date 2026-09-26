from sympy import diophantine, symbols

def test_diophantine_permute_order_consistency():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Test the specific case from the bug report
    # When syms=(m,n), permute=True, we get all permutations
    result_mn = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True)
    
    # When syms=(n,m), permute=True, we should get the same result (but currently don't)
    result_nm = diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True)
    
    # The bug: these should be equal but they're not
    # Before fix: result_mn = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    #            result_nm = {(3, 2)}
    
    # After fix they should both be the same
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Both should give the same comprehensive result
    assert result_mn == expected, f"syms=(m,n) result incorrect: expected {expected} but got {result_mn}"
    assert result_nm == expected, f"syms=(n,m) result incorrect: expected {expected} but got {result_nm}"
    
    # Also verify that the behavior is consistent with the order of symbols in the equation
    # The equation n**4 + m**4 - 2**4 - 3**4 has free symbols [n, m] in sorted order
    # When syms=(n,m), syms == var, so no reordering happens
    # When syms=(m,n), syms != var, so reordering happens and the bug manifests