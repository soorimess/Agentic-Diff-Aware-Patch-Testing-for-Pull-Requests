"""
Test for regression: Symbol instances should not have __dict__ attribute
since they use __slots__ for memory efficiency.

This is a regression test for the bug where Symbol instances gained a __dict__
attribute after the change to Printable class adding __slots__ = ().
"""

from sympy import Symbol


def test_symbol_should_not_have_dict_attribute():
    """Test that Symbol instances do not have __dict__ attribute.
    
    In SymPy 1.6.2, Symbol instances had no __dict__ attribute.
    In SymPy 1.7, this changed and Symbol instances gained __dict__.
    This is a regression that should be fixed.
    """
    s = Symbol('s')
    
    # Symbol instances should not have __dict__ attribute
    # This is the core behavior that was broken in 1.7
    assert not hasattr(s, '__dict__'), "Symbol should not have __dict__ attribute"


def test_symbol_has_correct_slots():
    """Test that Symbol has correct slots."""
    s = Symbol('s')
    
    # Symbol should have __slots__ with ('name',)
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)


def test_symbol_should_not_allow_dict_assignment():
    """Test that Symbol instances don't allow dictionary-style attribute assignment.
    
    If Symbol had __dict__, then new attributes could be added, which violates
    the slot-based memory efficiency.
    """
    s = Symbol('s')
    
    # This should raise AttributeError since Symbol should not have __dict__
    try:
        s.new_attr = 'value'
        assert False, "Symbol should not allow attribute assignment via __dict__"
    except AttributeError:
        # This is the correct behavior
        pass