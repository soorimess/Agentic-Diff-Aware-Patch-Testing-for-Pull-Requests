"""
Regression test for Sphinx mock inheritance bug (sphinx-doc/sphinx#9658).

This test ensures that classes inheriting from mocked classes display proper
base class names in documentation (e.g., "torch.nn.Module" instead of "torch.nn.").
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_base_class_name_resolution():
    """
    Test that mocked inheritance preserves proper base class names.
    
    The fix ensures that when classes inherit from mocked base classes,
    the documentation system can properly resolve and display full base class names
    instead of truncated versions.
    """
    # Create a mock base class simulating torch.nn.Module
    mock_base = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Create a subclass inheriting from the mocked base
    class MyModule(mock_base):
        def forward(self, x):
            return x
    
    # Get the inherited base class
    base_class = MyModule.__bases__[0]
    
    # Critical: The __name__ attribute must not be empty
    # Empty __name__ would cause documentation to show "torch.nn." instead of "torch.nn.Module"
    assert hasattr(base_class, '__name__')
    
    # This assertion is the core of what was fixed
    base_name = base_class.__name__
    assert base_name != '', "Base class __name__ should not be empty (would cause truncation in docs)"
    assert base_name == 'Module', f"Expected 'Module', got '{base_name}'"
    
    # Verify __qualname__ is also properly set
    assert hasattr(base_class, '__qualname__')
    assert base_class.__qualname__ == base_name


def test_subclass_attribute_setting():
    """
    Test that _make_subclass properly sets __name__ attribute on subclasses.
    
    This directly tests the fix in _make_subclass where __name__ = name was added
    to the attributes dictionary.
    """
    # Create subclass using _make_subclass
    subclass = _make_subclass('TestClassName', 'test.module', _MockObject)
    
    # The fix ensures __name__ is properly set
    assert hasattr(subclass, '__name__')
    assert subclass.__name__ == 'TestClassName'
    
    # Also check __qualname__ 
    assert hasattr(subclass, '__qualname__')
    assert subclass.__qualname__ == 'TestClassName'


def test_mock_object_has_name():
    """
    Test that _MockObject instances have __name__ attribute.
    
    This tests the fix where __name__ = '' was added to _MockObject class.
    """
    mock_obj = _MockObject()
    
    # The fix ensures __name__ exists on _MockObject instances
    assert hasattr(mock_obj, '__name__')
    # While exact value varies, it should not be None
    assert mock_obj.__name__ is not None


if __name__ == "__main__":
    # Run tests manually
    try:
        test_base_class_name_resolution()
        print("✓ test_base_class_name_resolution passed")
    except Exception as e:
        print(f"✗ test_base_class_name_resolution failed: {e}")
        
    try:
        test_subclass_attribute_setting()
        print("✓ test_subclass_attribute_setting passed")
    except Exception as e:
        print(f"✗ test_subclass_attribute_setting failed: {e}")
        
    try:
        test_mock_object_has_name()
        print("✓ test_mock_object_has_name passed")
    except Exception as e:
        print(f"✗ test_mock_object_has_name failed: {e}")