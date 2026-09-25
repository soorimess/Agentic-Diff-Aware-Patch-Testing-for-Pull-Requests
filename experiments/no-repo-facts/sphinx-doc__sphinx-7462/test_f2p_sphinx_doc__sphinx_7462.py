"""Test for bug with empty tuple type annotations in sphinx."""

from sphinx.domains.python import _parse_annotation


def test_empty_tuple_no_indexerror():
    """Test that parsing empty tuple annotation doesn't cause IndexError."""
    # Parse the exact case reported in the issue that caused the IndexError
    # This should not raise IndexError: pop from empty list
    try:
        result = _parse_annotation("Tuple[()]")
        assert isinstance(result, list)
        # If this doesn't raise, we won the race against the bug
        assert len(result) >= 0
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError(f"Bug still exists: {e}")
        else:
            raise  # Re-raise any other IndexError

def test_simple_empty_tuple_no_indexerror():
    """Test simple empty tuple doesn't cause IndexError"""
    try:
        result = _parse_annotation("()")
        assert isinstance(result, list)
        assert len(result) >= 0
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError(f"Bug still exists: {e}")
        else:
            raise