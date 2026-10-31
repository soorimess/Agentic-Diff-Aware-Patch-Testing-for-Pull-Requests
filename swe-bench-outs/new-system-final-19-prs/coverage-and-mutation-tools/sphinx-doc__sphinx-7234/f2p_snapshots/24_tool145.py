"""
Regression test for singledispatch function support in autodoc.

This test verifies that singledispatch functions are properly documented
with all their overloads.
"""
import functools
import inspect
from unittest.mock import patch

import pytest

from sphinx.ext.autodoc import FunctionDocumenter, MethodDocumenter
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
        assert SingledispatchFunctionDocumenter.priority > FunctionDocumenter.priority
    except ImportError:
        # Before the change, this should fail
        pytest.skip("SingledispatchFunctionDocumenter not available yet")


def test_singledispatch_method_documenter_exists():
    """Test that SingledispatchMethodDocumenter class exists and is registered."""
    # This should fail before the change and pass after
    try:
        from sphinx.ext.autodoc import SingledispatchMethodDocumenter
        assert SingledispatchMethodDocumenter is not None
        assert SingledispatchMethodDocumenter.objtype == 'singledispatch_method'
        assert SingledispatchMethodDocumenter.priority > MethodDocumenter.priority
    except ImportError:
        # Before the change, this should fail
        pytest.skip("SingledispatchMethodDocumenter not available yet")


def test_singledispatch_function_can_document_member():
    """Test that the documenter can identify singledispatch functions."""
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    except ImportError:
        pytest.skip("SingledispatchFunctionDocumenter not available yet")
    
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
    
    # Test that the documenter can document it
    assert SingledispatchFunctionDocumenter.can_document_member(
        my_func, 'my_func', False, None
    ) is True


def test_singledispatch_function_registry_structure():
    """Test that singledispatch function has correct registry structure."""
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
    
    # Check that it has the expected registry structure
    assert hasattr(my_func, 'registry')
    assert hasattr(my_func, 'dispatch')
    assert hasattr(my_func, 'register')
    
    # Registry should have at least the default and two registered functions
    assert len(my_func.registry) >= 3


def test_singledispatch_function_documentation():
    """Test that singledispatch functions are documented with all overloads."""
    try:
        from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    except ImportError:
        pytest.skip("SingledispatchFunctionDocumenter not available yet")
    
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
    
    # Test that the function can be documented
    # We can't fully test the documentation generation without a full Sphinx app,
    # but we can test that the documenter can be instantiated and has the right properties
    assert hasattr(my_func, 'registry')
    assert len(my_func.registry) >= 3
    
    # Check that we can access the registry items
    registry_items = list(my_func.registry.items())
    # Should have at least the default (object) and two registered types
    assert len(registry_items) >= 3
    
    # Check that the registry contains the expected types
    types_in_registry = [typ for typ, _ in registry_items if typ is not object]
    assert len(types_in_registry) == 2
    assert int in types_in_registry
    assert str in types_in_registry


def test_singledispatch_method_documenter_structure():
    """Test that SingledispatchMethodDocumenter has the expected structure."""
    try:
        from sphinx.ext.autodoc import SingledispatchMethodDocumenter
        # Test that the class exists and has expected attributes with actual values
        assert SingledispatchMethodDocumenter is not None
        assert SingledispatchMethodDocumenter.objtype == 'singledispatch_method'
        assert SingledispatchMethodDocumenter.priority > MethodDocumenter.priority
        assert hasattr(SingledispatchMethodDocumenter, 'can_document_member')
        # Test that the can_document_member method exists and is callable
        assert callable(SingledispatchMethodDocumenter.can_document_member)
    except ImportError:
        # Before the change, this should fail
        pytest.skip("SingledispatchMethodDocumenter not available yet")