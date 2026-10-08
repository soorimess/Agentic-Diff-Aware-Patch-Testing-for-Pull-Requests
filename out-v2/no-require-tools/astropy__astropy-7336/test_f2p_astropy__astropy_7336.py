# Licensed under a 3-clause BSD style license - see LICENSE.rst

import pytest
import astropy.units as u


def test_quantity_input_constructor_with_none_return_annotation():
    """
    Test that quantity_input decorator works correctly with constructors
    that have a return type annotation of None.
    
    This is a regression test for the bug where the decorator would fail
    with AttributeError: 'NoneType' object has no attribute 'to' when
    the decorated function has a return annotation of None.
    """
    
    class PoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V) -> None:
            pass

    # This should not raise an AttributeError
    poc = PoC(1.0 * u.V)
    
    # Verify that the object was created correctly
    assert poc is not None


def test_quantity_input_function_with_none_return_annotation():
    """
    Test that quantity_input decorator works correctly with functions
    that have a return type annotation of None.
    """
    
    @u.quantity_input
    def test_function(value: u.m) -> None:
        return None

    # This should not raise an AttributeError
    result = test_function(1.0 * u.m)
    
    # For functions with None return annotation, should return None
    assert result is None


def test_quantity_input_constructor_without_return_annotation():
    """
    Test that quantity_input decorator still works correctly with 
    constructors that don't have a return type annotation (the working case).
    """
    
    class WorkingPoC(object):
        @u.quantity_input
        def __init__(self, voltage: u.V):
            pass

    # This should work as before
    poc = WorkingPoC(1.0 * u.V)
    assert poc is not None


def test_quantity_input_function_without_return_annotation():
    """
    Test that quantity_input decorator still works correctly with 
    functions that don't have a return type annotation (the working case).
    """
    
    @u.quantity_input
    def working_function(value: u.m):
        return value

    # This should work as before
    result = working_function(1.0 * u.m)
    assert result.unit == u.m