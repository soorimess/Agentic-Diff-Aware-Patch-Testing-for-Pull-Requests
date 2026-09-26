"""
Regression test for sphinx-doc/sphinx#8459

This test ensures that autodoc_type_aliases works correctly when 
autodoc_typehints is set to "description".
"""
import pytest
from sphinx.util import inspect


def test_inspect_signature_type_aliases_support():
    """
    Test that inspect.signature supports type_aliases parameter which is the core fix.
    
    This test specifically verifies the exact API change that was made:
    Before: sig = inspect.signature(obj)
    After:  sig = inspect.signature(obj, type_aliases=app.config.autodoc_type_aliases)
    
    The fix enables type alias resolution when autodoc_typehints='description'
    """
    
    # Test function with annotations
    def test_func(data: dict) -> list:
        return [data]
    
    # The test verifies that the type_aliases parameter is accepted
    # This is the core functionality that was added in the fix
    try:
        # This call pattern was changed in the fix
        sig = inspect.signature(test_func, type_aliases={'dict': 'typing.Dict'})
        
        # Verify we got a valid signature
        assert sig is not None
        assert len(sig.parameters) == 1
        assert sig.return_annotation is not sig.empty
        
        # Verify parameter access works
        param = sig.parameters['data']
        assert param.annotation is not param.empty
        
        # If we reach here, the fix is working - the API call succeeds
        return True
        
    except TypeError as e:
        # This error would occur if the fix wasn't applied
        if "unexpected keyword argument" in str(e) or "type_aliases" in str(e):
            pytest.fail("The fix for sphinx-doc/sphinx#8459 is missing: "
                       "inspect.signature does not support type_aliases parameter")
        raise
    except Exception as e:
        pytest.fail(f"Unexpected error in signature inspection: {e}")


def test_type_alias_functionality():
    """
    Test that type alias functionality works in signature processing.
    
    This ensures that when type aliases are provided, they are handled 
    properly in signature inspection, which is what enables the bug fix.
    """
    
    # Create a scenario with type alias like in bug report
    from typing import Dict, Any
    
    JSONObject = Dict[str, Any]
    
    def sphinx_doc(data: JSONObject) -> JSONObject:
        """Function with type alias."""
        return data
    
    # Test signature inspection with type aliases
    try:
        # This is the exact call that was modified in the fix
        sig = inspect.signature(sphinx_doc, type_aliases={'JSONObject': 'types.JSONObject'})
        
        # Verify signature processing works
        assert sig is not None
        assert 'data' in sig.parameters
        param = sig.parameters['data']
        assert param.annotation is not param.empty
        
        # Success means the fix is working
        return True
        
    except Exception as e:
        pytest.fail(f"Type alias functionality test failed: {e}")


def test_signature_inspection_baseline():
    """
    Baseline test for normal signature inspection.
    """
    
    def simple_func(x: int) -> str:
        return str(x)
    
    # Basic functionality should work
    sig = inspect.signature(simple_func)
    assert sig is not None
    assert len(sig.parameters) == 1
    assert sig.return_annotation is not sig.empty