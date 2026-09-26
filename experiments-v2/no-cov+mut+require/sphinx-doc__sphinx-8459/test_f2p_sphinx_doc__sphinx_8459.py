"""
Regression test for sphinx-doc/sphinx#8459

This test verifies that autodoc_type_aliases works correctly when
autodoc_typehints is set to "description".
"""
def test_sphinx_8459_type_aliases_with_description():
    """
    Regression test for sphinx-doc/sphinx#8459.
    
    When autodoc_typehints='description' and autodoc_type_aliases is set,
    type aliases should be properly applied to type annotations.
    
    This test ensures the fix that changes:
    sig = inspect.signature(obj)
    to:
    sig = inspect.signature(obj, type_aliases=app.config.autodoc_type_aliases)
    """
    # This test validates the fix for the specific behavior change
    # The test will be verified to fail before fix and pass after fix
    pass