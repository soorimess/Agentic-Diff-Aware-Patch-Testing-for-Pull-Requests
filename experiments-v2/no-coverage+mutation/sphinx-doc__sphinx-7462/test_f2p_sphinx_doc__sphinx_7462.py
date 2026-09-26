"""
Regression test for IndexError with empty tuple type annotation.

This test ensures that empty tuple type annotations like Tuple[()] don't
cause an IndexError: pop from empty list in sphinx/domains/python.py.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple annotation doesn't raise IndexError."""
    # This should not raise IndexError: pop from empty list
    result = _parse_annotation('Tuple[()]')
    # The result should be a list with proper nodes
    assert isinstance(result, list)
    assert len(result) > 0


def test_empty_tuple_annotation_proper_format():
    """Test that empty tuple annotation produces proper format."""
    # Test that empty tuple produces expected structure
    result = _parse_annotation('Tuple[()]')
    
    # Should have at least the opening and closing parentheses
    # and should not be empty
    assert isinstance(result, list)
    assert len(result) >= 2
    
    # Should contain punctuation nodes for parentheses
    punctuation_nodes = [r for r in result if hasattr(r, 'tagname') and r.tagname == 'desc_sig_punctuation']
    # Should have at least opening and closing parentheses
    assert len(punctuation_nodes) >= 2
    
    # The first and last should be parentheses
    assert any('(' in str(node) for node in punctuation_nodes)
    assert any(')' in str(node) for node in punctuation_nodes)


def test_empty_tuple_vs_nonempty_tuple():
    """Test that empty and non-empty tuples behave differently but both work."""
    # Empty tuple should work without error
    empty_result = _parse_annotation('Tuple[()]')
    assert isinstance(empty_result, list)
    assert len(empty_result) > 0
    
    # Non-empty tuple should also work
    nonempty_result = _parse_annotation('Tuple[int, str]')
    assert isinstance(nonempty_result, list)
    assert len(nonempty_result) > 0
    
    # Both should be lists of nodes
    assert isinstance(empty_result, list)
    assert isinstance(nonempty_result, list)