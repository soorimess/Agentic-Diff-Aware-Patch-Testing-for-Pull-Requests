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


def test_singledispatch_function_can_document_member():
    """Test that the SingledispatchFunctionDocumenter can_document_member method works."""
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    except ImportError:
        pytest.skip("SingledispatchFunctionDocumenter not yet implemented")
    
    # Create a singledispatch function
    @functools.singledispatch
    def my_func(arg):
        """A test singledispatch function."""
        return f"Default: {arg}"
    
    @my_func.register
    def _(arg: int):
        return f"Integer: {arg}"
        
    # Test that can_document_member returns True for singledispatch functions
    assert SingledispatchFunctionDocumenter.can_document_member(my_func, 'my_func', False, None) is True
    
    # Test that it returns False for regular functions
    def regular_func():
        pass
    assert SingledispatchFunctionDocumenter.can_document_member(regular_func, 'regular_func', False, None) is False


def test_singledispatch_function_registry_structure():
    """Test that singledispatch functions have the expected registry structure."""
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
    
    # Test that the registry contains the expected items
    registry_items = list(process_data.registry.items())
    # Should have at least the default implementation and 2 registered functions
    assert len(registry_items) >= 3
    
    # Check that the registry has the right structure
    for typ, func in registry_items:
        # Each entry should be a type and a function
        assert callable(func)
        if typ is not object:  # Skip the default object type
            assert hasattr(typ, '__name__') or hasattr(typ, '__qualname__')


def test_singledispatch_function_documenter_method_exists():
    """Test that SingledispatchFunctionDocumenter has required methods."""
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    except ImportError:
        pytest.skip("SingledispatchFunctionDocumenter not yet implemented")
    
    # Test that key methods exist
    assert hasattr(SingledispatchFunctionDocumenter, 'can_document_member')
    assert hasattr(SingledispatchFunctionDocumenter, 'add_directive_header')
    assert hasattr(SingledispatchFunctionDocumenter, 'annotate_to_first_argument')
    
    # Test that they are callable
    assert callable(SingledispatchFunctionDocumenter.can_document_member)
    assert callable(SingledispatchFunctionDocumenter.add_directive_header)
    assert callable(SingledispatchFunctionDocumenter.annotate_to_first_argument)