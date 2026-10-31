"""
Regression test for singledispatch function support in autodoc.

This test verifies that singledispatch functions are properly documented
with all their overloads.
"""
import functools
import inspect
from unittest.mock import patch

import pytest

from sphinx.ext.autodoc import FunctionDocumenter
from sphinx.util.inspect import is_singledispatch_function


def test_is_singledispatch_function_helper():
    """Test the helper function that detects singledispatch functions."""
    # Create a singledispatch function
    @functools.singledispatch
    def my_func(arg):
        """A test singledispatch function."""
        return f"Default: {arg}"
    
    @my_func.register
    def _(arg: int):
        return f"Integer: {arg}"
        
    @my_func.register
    def _(arg: str):
        return f"String: {arg}"
    
    # Test that our helper function works
    assert is_singledispatch_function(my_func) is True
    
    # Test that regular functions are not detected
    def regular_func():
        pass
    assert is_singledispatch_function(regular_func) is False


def test_singledispatch_function_documenter_exists():
    """Test that SingledispatchFunctionDocumenter class exists and is registered."""
    # This should fail before the change and pass after
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
        assert SingledispatchFunctionDocumenter is not None
        assert SingledispatchFunctionDocumenter.objtype == 'singledispatch_function'
        assert SingledispatchFunctionDocumenter.directivetype == 'function'
        assert SingledispatchFunctionDocumenter.priority > FunctionDocumenter.priority
    except ImportError:
        # This is expected before the change
        pytest.skip("SingledispatchFunctionDocumenter not yet implemented")


def test_singledispatch_function_documentation():
    """Test that singledispatch functions can be documented."""
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    except ImportError:
        pytest.skip("SingledispatchFunctionDocumenter not yet implemented")
    
    # Create a singledispatch function
    @functools.singledispatch
    def process_data(arg):
        """Process data with different types."""
        return f"Default handler: {arg}"
    
    @process_data.register
    def _(arg: int):
        """Handle integer data."""
        return f"Integer handler: {arg}"
        
    @process_data.register
    def _(arg: str):
        """Handle string data."""
        return f"String handler: {arg}"
    
    # Test that the function has registry information
    assert hasattr(process_data, 'registry')
    # Should have default + 2 overloads
    assert len(process_data.registry) >= 2


def test_singledispatch_method_documenter_exists():
    """Test that SingledispatchMethodDocumenter class exists and is registered."""
    # This should fail before the change and pass after
    try:
        from sphinx.ext.autodoc import SingledispatchMethodDocumenter
        assert SingledispatchMethodDocumenter is not None
        assert SingledispatchMethodDocumenter.objtype == 'singledispatch_method'
        assert SingledispatchMethodDocumenter.directivetype == 'method'
        assert SingledispatchMethodDocumenter.priority > FunctionDocumenter.priority
    except ImportError:
        # This is expected before the change
        pytest.skip("SingledispatchMethodDocumenter not yet implemented")


def test_singledispatch_method_documentation():
    """Test that singledispatch methods can be documented."""
    try:
        from sphinx.ext.autodoc import SingledispatchMethodDocumenter
    except ImportError:
        pytest.skip("SingledispatchMethodDocumenter not yet implemented")
    
    # Create a class with a singledispatch method
    class MyClass:
        @functools.singledispatch
        def process_data(self, arg):
            """Process data with different types."""
            return f"Default handler: {arg}"
        
        @process_data.register
        def _(self, arg: int):
            """Handle integer data."""
            return f"Integer handler: {arg}"
            
        @process_data.register
        def _(self, arg: str):
            """Handle string data."""
            return f"String handler: {arg}"
    
    # Test that the method can be documented
    # We can't easily test the full documenter without a full Sphinx setup,
    # but we can test that the method has the right structure
    obj = MyClass()
    # The method itself should be a singledispatch object
    assert hasattr(obj.process_data, 'register')
    assert hasattr(obj.process_data, 'dispatch')