"""
Regression test for astropy/astropy#7336

The units.quantity_input decorator fails for constructors with type hinted 
return value -> None
"""

import astropy.units as u


def test_quantity_input_constructor_with_none_return_type():
    """Test that quantity_input decorator works with constructors that have -> None return type hint."""
    
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            pass

    # This should not raise AttributeError: 'NoneType' object has no attribute 'to'
    poc = PoC(1.0 * u.V)
    assert poc is not None


def test_quantity_input_function_with_none_return_type():
    """Test that quantity_input decorator works with functions that have -> None return type hint."""
    
    @u.quantity_input
    def test_function(value: u.m) -> None:
        return None

    # This should not raise AttributeError: 'NoneType' object has no attribute 'to'
    result = test_function(1.0 * u.m)
    assert result is None


def test_quantity_input_function_with_normal_return_type():
    """Test that quantity_input decorator still works with normal return types."""
    
    @u.quantity_input
    def test_function(value: u.m) -> u.cm:
        return value.to(u.cm)

    # This should work as before
    result = test_function(1.0 * u.m)
    assert result.unit == u.cm
    assert result.value == 100.0  # 1m = 100cm