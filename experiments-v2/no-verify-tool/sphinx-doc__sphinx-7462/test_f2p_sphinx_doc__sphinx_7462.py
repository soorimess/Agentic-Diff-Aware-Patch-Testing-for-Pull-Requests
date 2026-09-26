"""Regression test for empty tuple type annotation bug.

This test ensures that empty tuple type annotations like Tuple[()] don't cause
IndexError: pop from empty list.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_type_annotation_raises_no_indexerror():
    """Test that empty tuple type annotation doesn't raise IndexError."""
    # This is the exact case from the bug report that caused IndexError
    # The bug occurs when parsing Tuple[()] which creates an empty tuple AST node
    annotation = "Tuple[()]"
    
    # This should not raise IndexError: pop from empty list
    # Before the fix, this would fail with IndexError
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, the test passes
        assert isinstance(result, list)
    except IndexError as e:
        pytest.fail(f"IndexError raised when parsing empty tuple annotation: {e}")


def test_empty_tuple_type_annotation_with_list():
    """Test that empty list type annotation also works."""
    # Test similar case with List[()]
    annotation = "List[()]"
    
    try:
        result = _parse_annotation(annotation)
        assert isinstance(result, list)
    except IndexError as e:
        pytest.fail(f"IndexError raised when parsing empty list annotation: {e}")


def test_non_empty_tuple_still_works():
    """Test that non-empty tuple annotations still work correctly."""
    # This should continue to work as before
    annotation = "Tuple[int, str]"
    result = _parse_annotation(annotation)
    assert isinstance(result, list)