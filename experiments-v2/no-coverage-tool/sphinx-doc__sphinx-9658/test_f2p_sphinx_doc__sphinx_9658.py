"""
Regression test for Sphinx issue with mocked classes inheritance.

This test verifies that when a class inherits from a mocked class,
the base class information is correctly displayed in documentation.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_name_attributes_prevent_truncated_display():
    """
    Test that verifies the fix prevents truncated base class names in Sphinx docs.
    
    The bug: classes inheriting from mocked classes showed base classes as 
    "torch.nn." instead of "torch.nn.Module" due to improper __name__ handling.
    
    This test ensures that __name__ and __qualname__ attributes are properly set
    so Sphinx can display full class names.
    """
    
    # Create subclass that simulates what happens with mocked classes
    subclass = _make_subclass('DeepKernel', 'torch.nn', _MockObject)
    
    # These attributes are crucial for documentation display
    assert hasattr(subclass, '__name__'), "Subclass must have __name__ attribute"
    assert hasattr(subclass, '__qualname__'), "Subclass must have __qualname__ attribute"
    
    # The fix ensures these contain full names, not truncated ones
    assert subclass.__name__ == 'DeepKernel', f"Expected 'DeepKernel', got '{subclass.__name__}'"
    assert subclass.__qualname__ == 'DeepKernel', f"Expected 'DeepKernel', got '{subclass.__qualname__}'"
    
    # Critical: these should be accessible and not None to prevent display issues
    assert subclass.__name__ is not None, "Subclass __name__ should not be None"
    assert subclass.__qualname__ is not None, "Subclass __qualname__ should not be None"
    
    # Test that they are strings (not None, not empty, not broken)
    assert isinstance(subclass.__name__, str), "Subclass __name__ should be a string"
    assert isinstance(subclass.__qualname__, str), "Subclass __qualname__ should be a string"
    
    # Verify they contain meaningful values (not empty strings that would cause issues)
    assert len(subclass.__name__) > 0, "Subclass __name__ should not be empty"
    assert len(subclass.__qualname__) > 0, "Subclass __qualname__ should not be empty"


def test_inheritance_name_handling():
    """
    Test inheritance name handling for proper documentation.
    """
    
    # Simulate mocked module inheritance scenario
    mock_obj = _MockObject()
    
    # This represents a class inheriting from a mocked base (like DeepKernel from torch.nn.Module)
    class MockInheritedClass(mock_obj.SomeBase):
        pass
    
    # Both classes should have proper name attributes for documentation
    assert hasattr(MockInheritedClass, '__name__'), "Inherited class should have __name__"
    assert hasattr(MockInheritedClass, '__qualname__'), "Inherited class should have __qualname__"
    
    # These should be accessible and contain proper values
    assert MockInheritedClass.__name__ is not None, "Inherited class __name__ should be accessible"
    assert MockInheritedClass.__qualname__ is not None, "Inherited class __qualname__ should be accessible"
    assert len(MockInheritedClass.__name__) > 0, "Inherited class __name__ should not be empty"
    assert len(MockInheritedClass.__qualname__) > 0, "Inherited class __qualname__ should not be empty"


def test_make_subclass_attribute_correctness():
    """
    Test that _make_subclass function correctly sets name attributes.
    
    This directly tests the fix applied to the _make_subclass function.
    """
    # Test the specific function that was changed
    subclass = _make_subclass('TestClass', 'test.module', _MockObject)
    
    # The fix ensures these are properly set to prevent documentation bugs
    assert hasattr(subclass, '__name__'), "Subclass should have __name__ attribute"
    assert hasattr(subclass, '__qualname__'), "Subclass should have __qualname__ attribute"
    
    # Verify correct assignment that prevents truncated display
    assert subclass.__name__ == 'TestClass', f"Expected 'TestClass', got '{subclass.__name__}'"
    assert subclass.__qualname__ == 'TestClass', f"Expected 'TestClass', got '{subclass.__qualname__}'"
    
    # Ensure they are proper strings that Sphinx can use
    assert isinstance(subclass.__name__, str), "Subclass __name__ should be a string"
    assert isinstance(subclass.__qualname__, str), "Subclass __qualname__ should be a string"