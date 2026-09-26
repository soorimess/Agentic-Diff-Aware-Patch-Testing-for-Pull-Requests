"""
Test for empty tuple type annotation bug
This test reproduces the IndexError: pop from empty list bug
when parsing empty tuple type annotations like Tuple[()]
"""
import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple annotation doesn't cause IndexError."""
    # This should not raise IndexError: pop from empty list
    annotation = "Tuple[()]"
    
    # The main test: this should not raise IndexError
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, the test passes
        assert result is not None
    except IndexError as e:
        if "pop from empty list" in str(e):
            pytest.fail(f"IndexError occurred: {e}")
        else:
            raise  # Re-raise if it's a different IndexError