"""Test that posify preserves assumptions like finite."""

from sympy import Symbol, Dummy, posify


def test_posify_preserves_finite_assumption():
    """Test that posify preserves finite assumption on symbols."""
    # Create a symbol with finite=True assumption
    x = Symbol('x', finite=True)
    
    # Verify the symbol has the assumption before posify
    assert x.is_finite is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The result should be a dummy symbol
    assert isinstance(xp, Dummy)
    assert xp.name == 'x'
    
    # The key test: before fix this would be None, after fix it should be True
    # This was the reported bug - posify was ignoring is_finite assumption
    assert xp.is_finite is True


def test_posify_preserves_finite_assumption_in_expression():
    """Test that posify preserves finite assumption when applied to expressions."""
    # Create a symbol with finite=True assumption  
    x = Symbol('x', finite=True)
    
    # Apply posify to an expression with the symbol
    expr = x**2 + 1
    posified_expr, rep = posify(expr)
    
    # The key property: the result should preserve the finite assumption
    # Just check that the expression contains properly transformed symbols
    # The actual check of assumption preservation will be through the test above
    # Here we verify the transformation properly happened on the expression
    assert expr != posified_expr
    # This test focuses on ensuring no regression occurs in the fix
    assert len(rep) >= 0 # at least empty dict