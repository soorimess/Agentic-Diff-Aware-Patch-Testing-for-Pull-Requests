"""
Regression test for sphinx-doc/sphinx issue #9658.

This test verifies the specific fix applied to prevent truncated base class
names when documenting classes that inherit from mocked classes.
The issue was that in sphinx >= 3.4.2, when documenting classes inheriting
from mocked classes, base class names would appear like "torch.nn." instead
of "torch.nn.Module".
"""
from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mock_object_name_attribute_set_correctly():
    """Test that _MockObject.__name__ is properly set to empty string.
    
    This was the key fix: __name__ = '' was added to _MockObject class.
    This prevents class name truncation in documentation generation.
    """
    mock_obj = _MockObject()
    
    # Before fix: __name__ was not explicitly set, leading to name truncation
    # After fix: __name__ = '' is explicitly set to prevent truncation  
    assert hasattr(mock_obj, '__name__')
    
    # The fix ensures __name__ is set to an empty string
    # This prevents sphinx from truncating qualified names during documentation
    # This is a test of the actual behavior that was fixed
    assert mock_obj.__name__ == ''


def test_make_subclass_name_attributes():
    """Test that _make_subclass correctly sets name attributes for proper doc rendering.
    
    The fix ensures subclasses have __name__ and __qualname__ attributes that
    prevent documentation truncation.
    """
    # Create a mock that simulates torch.nn.Module 
    mock_module = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # These attributes are crucial for documentation generation
    assert hasattr(mock_module, '__name__')
    assert mock_module.__name__ == 'Module'
    
    assert hasattr(mock_module, '__qualname__')
    assert mock_module.__qualname__ == 'Module'
    
    # The __display_name__ is also important for proper rendering
    assert hasattr(mock_module, '__display_name__')
    assert mock_module.__display_name__ == 'torch.nn.Module'


def test_prevents_class_name_truncation():
    """Test the core issue: prevent truncated class names like 'torch.nn.' instead of 'torch.nn.Module'.
    
    Before the fix, if __name__ was not properly set, Sphinx would show
    truncated names in the "Bases" section of documentation.
    """
    # Simulate the situation where Sphinx documents a class inheriting from a mocked base
    mock_base = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # The key test - these attributes should be set correctly so when Sphinx 
    # renders the documentation, it displays the full class name
    assert mock_base.__name__ is not None
    assert mock_base.__qualname__ is not None
    
    # Previously, if __name__ was empty or non-existent, this would cause
    # truncation in sphinx documentation rendering
    assert mock_base.__name__ != ''
    assert mock_base.__qualname__ != ''


def test_attribute_consistency_for_inheritance():
    """Test that attributes maintain consistency needed for inheritance documentation.
    
    The issue occurred with inheritance scenarios, so we test that 
    the specific attributes used by sphinx for class display are properly set.
    """
    # Create mock base class
    mock_base = _make_subclass('BaseClass', 'test.module', _MockObject)
    
    # Check all name-related attributes have the right values to prevent truncation
    assert hasattr(mock_base, '__name__')
    assert hasattr(mock_base, '__qualname__') 
    assert hasattr(mock_base, '__display_name__')
    
    # These should all be set appropriately for proper sphinx documentation
    assert mock_base.__name__ == 'BaseClass'
    assert mock_base.__qualname__ == 'BaseClass'
    assert mock_base.__display_name__ == 'test.module.BaseClass'