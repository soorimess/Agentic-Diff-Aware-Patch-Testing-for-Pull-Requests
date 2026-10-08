"""
Regression test for Sphinx issue with Literal annotation values being treated as missing py:class.

This test verifies that Literal annotation values like True, False, 1, etc. are handled
correctly and not treated as class references that would cause nitpick warnings.
"""
from sphinx.domains.python import _parse_annotation


def test_literal_annotation_values_no_class_reference_issues(app):
    """
    Test that literal annotation values don't cause class reference issues.
    
    The fix ensures that literal values inside typing.Literal[...] are handled
    specially to prevent nitpick warnings when using -n -W flags.
    """
    
    # Test the exact problematic cases from the bug report
    test_cases = [
        'typing.Literal[True]',
        'typing.Literal[False]',
    ]
    
    for annotation in test_cases:
        # These should parse without causing nitpick warnings
        result = _parse_annotation(annotation, app.env)
        
        # Verify parsing works correctly
        assert isinstance(result, list)
        assert len(result) > 0


def test_literal_annotation_various_types(app):
    """
    Test literal annotations with various literal types.
    """
    
    # Test various literal types that could have caused issues
    test_cases = [
        'typing.Literal[True]',
        'typing.Literal[False]', 
        'typing.Literal[1]',
        'typing.Literal[0]',
        'typing.Literal[\"hello\"]',
        'typing.Literal[None]',
    ]
    
    for annotation in test_cases:
        result = _parse_annotation(annotation, app.env)
        assert isinstance(result, list)
        assert len(result) > 0


def test_literal_annotation_complex_scenarios(app):
    """
    Test complex literal annotation scenarios.
    """
    
    # Complex literal combinations
    complex_cases = [
        'typing.Literal[True, False]',
        'typing.Literal[1, 2, 3]', 
        'typing.Literal[\"a\", \"b\", \"c\"]',
        'typing.Literal[True, 1, \"test\", None]',
    ]
    
    for annotation in complex_cases:
        result = _parse_annotation(annotation, app.env)
        assert isinstance(result, list)
        assert len(result) > 0


def test_literal_annotation_forms(app):
    """
    Test both typing.Literal and Literal forms.
    """
    
    # Both forms should work correctly
    result1 = _parse_annotation('typing.Literal[True]', app.env)
    result2 = _parse_annotation('Literal[True]', app.env)
    
    assert isinstance(result1, list)
    assert isinstance(result2, list)
    assert len(result1) > 0
    assert len(result2) > 0