"""
Regression test for astropy/astropy#7336

Test that units.quantity_input decorator works correctly with constructors
and functions that have type hinted return value of None.
"""

import astropy.units as u


def test_quantity_input_constructor_with_none_return_type():
    """Test that quantity_input works with __init__ methods that have -> None return type hint."""
    
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            pass

    # This should not raise an AttributeError: 'NoneType' object has no attribute 'to'
    poc = PoC(1.0 * u.V)
    
    # Verify that the object was created successfully
    assert poc is not None


def test_quantity_input_function_with_none_return_type():
    """Test that quantity_input works with functions that have -> None return type hint."""
    
    @u.quantity_input
    def test_function(value: u.m) -> None:
        return None
    
    # This should not raise an AttributeError: 'NoneType' object has no attribute 'to'
    result = test_function(1.0 * u.m)
    
    # The function should return None (since that's what it's annotated to return)
    assert result is None


def test_quantity_input_constructor_without_return_type():
    """Test that quantity_input still works correctly without return type hint."""
    
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V):
            pass

    # This should work as before
    poc = PoC(1.0 * u.V)
    assert poc is not None


def test_quantity_input_function_without_return_type():
    """Test that quantity_input still works correctly without return type hint."""
    
    @u.quantity_input
    def test_function(value: u.m):
        return value
    
    # This should work as before
    result = test_function(1.0 * u.m)
    assert result == 1.0 * u.m