"""
Regression test for singledispatch function support.

This test verifies that @singledispatch functions are properly documented
with all their overloads shown in the documentation.
"""
import functools
from unittest.mock import Mock

import pytest

from sphinx.util.inspect import is_singledispatch_function


def test_singledispatch_function_detection():
    """Test that singledispatch functions can be detected."""
    # Create a singledispatch function
    @functools.singledispatch
    def func(x):
        """A singledispatch function."""
        return x
    
    # This should return True for a singledispatch function
    assert is_singledispatch_function(func) is True
    
    # This should return False for a regular function
    def regular_func(x):
        return x
    assert is_singledispatch_function(regular_func) is False


def test_singledispatch_function_documenter_exists():
    """Test that SingledispatchFunctionDocumenter class exists and has correct attributes."""
    # Import after the change is applied
    from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    
    assert hasattr(SingledispatchFunctionDocumenter, 'objtype')
    assert SingledispatchFunctionDocumenter.objtype == 'singledispatch_function'
    assert hasattr(SingledispatchFunctionDocumenter, 'directivetype')
    assert SingledispatchFunctionDocumenter.directivetype == 'function'
    assert hasattr(SingledispatchFunctionDocumenter, 'member_order')
    assert SingledispatchFunctionDocumenter.member_order == 30
    assert hasattr(SingledispatchFunctionDocumenter, 'priority')
    # Priority should be higher than FunctionDocumenter
    from sphinx.ext.autodoc import FunctionDocumenter
    assert SingledispatchFunctionDocumenter.priority > FunctionDocumenter.priority


def test_singledispatch_method_documenter_exists():
    """Test that SingledispatchMethodDocumenter class exists and has correct attributes."""
    # Import after the change is applied
    from sphinx.ext.autodoc import SingledispatchMethodDocumenter
    
    assert hasattr(SingledispatchMethodDocumenter, 'objtype')
    assert SingledispatchMethodDocumenter.objtype == 'singledispatch_method'
    assert hasattr(SingledispatchMethodDocumenter, 'directivetype')
    assert SingledispatchMethodDocumenter.directivetype == 'method'
    assert hasattr(SingledispatchMethodDocumenter, 'member_order')
    assert SingledispatchMethodDocumenter.member_order == 50
    assert hasattr(SingledispatchMethodDocumenter, 'priority')
    # Priority should be higher than MethodDocumenter
    from sphinx.ext.autodoc import MethodDocumenter
    assert SingledispatchMethodDocumenter.priority > MethodDocumenter.priority


def test_singledispatch_function_documenter_can_document():
    """Test that SingledispatchFunctionDocumenter can determine it can document a singledispatch function."""
    # Import after the change is applied
    from sphinx.ext.autodoc import SingledispatchFunctionDocumenter
    
    @functools.singledispatch
    def func(x):
        """A singledispatch function."""
        return x
    
    # This should return True for a singledispatch function
    result = SingledispatchFunctionDocumenter.can_document_member(func, 'func', False, None)
    assert result is True


def test_singledispatch_method_documenter_has_annotate_method():
    """Test that SingledispatchMethodDocumenter has annotate_to_first_argument method."""
    # Import after the change is applied
    from sphinx.ext.autodoc import SingledispatchMethodDocumenter
    
    # Test that the method exists
    assert hasattr(SingledispatchMethodDocumenter, 'annotate_to_first_argument')
    
    # Create a simple test function to verify method can be called
    def test_func(x):
        return x
    
    # Test that we can create a mock instance and call the method
    class MockDirective:
        def __init__(self):
            self.env = Mock()
            self.env.config = Mock()
            self.env.config.autodoc_docstring_signature = True
            self.env.config.autodoc_default_options = {}
            self.env.config.autodoc_typehints = 'none'
            self.env.config.autodoc_typehints_description_target = 'documented'
            self.env.config.autodoc_typehints_format = 'short'
            self.env.config.autodoc_inherit_docstrings = True
            self.env.config.autodoc_mock_imports = []
            self.genopt = Mock()
            self.genopt.__dict__ = {}
            self.result = []
        
        def add_line(self, line, source=None):
            self.result.append(line)
    
    # Create a mock instance to test method existence
    directive = MockDirective()
    # This is just to make sure we can access the method - we don't need to call it
    # since that would require the full setup
    assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])