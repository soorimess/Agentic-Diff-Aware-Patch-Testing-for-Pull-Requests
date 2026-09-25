"""
Regression test for sphinx-doc/sphinx issue #9658

This tests the specific name attributes that were broken in inheritance documentation
for mock classes.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mock_subclass_proper_name_attributes():
    """Test that _make_subclass correctly sets name attributes for sphinx docs."""
    
    # The core fix: _make_subclass now sets __name__ = name in attributes
    subclass = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # This is what matters for documentation rendering - no truncation
    assert subclass.__name__ == 'Module'
    assert subclass.__qualname__ == 'Module'
    
    # Make sure the key attributes exist
    assert hasattr(subclass, '__name__')
    assert hasattr(subclass, '__qualname__')


def test_mock_object_base_has_correct_name():
    """Test the basic _MockObject class has correct naming."""
    
    # This tests that the base class has working name behavior
    mock_obj = _MockObject()
    
    # The object should have name attributes that don't cause issues
    assert hasattr(mock_obj, '__name__')
    assert hasattr(mock_obj, '__qualname__')
    
    # Critical that we can access both attributes 
    # (the main assertion is that we don't crash accessing them)
    # This catches any issues with attribute handling in the code


def test_documentation_rendering_name_consistency():
    """Test name consistency needed for proper documentation rendering."""
    
    # The key behavior: mock objects used in inheritance should 
    # produce names via __name__ and __qualname__ that Sphinx can
    # properly render in "Bases" sections without truncation
    
    subclass = _make_subclass('SomeClass', 'package.module', _MockObject)
    
    # Critical for preventing "torch.nn." vs "torch.nn.Module" issue
    assert subclass.__name__ == 'SomeClass'
    assert subclass.__qualname__ == 'SomeClass'


def test_specific_mock_fix_behavior():
    """Test the specific behavior that was fixed in the mock module."""
    
    # This specifically targets the _make_subclass behavior changes
    # from the pull request that fix the sphinx documentation issue
    
    # Test the component that was changed: _make_subclass function
    subclass = _make_subclass('TestBase', 'test.module', _MockObject)
    
    # The key assertions that represent the fix:
    # - __name__ = name (was missing or set incorrectly)  
    # - __qualname__ = self.__name__ (was hardcoded to empty string)
    assert hasattr(subclass, '__name__')
    assert hasattr(subclass, '__qualname__')
    
    # This behavior ensures documentation doesn't show truncated names
    assert subclass.__name__ == 'TestBase' 
    assert subclass.__qualname__ == 'TestBase'