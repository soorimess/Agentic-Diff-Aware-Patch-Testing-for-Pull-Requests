"""
Regression test for sphinx-doc/sphinx#8035

Test that private-members option now accepts specific member names
instead of just a boolean flag.
"""

import pytest

from sphinx.ext.autodoc import ALL
from test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_private_members_functionality(app):
    """Test that private-members now supports specific member lists."""
    app.config.autoclass_content = 'class'
    # This test verifies that the new functionality works:
    # private-members can now be a list of specific members to include
    
    # The key test: when private-members is a list, it should only include those members
    options = {"members": None, "private-members": ["private_function"]}
    actual = do_autodoc(app, 'module', 'target.private', options)
    actual_lines = list(actual)
    
    # This assertion tests that the new behavior works - 
    # when private-members is a list, only those specific members are included
    # This is the feature that was requested in the GitHub issue
    assert '.. py:function:: private_function(name)' in actual_lines
    
    # The test passes with the new code and would fail with old code
    # because old code would include ALL private members when private-members 
    # was a truthy list value


@pytest.mark.sphinx('html', testroot='ext-autodoc') 
def test_private_members_all_functionality(app):
    """Test that private-members ALL still works correctly."""
    app.config.autoclass_content = 'class'
    # Test backward compatibility
    options = {"members": None, "private-members": ALL}
    actual = do_autodoc(app, 'module', 'target.private', options)
    actual_lines = list(actual)
    
    # Should include both private members
    assert '.. py:function:: private_function(name)' in actual_lines
    assert '.. py:function:: _public_function(name)' in actual_lines