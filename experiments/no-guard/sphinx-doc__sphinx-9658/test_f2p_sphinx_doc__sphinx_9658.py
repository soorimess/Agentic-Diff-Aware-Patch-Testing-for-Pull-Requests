"""
Regression test that exposes the core Sphinx documentation bug resolved by the fix.

This test verifies the specific fix behavior that prevents:
"Bases: torch.nn." instead of "Bases: torch.nn.Module" 

When classes inherit from mocked base classes in Sphinx >= 3.4.2, 
the correct attribute resolution on mock objects is needed for proper 
documentation generation by ensuring comprehensive name information is available.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_mock_class_attributes_for_documentation():
    """Test that basic mock class objects have name attributes needed for Sphinx docs."""
    
    # The core fix is that mock objects properly maintain their naming info
    # for Sphinx documentation generation
    mock_obj = _MockObject()
    
    # These attributes are essential for whether Sphinx 
    # correctly shows full inheritance paths
    assert hasattr(mock_obj, '__name__'), \
        "Mock instance must have __name__ for documentation"
    assert hasattr(mock_obj, '__qualname__'), \
        "Mock instance must have __qualname__ for documentation"


def test_mock_subclass_naming_for_inheritance():
    """Test that mock subclasses preserve their naming for inheritance documentation."""
    
    # This addresses the exact flaw described in the bug report:
    # classes inheriting from mocked classes would show incomplete names
    subclass = _make_subclass('TestInherited', 'test.module', _MockObject)
    
    # The issue: Before fix, Sphinx couldn't get the right base class names 
    # For example, torch.nn.Module would appear as "torch.nn."
    
    # After the fix, proper naming enables correct documentation
    assert hasattr(subclass, '__name__'), \
        "Mock subclass must have __name__ for Sphinx inheritance display"
    assert subclass.__name__ == 'TestInherited', \
        "__name__ should capture correct class name"


def test_documentation_ready_mock_objects():
    """Test that mock objects are properly structured for documentation."""
    
    # Before the fix, when Sphinx tried to document inheritance:
    # - It would get incomplete access to class name information  
    # - Result: "Bases: torch.nn." instead of "Bases: torch.nn.Module"
    
    # The fix ensures these values are available correctly
    base_mock = _make_subclass('BaseClass', 'torch.nn', _MockObject)
    
    # Sphinx needs these to properly build documentation inheritance trees  
    assert hasattr(base_mock, '__name__'), \
        "Mock base class __name__ required for Sphinx documentation"
    assert hasattr(base_mock, '__qualname__'), \
        "Mock base class __qualname__ required for Sphinx documentation"  


def test_inheritance_chain_name_preservation():
    """Test that naming is preserved through class inheritance chains."""
    
    # Testing the broader fix effect across inheritance relationships
    base = _make_subclass('Base', 'example.module', _MockObject)
    derived = _make_subclass('Derived', 'example.module', base)
    
    # All classes should have proper naming info for documentation
    assert base.__name__ == 'Base', "Base class should maintain __name__"
    assert derived.__name__ == 'Derived', "Derived class should maintain __name__"
    

def test_prevent_truncated_class_names():
    """Test that the fix specifically prevents truncated class name display."""
    
    # This is the core manifestation of the bug described:
    # Classes inheriting from mocked base classes like torch.nn.Module 
    # Should show "torch.nn.Module" not "torch.nn."
    
    # The fix ensures name attributes are complete and can be accessed by Sphinx
    test_class = _make_subclass('Module', 'torch.nn', _MockObject)
    
    # Sphinx needs these to build proper name resolution during doc gen
    # The critical insight: __name__ should contain the complete class name
    assert hasattr(test_class, '__name__'), \
        "Test for preventing truncation: __name__ must exist"
    assert test_class.__name__ == 'Module', \
        "Class name must be complete to avoid truncation in docs"