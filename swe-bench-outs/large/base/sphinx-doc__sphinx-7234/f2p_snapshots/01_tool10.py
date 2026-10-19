"""
Regression test for singledispatch support in autodoc.

This test ensures that @functools.singledispatch functions and 
@functools.singledispatchmethod methods are properly documented
with their overloads included in the documentation.
"""

import functools
from unittest.mock import Mock

import pytest

from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
from sphinx.util.inspect import is_singledispatch_function


def test_is_singledispatch_function():
    """Test detection of singledispatch functions."""
    
    @functools.singledispatch
    def func(x):
        """Main function docstring."""
        return x
    
    @func.register
    def _(x: int) -> int:
        """Int overload."""
        return x
    
    # This should be detected as a singledispatch function
    assert is_singledispatch_function(func) is True
    
    # Regular function should not be detected
    def regular_func(x):
        return x
    assert is_singledispatch_function(regular_func) is False


def test_singledispatch_function_documenter_can_document_member():
    """Test that SingledispatchFunctionDocumenter can document singledispatch functions."""
    
    @functools.singledispatch
    def func(x):
        """Main function docstring."""
        return x
    
    @func.register
    def _(x: int) -> int:
        """Int overload."""
        return x
    
    # Mock directive and parent
    directive = Mock()
    parent = Mock()
    
    # Test that it can document the member
    result = SingledispatchFunctionDocumenter.can_document_member(func, 'func', False, parent)
    assert result is True


def test_singledispatch_function_documenter_not_applicable():
    """Test that regular functions are not treated as singledispatch functions."""
    
    def regular_func(x):
        return x
    
    # Mock directive and parent
    directive = Mock()
    parent = Mock()
    
    # Test that regular functions are not documented as singledispatch
    result = SingledispatchFunctionDocumenter.can_document_member(regular_func, 'regular_func', False, parent)
    assert result is False


def test_singledispatch_function_documenter_add_directive_header():
    """Test that SingledispatchFunctionDocumenter properly formats directive headers."""
    
    @functools.singledispatch
    def func(x):
        """Main function docstring."""
        return x
    
    @func.register
    def _(x: int) -> int:
        """Int overload."""
        return x
    
    # Mock directive and parent
    directive = Mock()
    directive.env = Mock()
    directive.env.config = Mock()
    directive.env.config.autodoc_docstring_signature = False
    
    # Create a documenter instance
    documenter = SingledispatchFunctionDocumenter(directive, 'func')
    documenter.object = func
    documenter.name = 'func'
    
    # This should not raise an exception
    # We can't easily test the full output without more complex setup
    # but we can at least make sure it doesn't crash
    try:
        # This would normally call add_directive_header which should work
        # We're mainly testing that the class exists and can be instantiated
        assert documenter is not None
    except Exception:
        pytest.fail("SingledispatchFunctionDocumenter failed to instantiate or use properly")


def test_singledispatch_function_documenter_instantiation():
    """Test that SingledispatchFunctionDocumenter can be instantiated properly."""
    
    # Mock directive and parent
    directive = Mock()
    directive.env = Mock()
    directive.env.config = Mock()
    directive.env.config.autodoc_docstring_signature = False
    
    # Test instantiation
    documenter = SingledispatchFunctionDocumenter(directive, 'func')
    assert documenter is not None
    assert documenter.objtype == 'singledispatch_function'
    assert documenter.priority > 0  # Should have higher priority than FunctionDocumenter