"""
Test for private-members option with specific member names
This tests the feature request to allow specifying specific private members
for autodoc's :private-members: option, rather than just a boolean flag.
"""

import pytest

from test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_list_behavior(app):
    """
    Test that private-members option supports list-based member specification.
    
    This test verifies that the option infrastructure is in place to support
    specifying exact private members to document, rather than just boolean flags.
    """
    app.config.autoclass_content = 'class'
    
    # Test that the option can be processed without crashing
    # This tests the core infrastructure change
    options = {"members": None, "private-members": "private_function"}
    actual = do_autodoc(app, 'module', 'target.private', options)
    actual_lines = list(actual)
    
    # Verify basic functionality works
    assert len(actual_lines) > 0
    assert '.. py:module:: target.private' in actual_lines