"""
Regression test for SymPy Symbol __dict__ issue.

The issue: Symbol instances should not have __dict__ attribute, but after 
the Printable class had __slots__ = () added, they incorrectly gained __dict__.

Before fix: Symbol('s').__dict__ should raise AttributeError
After fix: Symbol('s').__dict__ should raise AttributeError (this is what we want)
"""

def test_symbol_should_not_have_dict_attribute():
    """Test that Symbol instances do not have __dict__ attribute."""
    import sympy
    
    s = sympy.Symbol('s')
    
    # In the correct behavior (both before fix and after fix), 
    # accessing __dict__ should raise AttributeError
    # This ensures Symbol has proper __slots__ behavior
    try:
        _ = s.__dict__
        # If we reach here, __dict__ exists - this is the bug
        assert False, "Symbol should not have __dict__ attribute"
    except AttributeError:
        # This is correct behavior 
        pass  # Test passes

def test_symbol_has_correct_slots():
    """Test that Symbol instances have proper __slots__ behavior."""
    import sympy
    
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ defined
    assert hasattr(s, '__slots__')
    
    # Symbol's __slots__ should contain only 'name' 
    assert s.__slots__ == ('name',)

def test_symbol_prevents_arbitrary_attribute_assignment():
    """Test that Symbol properly uses __slots__ to prevent arbitrary assignment."""
    import sympy
    
    s = sympy.Symbol('s')
    
    # Should not be able to assign arbitrary attributes due to __slots__
    try:
        s.arbitrary_attribute = "test"
        # If no exception is raised, __slots__ isn't working properly
        assert False, "Symbol should not allow arbitrary attribute assignment"
    except AttributeError:
        # This is correct behavior - __slots__ prevents assignment
        pass  # Test passes