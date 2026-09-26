"""
Regression test for Sphinx issue #9658
This test verifies that mock objects have proper __qualname__ attribute
to prevent incorrect documentation display.
"""

from sphinx.ext.autodoc.mock import _MockObject


def test_mock_object_qualname_is_not_empty_string():
    """
    Test that _MockObject.__qualname__ is not empty string.
    
    This test was failing before the fix for Sphinx issue #9658 where
    _MockObject.__qualname__ was incorrectly set to empty string ''.
    """
    # Create a _MockObject instance
    mock_obj = _MockObject()
    
    # Before the fix, this would be empty string causing incomplete documentation
    # After the fix, this should be set properly
    qualname = mock_obj.__qualname__
    
    # The key assertion: __qualname__ should not be empty string
    # This would have caused the bug where "torch.nn." was displayed instead of "torch.nn.Module"
    assert qualname != '', "MockObject __qualname__ should not be empty string"
    assert qualname is not None, "MockObject __qualname__ should be accessible"


def test_inheritance_base_class_names():
    """
    Test that inherited classes show correct base names in documentation.
    
    This tests the specific bug scenario from the issue report.
    """
    from sphinx.ext.autodoc.mock import _make_subclass
    
    # Create mock base class like torch.nn.Module
    mock_base = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Create a derived class inheriting from the mock base
    class Derived(mock_base):
        pass
    
    # Test that base class has proper naming for documentation display
    base_class = Derived.__bases__[0]
    
    # Both __name__ and __qualname__ should be accessible and meaningful
    assert hasattr(base_class, '__name__')
    assert hasattr(base_class, '__qualname__')
    
    # The __name__ should not be empty (would cause incomplete display)
    assert base_class.__name__ != '', "Base class __name__ should not be empty string"
    
    # The __qualname__ should also be proper (would have been empty string before fix)
    assert base_class.__qualname__ != '', "Base class __qualname__ should not be empty string"


def test_mock_object_attributes_exist():
    """
    Test that all required mock object attributes exist for Sphinx documentation.
    """
    mock_obj = _MockObject()
    
    # All these attributes should exist and be accessible
    assert hasattr(mock_obj, '__name__')
    assert hasattr(mock_obj, '__qualname__') 
    assert hasattr(mock_obj, '__module__')
    
    # The __qualname__ should be accessible (this is what was fixed)
    qualname = getattr(mock_obj, '__qualname__', None)
    assert qualname is not None, "MockObject __qualname__ should be accessible"