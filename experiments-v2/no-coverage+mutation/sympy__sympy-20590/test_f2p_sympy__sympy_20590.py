"""
Regression test for Symbol __dict__ behavior change.

In SymPy 1.6.2, Symbol instances had no __dict__ attribute.
In SymPy 1.7+, Symbol instances incorrectly gained a __dict__ attribute due to 
changes in the Printable class, which broke the expected __slots__ behavior.

This test ensures that Symbol instances do not have __dict__ attribute, 
which is the correct behavior that should be restored.
"""

def test_symbol_should_not_have_dict_attribute():
    """
    Test that Symbol instances do not have __dict__ attribute.
    
    Before the fix: Symbol instances incorrectly had __dict__ = {}
    After the fix: Symbol instances should not have __dict__ attribute at all
    """
    import sympy
    
    s = sympy.Symbol('s')
    
    # The bug: Symbol instances were getting __dict__ attribute in 1.7+
    # This should not happen - __slots__ should prevent __dict__ creation
    
    try:
        # This should raise AttributeError in correct behavior
        dict_attr = s.__dict__
        # If we reach here, __dict__ exists - this is the bug
        assert False, f"Symbol should not have __dict__ attribute, but got: {dict_attr}"
    except AttributeError:
        # This is the correct behavior
        pass

def test_symbol_has_correct_slots():
    """Verify Symbol has correct __slots__ definition"""
    import sympy
    
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ = ('name',)
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)