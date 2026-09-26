"""
Regression test for Symbol __dict__ issue.

Before the fix, Symbol instances had __dict__ since 1.7 due to Printable class
accidentally getting __slots__ = () which caused Symbol to inherit __dict__.
After the fix, Symbol instances should not have __dict__ attribute.
"""

def test_symbol_should_not_have_dict():
    """Test that Symbol instances do not have __dict__ attribute."""
    from sympy import Symbol
    
    s = Symbol('s')
    
    # Symbol instances should not have __dict__ attribute at all
    # This is the core behavior that was broken in 1.7
    assert not hasattr(s, '__dict__'), "Symbol instances should not have __dict__ attribute"
    
    # Also test that accessing __dict__ raises AttributeError
    try:
        _ = s.__dict__
        assert False, "Accessing __dict__ on Symbol should raise AttributeError"
    except AttributeError:
        pass  # This is expected

def test_symbol_slots_correct():
    """Test that Symbol instances have correct __slots__."""
    from sympy import Symbol
    
    s = Symbol('s')
    
    # Symbol should have __slots__ = ('name',)
    expected_slots = ('name',)
    actual_slots = getattr(s, '__slots__', None)
    
    assert actual_slots == expected_slots

def test_symbol_should_not_allow_extra_attributes():
    """Test that Symbol instances don't allow arbitrary attribute assignment."""
    from sympy import Symbol
    
    s = Symbol('s')
    
    # Should not be able to set arbitrary attributes - should raise AttributeError
    try:
        s.new_attr = 'test'
        assert False, "Symbol should not allow setting arbitrary attributes"
    except AttributeError:
        # This is the correct behavior after the fix
        pass