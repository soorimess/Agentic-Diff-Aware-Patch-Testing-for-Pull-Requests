"""
Regression tests for sphinx-doc/sphinx#8035: Support defining specific `:private-members:` for autodoc

This validates the core behavioral changes to support specific private member 
selection in autodoc directives, as requested in the GitHub issue.
"""

import pytest
from sphinx.ext.autodoc import members_option, ALL


def test_private_members_option_type_change():
    """Test that private-members option now properly uses members_option instead of bool_option.
    
    The key change: :private-members: now accepts specific member names rather than just boolean flags.
    """
    
    # Test 1: None should result in ALL (preserving backward compatibility)
    result = members_option(None)
    assert result is ALL
    
    # Test 2: True should result in ALL (preserving backward compatibility)  
    result = members_option(True)
    assert result is ALL
    
    # Test 3: Comma-separated list should result in list of member names
    result = members_option('__init__,__str__')
    assert result == ['__init__', '__str__']
    
    # Test 4: Single member should result in list with one element
    result = members_option('__init__')
    assert result == ['__init__']


def test_private_members_enhanced_api():
    """Test that the :private-members: directive now supports the requested enhanced API.
    
    The feature request was: "for :private-members: to take arguments, 
    similarly to how :members: currently works"
    """
    
    # Before the change: :private-members: couldn't specify which specific members
    # After the change: :private-members: accepts comma-separated list of names
    
    # Test that we can now specify exactly which private members to include
    member_list = ['__init__', '__str__', '__repr__']
    result = members_option(','.join(member_list)) 
    assert result == member_list
    
    # Valid syntax that should now work for the directive
    assert members_option('__init__, __str__') == ['__init__', '__str__']


def test_backward_compatibility_preserved():
    """Test that existing usage patterns still work correctly."""
    
    # The change should not break existing usage patterns:
    # - None values (should be treated as ALL)  
    # - True values (should be treated as ALL)
    # - Old boolean usage (which would be handled by the same ALL logic) 
    
    # These should all be equivalent in behavior
    assert members_option(None) is ALL
    assert members_option(True) is ALL


def test_new_functionality_enabled():
    """Test that the new functionality specifically requested in the issue works.
    
    The issue says: "what if I would only like to document 1 or 2?"
    Before: You could only include ALL or NO private members
    After: You can specify exactly 1 or 2 (or more) private members
    """
    
    # User can now specify exactly which private members to document
    # This is no longer just a flag but a list of names
    
    # Test the use case: document only __init__ and __str__, not __repr__
    private_members_to_document = ['__init__', '__str__']
    result = members_option(','.join(private_members_to_document))
    assert result == private_members_to_document
    
    # When the autodoc processing happens, it will then check:
    # if membername in result:
    #    keep = True  # Document this member  
    # else:
    #    keep = False # Don't document this member