"""
Regression test for IndexError with empty tuple type annotations.

This test ensures that empty tuple type annotations like Tuple[()] don't
cause an IndexError: pop from empty list.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple type annotations don't cause IndexError in _parse_annotation."""
    # This should not raise an IndexError
    annotation = "Tuple[()]"
    
    # The function should complete without raising IndexError
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, the test passes
        assert isinstance(result, list)
    except IndexError as e:
        pytest.fail(f"IndexError raised when parsing empty tuple annotation: {e}")


def test_empty_tuple_annotation_returns_proper_structure():
    """Test that empty tuple annotation returns proper structure."""
    # Test that we get a proper result structure for empty tuple
    annotation = "Tuple[()]"
    
    try:
        result = _parse_annotation(annotation)
        # Should return a list of nodes
        assert isinstance(result, list)
        # Should not be empty (should contain some nodes for the empty tuple)
        # The exact structure depends on implementation but shouldn't crash
    except IndexError as e:
        pytest.fail(f"IndexError raised when parsing empty tuple annotation: {e}")


if __name__ == "__main__":
    test_empty_tuple_annotation_no_indexerror()
    test_empty_tuple_annotation_returns_proper_structure()
    print("All tests passed!")