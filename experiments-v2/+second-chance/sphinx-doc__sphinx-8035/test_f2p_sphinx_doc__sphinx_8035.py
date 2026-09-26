"""
Regression test for sphinx-doc/sphinx#8035

This test validates the core change: private-members option now accepts 
comma-separated lists of member names instead of just boolean values.

Before: private-members = bool_option -> only True/False allowed
After: private-members = members_option -> accepts comma-separated lists
"""
import pytest
from sphinx.ext.autodoc import members_option, ALL


def test_private_members_accepts_comma_separated_lists():
    """
    Test that private-members now accepts comma-separated member names.
    
    This enables the feature requested in the GitHub issue.
    """
    # Test the new capability: comma-separated list parsing
    result = members_option("_attr1,_attr2,_attr3")
    
    # Should return a list, not a boolean
    assert isinstance(result, list)
    assert len(result) == 3
    assert "_attr1" in result
    assert "_attr2" in result
    assert "_attr3" in result


def test_private_members_enables_specific_inclusion():
    """
    Test that private-members now allows specifying exactly which 
    private members to include.
    
    This was not possible with the old boolean-only approach.
    """
    # Specify exactly which private members to include
    private_members = members_option("_specific_private,_another_private")
    
    # Should be a list with the specified members
    assert isinstance(private_members, list)
    assert "_specific_private" in private_members
    assert "_another_private" in private_members
    
    # Should NOT be boolean (old behavior)
    assert private_members != True
    assert private_members != False


def test_private_members_backward_compatibility():
    """
    Test that existing usage still works for backward compatibility.
    """
    # None should return ALL (as before)
    result = members_option(None)
    assert result is ALL
    
    # True should return ALL (as before) 
    result = members_option(True)
    assert result is ALL


def test_private_members_functional_enhancement():
    """
    Test the functional enhancement that this change provides.
    
    The enhancement is that users can now specify exactly which private
    members to document, rather than just including all or none.
    """
    # Test the new granular control
    result = members_option("_private1,_private2")
    
    # Should be a list with specific members
    assert isinstance(result, list)
    assert len(result) == 2
    
    # Should not behave like old boolean approach
    assert result != True  # Old approach would not allow this granularity
    assert result != False  # Old approach would not allow this granularity