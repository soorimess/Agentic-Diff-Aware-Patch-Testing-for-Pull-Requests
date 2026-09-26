"""
Regression test for the Symbol __dict__ issue.

This test verifies that Symbol instances don't have __dict__ attribute
as they did in SymPy 1.6.2, but rather should have no __dict__ since they
use __slots__.
"""

def test_symbol_should_not_have_dict():
    """Test that Symbol instances don't have __dict__ attribute (the bug fix)."""
    import sympy
    s = sympy.Symbol('s')
    
    # Before the fix, Symbol instances would have __dict__ (empty dict)
    # After the fix, Symbol instances should NOT have __dict__ attribute
    # This should raise AttributeError, not return an empty dict
    try:
        dict_attr = s.__dict__
        # If we get here, __dict__ exists - this means the bug is present
        # The fix should make __dict__ raise AttributeError
        assert False, "__dict__ should not exist on Symbol instances"
    except AttributeError:
        # This is the correct behavior - __dict__ should not exist
        pass

def test_symbol_has_correct_slots():
    """Test that Symbol instances have correct __slots__."""
    import sympy
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ with 'name' 
    assert hasattr(s, '__slots__')
    assert 'name' in s.__slots__
    
    # __slots__ should not include __dict__
    assert '__dict__' not in s.__slots__

def test_printable_no_dict():
    """Test that Printable base class doesn't create __dict__."""
    from sympy.printing.defaults import Printable
    
    p = Printable()
    
    # Printable should not have __dict__ since it now has __slots__ = ()
    try:
        dict_attr = p.__dict__
        # If we get here, __dict__ exists - this means Printable allows __dict__
        assert False, "__dict__ should not exist on Printable instances"
    except AttributeError:
        # This is the correct behavior
        pass