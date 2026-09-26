"""
Regression test for Symbol __dict__ issue.

In version 1.6.2 Symbol instances had no `__dict__` attribute
In version 1.7 they gained one (which is considered a bug).
This test ensures that Symbol instances do NOT have __dict__ attribute.
"""

def test_symbol_should_not_have_dict_attribute():
    """
    Test that Symbol instances do not have __dict__ attribute.
    
    In SymPy 1.6.2, accessing Symbol.__dict__ raised AttributeError.
    In SymPy 1.7, Symbol.__dict__ returned an empty dict {}.
    The latter behavior is considered a bug - Symbol should not have __dict__.
    """
    import sympy
    
    s = sympy.Symbol('s')
    
    # This should raise AttributeError (the correct behavior)
    # If it doesn't, then Symbol has __dict__ which is the bug
    try:
        dict_attr = s.__dict__
        # If we reach here, Symbol has __dict__ which is the bug
        raise AssertionError("Symbol instances should not have __dict__ attribute")
    except AttributeError:
        # This is the correct behavior - no __dict__ attribute exists
        pass

def test_symbol_has_expected_slots():
    """Test that Symbol instances have the expected __slots__."""
    import sympy
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ defined
    assert hasattr(s, '__slots__')
    
    # The slots should be ('name',) as expected for Symbol
    slots = s.__slots__
    assert slots == ('name',)