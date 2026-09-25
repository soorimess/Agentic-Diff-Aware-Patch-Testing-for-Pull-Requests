"""
Regression test for sphinx-doc/sphinx#9658

This test validates the fix to ensure that when documenting classes that 
inherit from mocked classes, the base class names are displayed correctly
and not truncated (e.g., "torch.nn.Module" not "torch.nn.").
"""
from sphinx.ext.autodoc.mock import _MockObject


def test_mock_object_qualname_not_empty():
    """
    Test that ensures MockObject instances have __qualname__ that is not 
    an empty string, which prevents truncated class displays in Sphinx docs.
    
    This was the root cause of sphinx-doc/sphinx#9658 where documentation
    showed "Bases: torch.nn." instead of "Bases: torch.nn.Module".
    
    Before the fix: __qualname__ was set to empty string ''
    After the fix: __qualname__ is set properly to avoid truncation issues
    """
    # Create a _MockObject - this was the source of the problematic behavior
    mock_obj = _MockObject()
    
    # The core issue was that __qualname__ would be empty string '' instead of meaningful value
    # This caused rendering problems in Sphinx documentation of class inheritance
    assert mock_obj.__qualname__ != ''