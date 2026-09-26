"""
Regression test for the bug where Symbol instances gained __dict__ in version 1.7.

The bug was that Symbol instances started having __dict__ attributes in version 1.7,
which breaks the expected behavior of using __slots__ for memory efficiency.
"""

def test_symbol_should_not_have_dict():
    """Test that Symbol instances do not have __dict__ attribute (the bug)."""
    import sympy
    s = sympy.Symbol('s')
    
    # This should raise AttributeError - Symbol instances should not have __dict__
    # The bug is that they DO have __dict__ in version 1.7+
    try:
        dict_attr = s.__dict__
        # If we get here, __dict__ exists - this is the bug
        # The test should fail in the buggy version, pass in the fixed version
        raise AssertionError("__dict__ should not exist on Symbol instances (bug)")
    except AttributeError:
        # This is the correct behavior - __dict__ should not exist
        pass

def test_symbol_slots():
    """Test that Symbol instances have correct __slots__."""
    import sympy
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ defined
    assert hasattr(s, '__slots__')
    
    # Check that it has the expected slots (name)
    slots = s.__slots__
    assert 'name' in slots
    # Should only have 'name' slot
    assert len(slots) == 1

def test_symbol_attribute_access():
    """Test that Symbol instances can access their name attribute."""
    import sympy
    s = sympy.Symbol('s')
    
    # Should be able to access name
    assert s.name == 's'

def test_symbol_no_arbitrary_attributes():
    """Test that Symbol instances cannot set arbitrary attributes."""
    import sympy
    s = sympy.Symbol('s')
    
    # Should not be able to set arbitrary attributes due to __slots__
    try:
        s.new_attr = 'test'
        # If we get here, __slots__ is not working properly (the bug)
        raise AssertionError("__slots__ is not working - should not be able to set new attributes")
    except AttributeError:
        # This is expected behavior
        pass