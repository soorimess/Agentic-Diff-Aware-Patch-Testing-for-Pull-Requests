"""
Regression test for sphinx-doc/sphinx#9658
Test that inherited classes are correctly documented when mocked.
This tests the specific issue where base classes show as "torch.nn." instead of "torch.nn.Module"
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mock_subclass_name_attributes():
    """Test that mock subclasses have correct name attributes for documentation.
    
    The fix ensures that name attributes are properly set so that Sphinx
    documentation generation works correctly for inherited classes.
    """
    
    # Create a mock class that represents torch.nn.Module
    mock_module = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # The __name__ should be set to the actual class name
    assert mock_module.__name__ == 'Module'
    
    # The __qualname__ should be set to the actual class name (not empty string)
    # This is the key fix - it should not be empty string when it has a meaningful value
    assert mock_module.__qualname__ == 'Module'
    
    # Both should exist and be set
    assert hasattr(mock_module, '__name__')
    assert hasattr(mock_module, '__qualname__')
    
    # The __display_name__ should be properly formed
    assert mock_module.__display_name__ == 'torch.nn.Module'


def test_inheritance_scenarios():
    """Test inheritance scenarios that were broken before the fix."""
    
    # Create a mock base class (simulating torch.nn.Module)
    mock_module = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Create a subclass that inherits from the mocked base
    mock_deep_kernel = _make_subclass('DeepKernel', 'alibi_detect.utils.pytorch.kernels', 
                                      mock_module)
    
    # Check that the subclass has proper name attributes for documentation
    assert mock_deep_kernel.__name__ == 'DeepKernel'
    assert mock_deep_kernel.__qualname__ == 'DeepKernel'
    assert mock_deep_kernel.__display_name__ == 'alibi_detect.utils.pytorch.kernels.DeepKernel'
    
    # Check that the base class has proper name attributes
    assert mock_module.__name__ == 'Module'
    assert mock_module.__qualname__ == 'Module'
    assert mock_module.__display_name__ == 'torch.nn.Module'


def test_name_attribute_consistency():
    """Test that name attributes are properly set and consistent.
    
    This specifically tests that __qualname__ is not empty string when it should have a value.
    """
    
    # Test with a subclass that has a real name
    mock_class = _make_subclass('Test', 'test.module', _MockObject)
    
    # Both __name__ and __qualname__ should be set to the actual name
    assert mock_class.__name__ == 'Test'
    assert mock_class.__qualname__ == 'Test'
    
    # They should be consistent
    assert mock_class.__name__ == mock_class.__qualname__
    
    # The __qualname__ should not be empty string when it has a meaningful value
    assert mock_class.__qualname__ != ''
    
    # __module__ should be set correctly
    assert mock_class.__module__ == 'test.module'
    
    # __display_name__ should be set correctly
    assert mock_class.__display_name__ == 'test.module.Test'