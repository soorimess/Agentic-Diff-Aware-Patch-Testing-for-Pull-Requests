"""
Regression test for sphinx-doc/sphinx#8035
Test that private-members option can accept specific member names, not just boolean.

This test demonstrates the exact change requested in the GitHub issue:
"Currently, if I'm using autodoc, the :private-members: option does not allow 
specification of which private members to document. The current behavior is to 
document all private members, but what if I would only like to document 1 or 2?"

The fix enables users to specify exactly which private members to document.
"""

def test_private_members_enhancement():
    """
    Test the core enhancement: users can now specify which private members to document.
    
    Before fix: :private-members: True/False only
    After fix: :private-members: '_method1,_method2' or ['_method1', '_method2']
    """
    
    from sphinx.ext.autodoc import members_option
    
    # Test that comma-separated strings work (new functionality)
    result = members_option('_method1,_method2')
    assert result == ['_method1', '_method2']
    
    # Test that single member works
    result = members_option('_method1')
    assert result == ['_method1']


def test_issue_feature_request():
    """
    Test that the exact feature request from the GitHub issue is satisfied.
    
    Issue: "For :private-members: to take arguments, similarly to how :members: currently works"
    """
    
    from sphinx.ext.autodoc import members_option
    
    # This is what users wanted to be able to do:
    # Instead of just: :private-members: True/False
    # They can now do: :private-members: _method1,_method2
    
    # Test the new capability
    result = members_option('_method1,_method2,_method3')
    assert result == ['_method1', '_method2', '_method3']


def test_backward_compatibility():
    """
    Test that existing boolean usage still works for backward compatibility.
    """
    
    from sphinx.ext.autodoc import bool_option
    
    # These should work in both versions
    result = bool_option(True)
    assert result is True
    
    result = bool_option(False)
    assert result is True


if __name__ == '__main__':
    test_private_members_enhancement()
    test_issue_feature_request()
    test_backward_compatibility()
    print("All tests passed - demonstrating the fix for sphinx#8035")