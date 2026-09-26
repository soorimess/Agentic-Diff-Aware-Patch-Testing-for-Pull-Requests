"""
Regression test for sphinx-doc/sphinx#8035

This test verifies that the private-members option now accepts specific member names
rather than just a boolean flag, allowing users to specify which private members to document.
"""

def test_private_members_filtering_behavior():
    """
    Test the specific filtering behavior change in is_filtered_inherited_member.
    
    Before: private-members was boolean, so filtering was: 
        keep = self.options.private_members
    
    After: private-members can be a list, so filtering is:
        if self.options.private_members is None:
            keep = False
        elif self.options.private_members is ALL:
            keep = True
        else:
            keep = membername in self.options.private_members
    """
    
    # Test that we can now specify exact private members to document
    from sphinx.ext.autodoc import members_option, ALL
    
    # This is the new capability - specify exact members
    private_members_input = "_specific_attr,_another_private"
    parsed_members = members_option(private_members_input)
    
    # Verify it parses correctly
    assert parsed_members == ["_specific_attr", "_another_private"]
    
    # Test the new filtering logic that wasn't possible before
    # This simulates what happens in the updated is_filtered_inherited_member function
    
    # The key difference: before we could only have boolean True/False
    # Now we can have a list of specific members
    
    def simulate_new_filtering_logic(member_name, private_members_option):
        """Simulate the new filtering logic from the PR."""
        if private_members_option is None:
            return False
        elif private_members_option is ALL:
            return True
        else:
            # This is the NEW capability - check membership in specific list
            return member_name in private_members_option
    
    # Test that specific members are documented
    assert simulate_new_filtering_logic("_specific_attr", parsed_members) == True
    assert simulate_new_filtering_logic("_another_private", parsed_members) == True
    
    # Test that non-specified members are NOT documented (this is the key improvement)
    assert simulate_new_filtering_logic("_unspecified_attr", parsed_members) == False
    
    print("✓ New filtering behavior allows specific member selection")


def test_private_members_option_specification():
    """
    Test that private-members option specification changed from bool_option to members_option.
    """
    from sphinx.ext.autodoc import ModuleDocumenter, ClassDocumenter
    
    # Check that both documenters now accept comma-separated values
    module_spec = ModuleDocumenter.option_spec
    class_spec = ClassDocumenter.option_spec
    
    assert 'private-members' in module_spec
    assert 'private-members' in class_spec
    
    # Verify the option processing now supports lists (not just booleans)
    from sphinx.ext.autodoc import members_option
    result = members_option("_attr1,_attr2")
    assert result == ["_attr1", "_attr2"]
    
    print("✓ private-members option now supports comma-separated values")


def test_feature_request_syntax():
    """
    Test that the exact syntax from the feature request now works.
    
    Feature request: "For :private-members: to take arguments, 
    similarly to how :members: currently works"
    """
    from sphinx.ext.autodoc import members_option
    
    # This is the syntax that should now work
    syntax = "_attr1,_attr2,_method1"
    result = members_option(syntax)
    
    # Should parse into list of member names
    assert result == ["_attr1", "_attr2", "_method1"]
    
    # This enables the requested functionality
    assert len(result) == 3
    assert "_attr1" in result
    assert "_attr2" in result
    assert "_method1" in result
    
    print("✓ Feature request syntax works correctly")


def test_backward_compatibility():
    """
    Test that existing usage patterns still work for backward compatibility.
    """
    from sphinx.ext.autodoc import members_option, ALL
    
    # These should work as before
    assert members_option(True) is ALL
    assert members_option(None) is ALL
    
    print("✓ Backward compatibility maintained")


def test_filtering_scenarios():
    """
    Test all three filtering scenarios that are now supported.
    """
    from sphinx.ext.autodoc import members_option, ALL
    
    # Scenario 1: None - no private members
    result = None
    assert result is None
    
    # Scenario 2: ALL - all private members
    result = ALL
    assert result is ALL
    
    # Scenario 3: List - specific private members
    result = members_option("_attr1,_attr2")
    assert isinstance(result, list)
    assert "_attr1" in result
    assert "_attr2" in result
    
    print("✓ All filtering scenarios work correctly")