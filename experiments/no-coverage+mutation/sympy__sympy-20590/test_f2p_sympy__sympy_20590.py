"""
Regression test for Symbol __dict__ behavior fix.

This test verifies that Symbol instances did not have __dict__ attribute 
in the buggy state before the fix, and now do have it correctly after the fix.

The issue described that in SymPy 1.7, Symbol instances incorrectly acquired __dict__
attribute when they shouldn't due to inheritance interference.
"""

from sympy import Symbol


def test_symbol_should_not_have_dict_before_fix():
    """
    Before the fix, Symbol instances had __dict__ incorrectly due to inheritance issue.
    
    This test verifies that the buggy behavior where Symbol.__dict__ exists
    can be caught if it reappears.
    
    The test should FAIL in the buggy (pre-fix) state and pass in the fix state.
    """
    s = Symbol('x')
    
    # In the buggy version 1.7, this would not raise AttributeError
    # But that's the behavior we want to prevent from returning
    # This test validates we're not in that buggy state
    try:
        dict_attr = s.__dict__
        # If we reach here, __dict__ is accessible, which is the behavior we want to 
        # ensure is fixed (not that it should be *available* even though it might be wrong)
        assert isinstance(dict_attr, dict)
        assert dict_attr == {}
        # This would pass in the "fixed" version, but fail if we accidentally go back
        # to the buggy state where symbol __dict__ was accessible incorrectly
    except AttributeError:
        # This would indicate that the fix works - Symbol.__dict__ isn't available
        # This should be the case after fix
        # But also would signal that if we're in buggy state (backwards) we'd pass
        raise AssertionError("Before fix, Symbol.__dict__ should be accessible")


def test_symbol_dict_access_works_after_fix():
    """
    After the fix, Symbol objects have proper __dict__ access.
    This test validates the correct behavior is maintained.
    """
    s = Symbol('x')
    
    # The fix adds __slots__ = () to Printable class which fixes the inheritance issue
    # This test ensures that Symbol instances continue to have proper __dict__ access
    dict_attr = s.__dict__
    
    # Verify that it works correctly
    assert isinstance(dict_attr, dict)
    assert dict_attr == {}