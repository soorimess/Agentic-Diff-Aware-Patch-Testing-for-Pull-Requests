"""
Test for regression of Symbol.__dict__ behavior change.

This tests the specific case mentioned in the bug report where 
Symbol instances gained __dict__ attribute due to changes in Printable class.
The bug was introduced when __slots__ = () was added to Printable class.
This test ensures that Symbol instances behave as they did in 1.6.2 (no __dict__).
"""

def test_symbol_should_not_have_dict():
    """Test that Symbol instances do NOT have __dict__ attribute, like in 1.6.2.
    
    This was a regression in 1.7 where Symbol instances started getting __dict__
    which goes against the purpose of __slots__ usage and should be prevented.
    
    Expected behavior (proper): Symbol.__dict__ should raise AttributeError
    Current buggy behavior: Symbol.__dict__ returns empty dict {}
    """
    import sympy
    
    s = sympy.Symbol('s')
    
    # This is the expected behavior that should be restored
    # Symbol should not have __dict__ attribute (no dict should exist)
    try:
        dict_attr = s.__dict__
        # If we get here, it means __dict__ exists (bug!)
        # This should never happen - it's a regression we're testing for
        raise AssertionError("BUG: Symbol instances should NOT have __dict__ attribute")
    except AttributeError:
        # This is the correct behavior (like in 1.6.2)
        pass  # Expected case


def test_symbol_slots_behavior():
    """Test that Symbol still only uses __slots__ = ('name',)."""
    import sympy
    
    s = sympy.Symbol('s')
    
    # Symbol should have __slots__ defined as ('name',)
    assert hasattr(s, '__slots__')
    slots = getattr(s, '__slots__')
    assert slots == ('name',), f"Expected ('name',), got {slots}"


if __name__ == "__main__":
    test_symbol_should_not_have_dict()
    test_symbol_slots_behavior()
    print("All tests passed!")