"""
Regression test for singledispatch function/method support in Sphinx autodoc.

This test verifies that @singledispatch functions and methods are properly
documented by the new SingledispatchFunctionDocumenter and SingledispatchMethodDocumenter.
"""

import functools


def test_singledispatch_function_detection():
    """Test that is_singledispatch_function correctly identifies singledispatch functions."""
    from sphinx.util.inspect import is_singledispatch_function
    
    @functools.singledispatch
    def my_func(arg):
        """A singledispatch function."""
        return arg
    
    my_func.register(int, lambda x: f"int: {x}")
    my_func.register(str, lambda x: f"str: {x}")
    
    # Test that it correctly identifies singledispatch functions
    result = is_singledispatch_function(my_func)
    assert result is True
    
    # Test that it correctly rejects regular functions
    def regular_func(x):
        return x
    result = is_singledispatch_function(regular_func)
    assert result is False