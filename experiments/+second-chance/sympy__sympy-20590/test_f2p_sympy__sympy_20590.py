from sympy import Symbol

def test_symbol_should_not_have_dict():
    """Test that Symbol instances should not have __dict__ attribute.
    
    In SymPy 1.6.2, Symbol instances had no __dict__ attribute.
    In SymPy 1.7, due to inheritance chain issues, Symbol instances incorrectly 
    gained a __dict__ attribute, which violates the __slots__ mechanism. 
    This is a bug because __slots__ should prevent __dict__ creation.
    """
    s = Symbol('x')
    
    # This behavior is wrong - Symbol should not have __dict__
    # according to its __slots__ definition
    has_dict = hasattr(s, '__dict__')
    assert not has_dict, "Symbol instances should not have __dict__ when they have __slots__"
    
    # Verify the slots exists as expected
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)

def test_symbol_should_not_allow_arbitrary_attribute_assignment():
    """Test that Symbol instances should reject arbitrary attribute assignment.
    
    If a Symbol has __slots__ defined properly, it should not allow assignment 
    of new attributes, which indicates __dict__ is not properly controlled.
    """
    s = Symbol('x')
    
    # This behavior is wrong - Symbol should reject new attribute assignment
    try:
        s.new_attr = 'test_value'
        # If we get here, then __dict__ was created and new attributes are allowed
        assert False, "Symbol should not allow assignment of arbitrary attributes"
    except AttributeError:
        # This is the correct behavior
        pass

def test_that_symbol_has_correct_slots_definition():
    """Test that Symbol has correct __slots__ definition."""
    s = Symbol('x')
    
    # Verify Symbol has the expected __slots__ 
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)
    
    # Symbols should be able to access existing attributes
    assert s.name == 'x'