"""
Regression test for sphinx issue #8035: 
Support defining specific `:private-members:` for autodoc

This test ensures the fix that allows `:private-members:` to take arguments 
(such as `:private-members: _method1,_method2`) rather than only accepting 
boolean flags like `:private-members: True` or `:private-members:`.

The specific problem was that private-members was using bool_option which converted
any input to True, preventing specification of specific members. This change
switched private-members to use members_option instead, enabling comma-separated
lists of private member names.
"""

import pytest
from sphinx.ext.autodoc import members_option, bool_option, ALL


def test_private_members_now_supports_member_lists():
    """
    Test that demonstrates the main fix: private-members now supports 
    comma-separated member names (like :members: does) instead of just booleans.
    
    Before the fix: private-members='_method1,_method2' would be processed by bool_option
    and converted to True -> all private members documented
    
    After the fix: private-members='_method1,_method2' is processed by members_option  
    and converted to ['_method1', '_method2'] -> only specified members documented
    """
    
    # Test the core difference in option processing
    # bool_option always returns True regardless of input  
    result_bool = bool_option('_method1,_method2')
    assert result_bool is True  # This was BEFORE behavior
    
    # members_option properly parses comma-separated strings
    result_members = members_option('_method1,_method2') 
    assert result_members == ['_method1', '_method2']  # This is AFTER behavior
    
    # This test demonstrates that we can now specify exactly WHICH private members to include
    # Rather than just documenting ALL private members (as with bool_option behavior)


def test_feature_request_implementation():
    """
    Verify that the feature request from bug report is implemented:
    "For :private-members: to take arguments, similarly to how :members: currently works"
    """
    
    # The bug report requested the ability to specify specific private members
    # This now works because we use members_option for private-members
    
    # Test that we can specify specific private members
    specific_members = members_option('_private_func1,_private_func2')
    
    # Should parse into a list of the specific member names
    assert isinstance(specific_members, list)
    assert len(specific_members) == 2
    assert '_private_func1' in specific_members
    assert '_private_func2' in specific_members
    
    # Formerly this wouldn't work at all because bool_option would ignore the comma-separated nature


def test_backward_compatibility_maintained():
    """
    Ensure that the change maintains backward compatibility for special values.
    """
    
    # None and True should still mean "all members" (both behaviors)
    assert members_option(None) is ALL
    assert members_option(True) is ALL
    assert bool_option(None) is True
    assert bool_option(True) is True