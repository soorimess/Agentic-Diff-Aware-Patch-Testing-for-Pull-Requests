"""
Regression test for IndexError with empty tuple type annotation.

This test ensures that empty tuple type annotations like Tuple[()] don't
cause an IndexError in the Python domain's _parse_annotation function.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple annotation doesn't raise IndexError."""
    # This should not raise an IndexError - the bug was that it would
    # The specific case from the bug report: Tuple[()]
    try:
        result = _parse_annotation("Tuple[()]")
        # If we get here without exception, the test passes
        assert isinstance(result, list)
        # Should have at least a couple of elements for the parentheses
        assert len(result) >= 2
    except IndexError:
        pytest.fail("IndexError was raised when parsing empty tuple annotation")


def test_empty_tuple_annotation_various_forms():
    """Test various empty tuple annotation forms don't raise IndexError."""
    # Test different empty tuple forms that should not cause IndexError
    test_cases = [
        "Tuple[()]",
        "tuple[()]",
        "typing.Tuple[()]",
    ]
    
    for annotation in test_cases:
        # These should all work without raising IndexError
        try:
            result = _parse_annotation(annotation)
            assert isinstance(result, list)
            assert len(result) >= 2
        except IndexError:
            pytest.fail(f"IndexError was raised when parsing {annotation}")


def test_non_empty_tuple_annotation_still_works():
    """Ensure that non-empty tuple annotations still work correctly."""
    # Test that normal tuple annotations still work
    result = _parse_annotation("Tuple[int, str]")
    assert isinstance(result, list)
    assert len(result) > 0
    
    result = _parse_annotation("tuple[int, str]")
    assert isinstance(result, list)
    assert len(result) > 0