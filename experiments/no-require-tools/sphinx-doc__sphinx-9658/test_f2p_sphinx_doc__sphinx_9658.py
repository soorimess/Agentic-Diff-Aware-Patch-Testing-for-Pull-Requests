"""
Regression test for sphinx-doc/sphinx #9658 - for inherited class documentation naming

This test will fail on the pre-fix code and pass on the fixed code.
It focuses on the specific core behavioral difference that was fixed.
"""

from sphinx.ext.autodoc.mock import _MockObject, _make_subclass


def test_inheritance_base_class_name_resolution():
    """
    Test that mock objects used to document inherited classes have correct
    name attributes to prevent truncated display names in documentation.
    
    Before fix: Classes inheriting mocked classes would show base names like 
    "torch.nn." instead of "torch.nn.Module"
    """
    
    # Create a mock subclass representing an inherited base class
    # This is the case that was failing - Sphinx documenting inheritance hierarchies
    mock_inherited = _make_subclass("Module", "torch.nn", _MockObject)
    
    # The fix ensures these attributes are correctly set so that when Sphinx
    # builds documentation display, there's no truncation
    
    # Critical check: verify __name__ is properly assigned (ensures the patch line 77 works)
    assert hasattr(mock_inherited, '__name__')
    assert mock_inherited.__name__ == "Module"
    
    # Critical check: verify __qualname__ correctly uses __name__ (ensures patch line 44 works)  
    assert hasattr(mock_inherited, '__qualname__')
    assert mock_inherited.__qualname__ == "Module"
    
    # Critical check: verify __display_name__ is constructed properly (ensures the full namespace is preserved)
    assert hasattr(mock_inherited, '__display_name__') 
    assert mock_inherited.__display_name__ == "torch.nn.Module"
    
    # The fix ensures that __qualname__ gets value from __name__ - this prevents
    # the case where qualname resolution fails resulting in incomplete display