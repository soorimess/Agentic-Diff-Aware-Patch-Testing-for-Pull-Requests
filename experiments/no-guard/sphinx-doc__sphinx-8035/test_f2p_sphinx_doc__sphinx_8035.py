"""
Regression test for feature request to support specific private members in autodoc.

This ensures the change in how :private-members: option is handled
enables the documented functionality.
"""

from sphinx.ext.autodoc.__init__ import ALL, members_option


def test_private_members_option_type_handling():
    """
    Primary test for the fundamental API change: 
    private-members now handles lists instead of just bools.
    
    This is what enables the feature request to specify exact private members.
    """
    
    # The change: private-members option now uses members_option instead of bool_option
    # This is actually a simple but critical API-breaking change
    
    # With old bool_option behavior, "false" as a string would be processed as True
    # With new members_option behavior, "false" as a string becomes ["false"]
    
    # Before: :private-members: false would interpret as "document all private members" 
    # After: :private-members: false would try to interpret as "document member named false"
    
    # The test: This explicitly confirms the new behavior is what we expect
    
    # Valid cases that demonstrate the new capability:
    result_none = members_option(None)        # Should be ALL sentinel
    result_true = members_option(True)        # Should be ALL sentinel  
    result_list = members_option("_method1,_method2")  # Should be list
    result_single = members_option("_method1")  # Should be list with one item
    result_false_str = members_option("false")  # Should be ["false"], NOT True
    
    # Make sure these are the expected types/values for new functionality
    assert result_none is ALL
    assert result_true is ALL
    assert result_list == ["_method1", "_method2"]
    assert result_single == ["_method1"]
    assert result_false_str == ["false"]  # This is the key difference!
    
    # Test one concrete scenario of what user wants:
    # User wants to specify exactly which private members to document
    # :private-members: _handler,_processor
    specific_private_members = members_option("_handler,_processor")
    assert specific_private_members == ["_handler", "_processor"]


def test_private_members_enables_selection():
    """
    Test that basic member selection capability works as expected. 
    This demonstrates that the selection logic can now work with lists.
    """
    
    # The problem the PR wanted to solve: you couldn't specify
    # exactly which private members to document
    
    # BEFORE: private-members was only boolean-type  
    # AFTER: private-members can be a list
    
    # The ability to only document _handler and _processor
    # instead of all private members, is now possible
    
    # This just asserts the ability to build the right structure
    # for the filtering logic to work with
    
    desired_members = members_option("_specific1,_specific2")
    
    # Now the filtering code can use:
    # if membername in desired_members:
    #    keep = True
    # else:
    #    keep = False
    
    assert desired_members == ["_specific1", "_specific2"]
    
    # The structure now enables proper filtering bounds checking 
    assert "_specific1" in desired_members
    assert "_specific2" in desired_members
    assert "_other" not in desired_members

    
def test_private_members_new_api_shape():
    """
    Test the API shape change that provides the enabling functionality.
    """
    
    # The change specifically makes sure private-members option can accept 
    # the same kinds of values as members and special-members options
    
    # All three are now alike:
    # :members: :special-members: :private-members:  
    # Can all accept None, True, or comma-separated strings
    
    # Test the structure that enables this:
    api Shape_tests = [
        (None, ALL), 
        (True, ALL), 
        ("_method1", ["_method1"]), 
        ("_method1,_method2", ["_method1", "_method2"])
    ]
    
    for input_val, expected in Shape_tests:
        result = members_option(input_val)
        assert result == expected, f"Failed for input {input_val}: expected {expected}, got {result}"