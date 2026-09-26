from sympy import Symbol

def test_symbol_no_dict():
    """Test that Symbol instances do not have __dict__ attribute.
    
    In SymPy 1.6.2, Symbol instances had no __dict__ attribute.
    This was broken in 1.7 where Symbol instances started to have __dict__.
    """
    s = Symbol('s')
    # Symbol instances should not have __dict__ attribute
    # This should raise AttributeError in the correct behavior
    try:
        dict_attr = s.__dict__
        # If we get here, __dict__ exists - this is the bug
        assert False, "__dict__ should not exist on Symbol instances"
    except AttributeError:
        # This is the expected behavior (1.6.2 behavior)
        pass