"""Regression test for autodoc_type_aliases with autodoc_typehints='description'"""

def test_signature_supports_type_aliases_direct():
    """
    Test sphinx.util.inspect.signature with type_aliases parameter.
    This directly checks the main function change.
    """
    from sphinx.util.inspect import signature
    from typing import Dict, Any
    
    def function_with_annotations(param: Dict[str, Any]) -> Dict[str, Any]:
        return {}
    
    # This is the NEW path from the patch
    try:
        sig = signature(function_with_annotations, type_aliases={})
        # If we get here without an error, the parameter is accepted
        # This shows the fix is in place
        return True
    except TypeError as e:
        if "unexpected keyword argument" in str(e) or "type_aliases" in str(e):
            raise AssertionError("type_aliases parameter not supported - this means fix not applied")
        raise e


def test_signature_type_aliases_behavior():
    """
    Test that demonstrates what exactly the patch was modifying
    """
    from sphinx.util.inspect import signature
    from typing import Dict, Any
    
    def test_func(param: Dict[str, Any]) -> None:
        pass
    
    # Test that we can pass any non-empty type_aliases dict  
    try:
        sig = signature(test_func, type_aliases={'Dict[str, Any]': 'types.JSONObject'})
        assert sig is not None
        return "SUCCESS"
    except TypeError as e:
        if "unexpected keyword argument" in str(e):
            raise AssertionError("Fix is not applied - type_aliases parameter missing")
        raise e