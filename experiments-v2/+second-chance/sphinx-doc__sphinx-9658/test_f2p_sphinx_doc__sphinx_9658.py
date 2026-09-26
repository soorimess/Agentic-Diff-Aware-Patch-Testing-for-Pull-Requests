"""
Regression test for sphinx-doc/sphinx#9658

This test verifies that when classes inherit from mocked classes,
the documentation properly shows the base class name instead of
truncated/incorrect names like "torch.nn." instead of "torch.nn.Module".
"""

from sphinx.ext.autodoc.mock import _MockObject, _MockModule, _make_subclass


def test_mock_class_name_attribute():
    """
    Test that mock classes have proper __name__ attribute.
    
    The core issue: when Sphinx documents inheritance from mocked classes,
    it uses the __name__ attribute to determine what to display.
    Before the fix, __name__ was not properly set, causing truncated names.
    """
    # Create a mock module like torch.nn
    mock_module = _MockModule('torch.nn')
    
    # Create a mock class like torch.nn.Module
    mock_module_class = mock_module.Module
    
    # The key assertion: __name__ should be 'Module', not something malformed
    # This is what causes the bug where "Bases: torch.nn." shows instead of "Bases: torch.nn.Module"
    assert hasattr(mock_module_class, '__name__')
    
    # The __name__ should be just 'Module', not 'torch.nn.Module.__name__' or empty
    actual_name = getattr(mock_module_class, '__name__', None)
    assert actual_name is not None
    assert actual_name != ''
    assert actual_name == 'Module', f"Expected __name__ to be 'Module', got '{actual_name}'"


def test_mock_subclass_creation():
    """
    Test that _make_subclass properly sets __name__ attribute.
    
    This directly tests the fix in the _make_subclass function.
    """
    # Test the _make_subclass function directly
    subclass = _make_subclass('TestSubclass', 'test.module', _MockObject)
    
    # The fix ensures __name__ is properly set
    assert hasattr(subclass, '__name__')
    assert subclass.__name__ == 'TestSubclass'
    
    # Test that __qualname__ is also set correctly
    assert hasattr(subclass, '__qualname__')
    assert subclass.__qualname__ == 'TestSubclass'
    
    # Test that __display_name__ is also set correctly  
    assert hasattr(subclass, '__display_name__')
    assert subclass.__display_name__ == 'test.module.TestSubclass'


def test_inheritance_name_display():
    """
    Test that inheritance properly preserves class names for documentation.
    
    This simulates what Sphinx does when documenting classes that inherit
    from mocked classes.
    """
    # Create a mock module like torch.nn
    mock_module = _MockModule('torch.nn')
    
    # Create a mock class like torch.nn.Module
    mock_module_class = mock_module.Module
    
    # Create a class that inherits from the mock class
    class TestInherited(mock_module_class):
        """Test class inheriting from mocked Module."""
        pass
    
    # The base class should have a proper __name__ for documentation
    base_class = TestInherited.__bases__[0]
    
    # This is what Sphinx uses to display the base class name in "Bases" section
    assert hasattr(base_class, '__name__')
    assert base_class.__name__ == 'Module'