"""
Regression test for sphinx-doc/sphinx#9658

This test verifies that mock objects have non-empty __qualname__ attributes
so that Sphinx documentation correctly displays full class names instead of
truncated ones like "torch.nn." instead of "torch.nn.Module".
"""

from sphinx.ext.autodoc.mock import _MockModule


def test_mock_class_qualname_is_not_empty():
    """
    Test that mock classes have non-empty __qualname__ attributes.
    
    Before the fix: mock classes had empty __qualname__ which caused
    Sphinx to display truncated names in documentation.
    
    After the fix: mock classes should have proper __qualname__ for full display.
    """
    
    # Create a mock that represents torch.nn.Module
    mock_torch_nn = _MockModule('torch.nn')
    mock_module_class = mock_torch_nn.Module
    
    # The key assertion: __qualname__ should not be empty string
    # This was the root cause of truncated display in Sphinx documentation
    qualname = getattr(mock_module_class, '__qualname__', '')
    assert qualname != '', "Mock class __qualname__ should not be empty string"


def test_mock_class_name_attributes():
    """
    Test that mock classes have proper name attributes for documentation.
    """
    
    # Create mock representing a module/class hierarchy
    mock_torch_nn = _MockModule('torch.nn')
    mock_module_class = mock_torch_nn.Module
    
    # Check that the mock class has proper name attributes
    name = getattr(mock_module_class, '__name__', '')
    qualname = getattr(mock_module_class, '__qualname__', '')
    
    # Both should be meaningful for proper documentation
    assert name != '', "Mock class __name__ should not be empty"
    assert qualname != '', "Mock class __qualname__ should not be empty"