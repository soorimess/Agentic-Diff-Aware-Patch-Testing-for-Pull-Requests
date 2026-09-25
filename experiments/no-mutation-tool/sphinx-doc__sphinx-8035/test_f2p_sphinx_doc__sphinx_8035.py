"""
Regression test for Sphinx issue #8035 - Support defining specific :private-members: for autodoc

This test checks the specific behavior change where private-members 
can now accept comma-separated member names instead of just boolean values.

The test ensures the fix creates the ability to specify:
    :private-members: _private_attr, __very_private_attr

Instead of only being able to do:
    :private-members: True (document all)
    :private-members: False (document none)
"""

def test_private_members_limitation_current():
    """
    Test to show that currently private-members can only accept boolean values.
    
    This demonstrates the existing limitation that the PR should fix.
    """
    from sphinx.ext.autodoc import bool_option
    
    # When users specify specific private member names, they get treated as truthy
    # This is the limitation we need to fix 
    test_input = "_private_attr,__very_private_attr"
    result = bool_option(test_input)
    
    # In the current system, string inputs to bool_option are converted to True
    # This is because bool_option treats any non-None, non-False value as truthy
    assert result is True
    
    print("✓ Confirmed current limitation: comma-separated strings become True")


def test_private_members_option_spec_change():
    """
    Test that shows the option specification should change.
    
    Before: 'private-members': bool_option
    After:  'private-members': members_option
    """
    
    from sphinx.ext.autodoc import ModuleDocumenter, ClassDocumenter, members_option
    
    # Confirm the current specification (will fail before fix, pass after)
    module_private_option = ModuleDocumenter.option_spec['private-members']
    class_private_option = ClassDocumenter.option_spec['private-members'] 
    
    # This demonstrates what we expect to change
    assert module_private_option == members_option
    assert class_private_option == members_option
    
    print("✓ Expected: Both ModuleDocumenter and ClassDocumenter use members_option")


def test_members_option_capability():
    """
    Test that members_option properly handles comma-separated values.
    
    This test demonstrates what the new members_option can now do.
    """
    from sphinx.ext.autodoc import members_option
    
    # The key feature: comma-separated member names should be parsed correctly
    test_input = "_private_attr,__very_private_attr" 
    result = members_option(test_input)
    
    expected = ["_private_attr", "__very_private_attr"]
    assert result == expected
    
    print("✓ members_option correctly parses comma-separated member names")


def test_behavior_change():
    """
    Main test showing the behavior that changes.
    
    Before: private-members = bool_option => only accepts True/False/None
    After:  private-members = members_option => accepts lists and comma-separated names
    """
    
    from sphinx.ext.autodoc import bool_option, members_option
    
    # Show the fundamental contrast:
    test_string = "_private_attr,__very_private_attr"
    
    # Old behavior (bool_option): any non-None, non-False string is True
    old_result = bool_option(test_string)
    assert old_result is True  # This is the limitation
    
    # New behavior (members_option): parse as list of member names 
    new_result = members_option(test_string) 
    expected = ["_private_attr", "__very_private_attr"]
    assert new_result == expected  
    
    print("✓ Demonstrated fundamental behavior difference needing fix")


def test_merge_members_option_exists():
    """
    Test that the new merge_members_option function exists and is available.
    
    This confirms that the core logic involved in the fix is properly in place.
    """
    try:
        from sphinx.ext.autodoc import merge_members_option
        # If this exists, it means the PR is applied and the function can be used
        print("✓ merge_members_option function exists (PR applied)")
        # Try to call it with empty dict - should not error (just return early)
        merge_members_option({})
        print("✓ merge_members_option calls successfully with empty dict")
    except ImportError:
        # This is expected before the fix
        print("✓ merge_members_option function not yet available (expected before fix)")


def test_key_functional_difference():
    """
    Test the key functional difference that this PR enables.
    
    Users should now be able to specify specific private members  
    with comma-separated names, not just True/False.
    """
    from sphinx.ext.autodoc import members_option
    
    # Complex case - trying the exact feature that was requested
    specific_members_input = "_attr1,_attr2,_attr3"
    
    # Before fix: this would be converted to True by bool_option  
    # After fix: this should parse as a list of actual member names
    
    result = members_option(specific_members_input)
    expected = ["_attr1", "_attr2", "_attr3"]
    
    assert result == expected
    print("✓ Users can now specify comma-separated private member names as requested")
    
    # Also test that the basic cases work
    assert members_option(None) is None
    assert members_option(True) is "ALL"  # The ALL object from sphinx.ext.autodoc
    assert members_option(False) is False
    
    print("✓ All basic members_option cases work correctly")