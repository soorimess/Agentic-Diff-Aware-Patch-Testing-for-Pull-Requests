"""
Regression test for Symbol __dict__ behavior change.

The bug report states that in version 1.6.2 Symbol instances had no __dict__ attribute,
but in 1.7 they do. This is because the Printable class now has __slots__ = (),
which allows subclasses to have __dict__.

This is a bug because Symbol instances should respect their __slots__ definition and
not have __dict__ attribute, which violates the purpose of __slots__.
"""

def test_symbol_should_not_have_dict_attribute():
    """
    Test that Symbol instances should not have __dict__ attribute.
    
    Before fix: Symbol instances had __dict__ (bug)
    After fix:  Symbol instances should NOT have __dict__ (correct behavior)
    """
    import sympy
    
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ defined
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)
    
    # Symbol instances should NOT have __dict__ attribute (this is the bug)
    # The __slots__ = ('name',) should prevent __dict__ from existing
    try:
        dict_attr = s.__dict__
        # If we get here, __dict__ exists - this is the bug behavior
        # This assertion should fail in the fixed version
        assert False, "__dict__ should not exist on Symbol instances due to __slots__"
    except AttributeError:
        # This is the correct behavior - __dict__ should not exist
        pass

def test_symbol_slots_prevent_arbitrary_attributes():
    """
    Test that Symbol instances properly respect __slots__ and prevent
    setting arbitrary attributes.
    """
    import sympy
    
    s = sympy.Symbol('s')
    
    # Check that __slots__ is defined as expected
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)
    
    # Check that we can access the name attribute
    assert s.name == 's'
    
    # Check that we cannot set arbitrary attributes (because of __slots__)
    try:
        s.new_attr = 'test'
        # If we get here, __slots__ is not working properly - this is the bug
        assert False, "Should not be able to set arbitrary attributes on Symbol due to __slots__"
    except AttributeError:
        # This is expected - __slots__ should prevent this
        pass