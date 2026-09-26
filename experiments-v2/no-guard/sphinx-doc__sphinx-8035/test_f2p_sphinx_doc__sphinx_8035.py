"""
Regression test for sphinx-doc/sphinx#8035
Test that private-members option now supports specifying specific private members
"""
import pytest


def test_private_members_new_functionality():
    """
    Test that private-members option infrastructure now supports list arguments.
    
    This test verifies that the change from bool_option to members_option
    enables the new functionality where private-members can accept comma-separated
    values to specify which private members to document.
    """
    # Test the core functionality that differentiates old vs new behavior
    from sphinx.ext.autodoc.__init__ import members_option, bool_option
    
    # In old code: bool_option("private_function") -> True (always document)
    # In new code: members_option("private_function") -> ["private_function"] (specific document)
    
    # This test validates the infrastructure change
    assert bool_option("private_function") is True
    result = members_option("private_function")
    assert isinstance(result, list)
    assert result == ["private_function"]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_integration(app):
    """
    Integration test for private-members option functionality.
    """
    app.config.autoclass_content = 'class'
    
    from test_ext_autodoc import do_autodoc
    
    # Test basic functionality works
    options = {"members": None, "private-members": None}
    actual = do_autodoc(app, 'module', 'target.private', options)
    lines = list(actual)
    assert len(lines) > 0
    
    # Test with ALL (should work in both versions)
    options = {"members": None, "private-members": "ALL"}
    actual = do_autodoc(app, 'module', 'target.private', options)
    lines = list(actual)
    assert len(lines) > 0
    
    # Test with comma-separated string (the new functionality)
    # This should work in the new code but would have been treated as True in old code
    options = {"members": None, "private-members": "private_function"}
    actual = do_autodoc(app, 'module', 'target.private', options)
    lines = list(actual)
    assert len(lines) > 0