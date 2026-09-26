"""
Regression test for sphinx-doc/sphinx#9658

This test verifies that when classes inherit from mocked classes,
the base class names are displayed correctly in the "Bases" section
of documentation, rather than showing truncated names like "torch.nn."
instead of "torch.nn.Module".
"""

from sphinx.ext.autodoc.mock import _MockObject, _MockModule, mock


def test_mocked_class_name_attribute():
    """Test that mocked classes have proper __name__ attribute to avoid truncation."""
    
    # Create a mock module and class like torch.nn.Module
    mock_module = _MockModule('torch.nn')
    mock_module_class = mock_module.Module
    
    # Check the __name__ attribute of the mock class
    # This is what Sphinx uses to display class names in documentation
    assert hasattr(mock_module_class, '__name__')
    
    # Before the fix, __name__ might have been empty or incorrectly set
    # This would cause Sphinx to show truncated names like "torch.nn." instead of "torch.nn.Module"
    # The fix ensures __name__ is properly set
    assert mock_module_class.__name__ == 'Module'


def test_mocked_class_qualname_attribute():
    """Test that __qualname__ is properly set for mocked classes."""
    
    # Create a mock module and class
    mock_module = _MockModule('torch.nn')
    mock_module_class = mock_module.Module
    
    # Check that __qualname__ is properly set
    # The fix ensures __qualname__ matches __name__ for proper display
    assert hasattr(mock_module_class, '__qualname__')
    
    # This is the key fix: __qualname__ should equal __name__ 
    # to avoid issues with Sphinx's display logic
    assert mock_module_class.__qualname__ == mock_module_class.__name__


def test_inheritance_base_class_name():
    """Test that inheritance from mocked classes preserves full names."""
    
    # Create a mock class that represents a base class like torch.nn.Module
    mock_module = _MockModule('torch.nn')
    mock_base_class = mock_module.Module
    
    # Create a subclass that inherits from the mocked base
    class DerivedClass(mock_base_class):
        """A derived class inheriting from mocked base."""
        pass
    
    # Check the base class information
    bases = DerivedClass.__bases__
    assert len(bases) == 1
    base_class = bases[0]
    
    # The key assertion: __name__ should not be empty (which was causing truncation)
    assert hasattr(base_class, '__name__')
    assert base_class.__name__ != ''  # This was the bug - empty name caused truncation
    assert base_class.__name__ == 'Module'  # Should be the actual class name


def test_mock_object_creation():
    """Test the internal _make_subclass function behavior."""
    
    # Test creating a subclass manually using _make_subclass
    from sphinx.ext.autodoc.mock import _make_subclass
    
    # Create a mock class using _make_subclass directly
    subclass = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Check that __name__ is properly set (this was the issue)
    assert hasattr(subclass, '__name__')
    assert subclass.__name__ == 'Module'
    
    # Check that __qualname__ is also properly set
    assert hasattr(subclass, '__qualname__')
    assert subclass.__qualname__ == subclass.__name__