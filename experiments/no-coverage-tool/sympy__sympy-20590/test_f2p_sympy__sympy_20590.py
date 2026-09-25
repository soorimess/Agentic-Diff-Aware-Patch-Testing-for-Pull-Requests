"""
Regression test for issue where Symbol instances gained __dict__ after
adding __slots__ = () to the Printable base class.

When __slots__ = () is added to Printable, Symbol instances now have __dict__,
which they shouldn't have since they use __slots__ in their inheritance chain.
"""

from sympy import Symbol

def test_symbol_should_not_have_dict():
    """Test that Symbol instances do not have __dict__ attribute."""
    s = Symbol('x')
    # Before the change: AttributeError would be raised
    # After the change: __dict__ exists and is empty
    # The correct behavior is that __dict__ should not exist
    try:
        dict_attr = s.__dict__
        # If we get here, __dict__ exists, which is the bug
        # This should not happen - symbols should not have __dict__
        assert False, "__dict__ should not exist on Symbol instances"
    except AttributeError:
        # This is the correct behavior - __dict__ should not exist
        pass

def test_symbol_has_slots():
    """Test that Symbol instances have the proper slots."""
    s = Symbol('x')
    assert hasattr(s, '__slots__')
    # Check that the slots are what we expect
    expected_slots = ('name',)
    assert s.__slots__ == expected_slots