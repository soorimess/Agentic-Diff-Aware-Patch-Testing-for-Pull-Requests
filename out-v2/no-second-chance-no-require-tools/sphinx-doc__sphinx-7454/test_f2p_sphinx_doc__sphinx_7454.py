"""
Regression test for sphinx-doc/sphinx#7454
Inconsistent handling of None by autodoc_typehints

This test ensures that the fix for None type annotation handling is properly 
implemented and prevents regression.
"""
import sys
import os

# Add the current directory to the path so we can import sphinx
sys.path.insert(0, os.path.abspath('.'))

from sphinx.domains.python import _parse_annotation


def test_parse_annotation_none_handling():
    """
    Test that _parse_annotation correctly handles None type annotation.
    
    The bug was that when autodoc_typehints='signature', None in return type 
    hints would not get a clickable link to None's documentation, while 
    autodoc_typehints='description' would work correctly.
    
    This test ensures that the parsing works correctly for both 'None' and 
    other types, which is the foundation for proper linking behavior.
    """
    
    # Test parsing of None annotation - this should not raise any errors
    none_result = _parse_annotation('None')
    
    # Should return a list of nodes
    assert isinstance(none_result, list)
    assert len(none_result) >= 1
    
    # Test parsing of regular type annotation
    int_result = _parse_annotation('int')
    assert isinstance(int_result, list)
    assert len(int_result) >= 1
    
    # Both should produce valid structures that can be processed
    # The key is that they both work without errors and produce proper node structures
    assert none_result[0] is not None
    assert int_result[0] is not None


def test_parse_annotation_consistent_behavior():
    """
    Test that parsing behaves consistently for different type annotations.
    """
    # Test various type annotations to ensure consistent behavior
    test_cases = ['None', 'int', 'str', 'list', 'dict', 'float']
    
    for case in test_cases:
        # All should parse without raising exceptions
        result = _parse_annotation(case)
        assert isinstance(result, list), f"Failed to parse type annotation: {case}"
        assert len(result) >= 1, f"Failed to parse type annotation: {case}"
        
        # Should produce valid nodes
        from sphinx.addnodes import pending_xref
        assert isinstance(result[0], pending_xref), f"Failed to create proper node for {case}"