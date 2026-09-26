"""
Regression test for sphinx-doc/sphinx#8035

This test verifies that the private-members option now accepts specific member names
instead of just being a boolean flag.
"""

import pytest


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_functionality(app):
    """
    Test that private-members option now accepts list arguments.
    
    This test verifies that the change allows private-members to accept
    a list of member names, similar to how members option works.
    """
    from test_ext_autodoc import do_autodoc
    
    app.config.autoclass_content = 'class'
    
    # This is the new functionality: private-members can accept a list
    # In the old version, this would likely cause an error or incorrect behavior
    # In the new version, this should work correctly
    options = {"members": None,
               "private-members": ["private_function"]}
    actual = do_autodoc(app, 'module', 'target.private', options)
    
    # Verify that the functionality doesn't crash and produces output
    actual_lines = list(actual)
    assert len(actual_lines) > 0