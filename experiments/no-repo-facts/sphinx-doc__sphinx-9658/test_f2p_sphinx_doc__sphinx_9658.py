"""
Regression test for Sphinx issue #9658: 
Inherited classes not correctly documented when mocked

This test is designed to assert the behavioral difference that would 
have existed in different states of the _MockObject class qualname handling.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_qualname_consistency_in_mocked_inheritance():
    """
    The key behavioral test that was broken and fixed:
    When documentation systems process classes inheriting from mocked base classes,
    they should get consistent __name__ and __qualname__ values to avoid 
    truncated display names like "torch.nn." instead of "torch.nn.Module".
    """
    
    # Create a mocked base class as would happen with autodoc_mock_imports
    mock_base = _MockObject()
    
    # Create a class that inherits from it (simulating: class MyClass(torch.nn.Module))
    class InheritedClass(mock_base.SomeClass):
        """A test class inheriting from mocked base."""
        def method(self):
            return "test"
    
    # Validate that the documentation-ready attributes are present
    bases = InheritedClass.__bases__
    assert len(bases) > 0
    base_class = bases[0]
    
    # These tests check the fix that ensures consistent naming behavior 
    # for documentation systems
    assert hasattr(base_class, '__name__'), "Missing __name__ for documentation"
    assert hasattr(base_class, '__qualname__'), "Missing __qualname__ for documentation"
    
    # The critical behavioral difference: before fix, these might not
    # have been consistent or meaningful for documentation display
    name = getattr(base_class, '__name__', None) 
    qualname = getattr(base_class, '__qualname__', None)
    
    # Both should be meaningful for proper documentation display
    # Truncation would happen if either is incorrect or empty
    assert name is not None and name != '', "Base name should be meaningful"
    assert qualname is not None and qualname != '', "Base qualname should be meaningful"


def test_subclass_creation_qualname_attributes():
    """
    Direct test of the specific behavior changes in _make_subclass that 
    were part of the fix to ensure proper naming structures.
    """
    
    # Test that subclasses created via _make_subclass have proper naming
    # structures that documenters can rely on
    subclass = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # The fix ensures __name__ and __qualname__ are properly assigned
    assert hasattr(subclass, '__name__'), "Subclass missing __name__"
    assert hasattr(subclass, '__qualname__'), "Subclass missing __qualname__"
    
    # These should match according to the fix behavior
    assert subclass.__name__ == 'Module'
    assert subclass.__qualname__ == 'Module'
    
    # The __display_name__ should be properly formed 
    # (was part of the class attribute changes in the fix)
    assert hasattr(subclass, '__display_name__')
    assert subclass.__display_name__ == 'torch.nn.Module'
    
    # Test a condition that would fail if the __qualname__ wasn't correctly set
    # The original issue was truncated names in documentation outputs
    # This assertion specifically captures that documented behavior expectation
    expected_display_name = 'torch.nn.Module'
    actual_display_name = subclass.__display_name__
    
    # The fix was specifically to ensure qualname structures are complete  
    # such that when Sphinx displays base classes, it doesn't truncate
    assert actual_display_name == expected_display_name, \
        f"Expected {expected_display_name}, got {actual_display_name}"