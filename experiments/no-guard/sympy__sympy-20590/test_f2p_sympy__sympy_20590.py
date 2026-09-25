"""Test that Symbol instances don't have __dict__ attribute - regression test for bug fixed in PR."""
from sympy import Symbol


def test_symbol_should_not_have_dict_attribute():
    """Test that Symbol instances should not have __dict__ attribute.
    
    This is a regression test. In version 1.6.2, Symbol instances had no __dict__ attribute.
    The change in version 1.7 introduced a bug where Symbol instances accidentally 
    acquired __dict__. This test verifies that Symbol instances do not have __dict__
    on their instances (as they did in 1.6.2 and should again after fix).
    
    The assertion checks that accessing __dict__ raises AttributeError, just like 
    in SymPy 1.6.2.
    """
    s = Symbol('s')
    
    # Before fix (buggy version 1.7+): hasattr(s, '__dict__') would return True 
    # After fix (correct version): hasattr(s, '__dict__') should return False
    # 
    # The behavior we're fixing is that Symbol instances should not have __dict__
    # attribute as they did in 1.6.2. The bug occurred because the Printable
    # class (from _print_helpers.py) started getting __slots__ = (), which 
    # somehow caused the inheritance chain to affect Symbol instances having __dict__.
    
    # Test that accessing __dict__ raises AttributeError - this is the fundamental issue being fixed
    try:
        _ = s.__dict__
        # If __dict__ exists and is accessible, its the buggy behavior
        assert False, "Symbol instances should not have __dict__ attribute - this indicates the bug is present"
    except AttributeError:
        # This is correct behavior - the __dict__ should not be accessible
        pass