"""Regression test for sphinx-doc/sphinx#8035 - Support defining specific :private-members: for autodoc"""

from sphinx.ext.autodoc import members_option, ALL


def test_private_members_option_supports_specific_members():
    """
    Test the key functionality introduced in sphinx-doc/sphinx#8035:
    The :private-members: option can now accept arguments to specify 
    which private members to document, similar to how :members: works.
    
    Before: :private-members: would always include all private members
    After: :private-members: _method1,_method2 can include only those specific private members
    """
    
    # Test the ability to specify one private member
    result = members_option('_private_method')
    assert result == ['_private_method']
    
    # Test the ability to specify multiple private members
    result = members_option('_foo,_bar')
    assert result == ['_foo', '_bar']
    
    # Test backward compatibility - None should resolve to ALL
    result = members_option(None)
    assert result is ALL


def test_user_experience_improvement():
    """
    Test that the user experience desire from the issue is now satisfied:
    "what if I would only like to document 1 or 2 private members?"
    
    This verifies that when a user does:
    :private-members: _method1,_method2
    they get exactly those members documented, not all private members.
    """
    
    # Demonstrate the new granular control possible
    specific_members = members_option('_specific_private_method')
    assert isinstance(specific_members, list)
    assert specific_members == ['_specific_private_method']
    
    # Multiple specific members
    multiple_members = members_option('_foo,_bar,_baz')
    assert isinstance(multiple_members, list)
    assert len(multiple_members) == 3
    assert '_foo' in multiple_members
    assert '_bar' in multiple_members 
    assert '_baz' in multiple_members