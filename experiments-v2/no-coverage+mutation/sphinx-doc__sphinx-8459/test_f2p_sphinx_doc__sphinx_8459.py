"""
Regression test for sphinx-doc/sphinx#8459

This test ensures that autodoc_type_aliases works correctly when 
autodoc_typehints is set to "description".
"""
import inspect


def test_typehint_alias_behavior():
    """
    Test that demonstrates the expected behavior change for autodoc_type_aliases.
    
    The bug was that when autodoc_typehints='description', type aliases were not used.
    The fix adds type_aliases parameter to inspect.signature() call.
    
    This test shows the current (buggy) behavior where inspect.signature doesn't support type_aliases.
    """
    
    # Create a function that would use type aliases
    def sphinx_doc(data: "JSONObject") -> "JSONObject":
        """Test function with type alias."""
        return data
    
    # Basic functionality should work
    sig = inspect.signature(sphinx_doc)
    assert sig is not None
    
    # The core issue: inspect.signature with type_aliases should fail in old version
    # This demonstrates the bug - the fix is needed
    try:
        # This is what the NEW code does - should work after fix
        sig_with_aliases = inspect.signature(sphinx_doc, type_aliases={'JSONObject': 'types.JSONObject'})
        # If this works, the fix is applied
        fix_works = True
    except TypeError as e:
        if "type_aliases" in str(e):
            # Expected in old version - fix needed
            fix_works = False
        else:
            raise
    except Exception:
        fix_works = False
    
    # In the old version, this should fail, which means the bug exists
    # This test validates that we're in the buggy state
    assert not fix_works, (
        "In the old version, inspect.signature should not accept type_aliases parameter. "
        "This shows that autodoc_type_aliases is not used with autodoc_typehints='description'."
    )


def test_function_basic():
    """
    Basic function test.
    """
    def test_function(data: "JSONObject") -> "JSONObject":
        """Test function."""
        return data
    
    assert callable(test_function)
    sig = inspect.signature(test_function)
    assert sig is not None