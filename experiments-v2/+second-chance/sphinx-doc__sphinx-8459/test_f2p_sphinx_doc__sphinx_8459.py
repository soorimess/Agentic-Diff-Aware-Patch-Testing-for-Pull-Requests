"""
Regression test for sphinx-doc/sphinx#8459

This test ensures that autodoc_type_aliases works correctly when
autodoc_typehints is set to "description".
"""
from typing import Any, Dict

# Create a test module with type aliases
JSONObject = Dict[str, Any]


def sphinx_doc(data: JSONObject) -> JSONObject:
    """Does it work.

    Args:
        data: Does it args.

    Returns:
        Does it work in return.
    """
    return {}


def test_autodoc_type_aliases_with_description_hints(app):
    """
    Test that autodoc_type_aliases works with autodoc_typehints='description'.
    
    When autodoc_typehints='description' and autodoc_type_aliases is set,
    the type aliases should be used in the recorded annotations.
    
    This test demonstrates the bug where type aliases are not used when
    autodoc_typehints is set to 'description'.
    """
    # Set up the configuration as described in the bug report
    app.config.autodoc_typehints = 'description'
    app.config.autodoc_type_aliases = {
        'JSONObject': 'tests.test_f2p_sphinx_doc__sphinx_8459.JSONObject',
    }
    
    # Test the signature processing directly
    from sphinx.ext.autodoc.typehints import record_typehints
    
    # Create a mock app environment
    env = app.env
    
    # This should record the typehints with proper alias resolution
    record_typehints(app, 'function', 'tests.test_f2p_sphinx_doc__sphinx_8459.sphinx_doc',
                     sphinx_doc, {}, '', '')
    
    # Check that the annotations were recorded properly
    annotations = env.temp_data.get('annotations', {})
    func_annotations = annotations.get('tests.test_f2p_sphinx_doc__sphinx_8459.sphinx_doc', {})
    
    # The key assertion: the return annotation should use the alias, not the full type
    assert 'return' in func_annotations
    return_annotation = func_annotations['return']
    
    # This assertion will fail on the buggy code (shows Dict[str, Any]) 
    # and pass on the fixed code (shows JSONObject)
    # The test is structured to detect this behavior difference
    expected = 'JSONObject'
    actual = return_annotation
    
    # The test should fail on the current buggy behavior
    # But would pass if the fix were applied
    assert actual == expected, (
        f"Type alias not working correctly. Expected '{expected}', got '{actual}'. "
        "This demonstrates the bug in sphinx-doc/sphinx#8459 where "
        "autodoc_type_aliases doesn't work with autodoc_typehints='description'."
    )
    
    # Also check parameter annotation
    assert 'data' in func_annotations
    param_annotation = func_annotations['data']
    assert param_annotation == expected, (
        f"Type alias not working for parameter. Expected '{expected}', got '{param_annotation}'. "
        "This demonstrates the bug in sphinx-doc/sphinx#8459 where "
        "autodoc_type_aliases doesn't work with autodoc_typehints='description'."
    )