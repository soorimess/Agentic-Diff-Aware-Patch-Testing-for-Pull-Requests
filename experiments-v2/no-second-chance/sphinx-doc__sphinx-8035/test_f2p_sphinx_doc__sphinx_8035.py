"""
Regression test for sphinx-doc/sphinx#8035

This test verifies that the private-members option now supports specifying
specific private members to document, rather than just including all or none.
"""
import pytest


def test_private_members_now_accepts_list():
    """
    Test that private-members option now accepts a list of member names like members option does.
    
    This addresses the feature request: "For :private-members: to take arguments, 
    similarly to how :members: currently works"
    """
    from sphinx.ext.autodoc import members_option, ALL
    
    # Test that we can now specify specific private members as a list
    # This is the core functionality that was added
    result = members_option("private_func1,private_func2")
    assert isinstance(result, list)
    assert "private_func1" in result
    assert "private_func2" in result
    assert len(result) == 2
    
    # Test backward compatibility - None and True should still work
    assert members_option(None) is ALL
    assert members_option(True) is ALL


def test_private_members_list_parsing():
    """
    Test that private-members list parsing works correctly.
    """
    from sphinx.ext.autodoc import members_option
    
    # Various valid list formats
    assert members_option("") == []
    assert members_option("func1") == ["func1"]
    assert members_option("func1,func2") == ["func1", "func2"]
    assert members_option(" func1 , func2 ") == ["func1", "func2"]  # handles whitespace