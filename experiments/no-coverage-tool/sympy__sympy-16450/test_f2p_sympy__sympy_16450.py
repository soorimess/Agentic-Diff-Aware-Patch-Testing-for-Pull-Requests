from sympy import Symbol, posify

def test_posify_preserves_finite_assumption():
    """Test that posify preserves the finite assumption of symbols."""
    # Create a symbol with finite=True assumption 
    x = Symbol('x', finite=True)
    
    # Verify the original assumption is set
    assert x.is_finite is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should also have is_finite=True
    # This is the bug: before the fix, xp.is_finite would be None
    assert xp.is_finite is True
    # Also verify it has the required assumptions for being positive
    assert xp.is_positive is True

def test_posify_preserves_multiple_assumptions():
    """Test that posify preserves multiple assumptions."""
    # Create a symbol with multiple assumptions
    x = Symbol('x', finite=True, integer=True, positive=True)
    
    # Verify the original assumptions are set
    assert x.is_finite is True
    assert x.is_integer is True
    assert x.is_positive is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should preserve all assumptions
    assert xp.is_finite is True
    assert xp.is_integer is True
    assert xp.is_positive is True

def test_posify_preserves_infinite_assumption():
    """Test that posify preserves the infinite assumption of symbols."""
    # Create a symbol with infinite=True assumption 
    x = Symbol('x', infinite=True)
    
    # Verify the original assumption is set
    assert x.is_infinite is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should also have is_infinite=True
    assert xp.is_infinite is True
    # Also verify it has the required assumptions for being positive
    assert xp.is_positive is True

def test_posify_preserves_commutative_assumption():
    """Test that posify preserves the commutative assumption of symbols."""
    # Create a symbol with commutative=True assumption 
    x = Symbol('x', commutative=True)
    
    # Verify the original assumption is set
    assert x.is_commutative is True
    
    # Apply posify
    xp, rep = posify(x)
    
    # The new symbol should also have is_commutative=True
    assert xp.is_commutative is True