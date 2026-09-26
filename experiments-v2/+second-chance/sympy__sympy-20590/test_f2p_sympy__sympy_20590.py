"""
Regression test for the Symbol __dict__ issue.

In SymPy 1.6.2, Symbol instances had no __dict__ attribute.
In SymPy 1.7, they started to have __dict__ (which is problematic).
This test ensures that Symbol instances don't have __dict__.
"""

def test_symbol_has_no_dict():
    """Test that Symbol instances do not have __dict__ attribute."""
    import sympy
    s = sympy.Symbol('s')
    
    # Symbol instances should not have __dict__ because they use __slots__
    # This should raise AttributeError in the correct behavior
    try:
        dict_attr = s.__dict__
        # If we get here, it means __dict__ exists, which is the bug
        assert False, "__dict__ should not exist on Symbol instances"
    except AttributeError:
        # This is the expected behavior - __dict__ should not exist
        pass