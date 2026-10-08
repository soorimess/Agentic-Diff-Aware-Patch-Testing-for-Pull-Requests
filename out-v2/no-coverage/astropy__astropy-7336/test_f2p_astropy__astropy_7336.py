"""
Regression test for astropy/astropy#7336

Test that units.quantity_input decorator works correctly with constructors
that have type hinted return value of None.
"""

import pytest
import astropy.units as u


def test_quantity_input_constructor_with_none_return():
    """
    Test that quantity_input decorator works with __init__ methods that 
    have return type annotation of None.
    
    This is a regression test for the bug where the decorator would fail
    with AttributeError: 'NoneType' object has no attribute 'to' when
    the decorated method has -> None return annotation.
    """
    
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            self.voltage = voltage

    # This should not raise an AttributeError
    poc = PoC(1.0 * u.V)
    assert poc.voltage == 1.0 * u.V


def test_quantity_input_function_with_none_return():
    """
    Test that quantity_input decorator works with regular functions that 
    have return type annotation of None.
    """
    
    @u.quantity_input
    def process_voltage(voltage: u.V) -> None:
        return None

    # This should not raise an AttributeError
    result = process_voltage(1.0 * u.V)
    assert result is None


def test_quantity_input_function_with_actual_return():
    """
    Test that quantity_input decorator still works correctly with 
    functions that return actual quantities.
    """
    
    @u.quantity_input
    def convert_to_millivolts(voltage: u.V) -> u.mV:
        return voltage.to(u.mV)

    # This should work as before
    result = convert_to_millivolts(1.0 * u.V)
    assert result == 1000.0 * u.mV