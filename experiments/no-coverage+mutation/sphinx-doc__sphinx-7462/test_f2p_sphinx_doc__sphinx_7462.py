"""
Regression test for sphinx-doc/sphinx#7462: IndexError with empty tuple type annotation
"""
import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_indexerror():
    """Test that empty tuple annotation doesn't cause IndexError.
    
    This reproduces the bug reported in sphinx-doc/sphinx#7462 where
    parsing "Tuple[()]" would raise IndexError: pop from empty list.
    """
    # This test is designed to fail on the buggy code and pass on fixed code
    try:
        result = _parse_annotation("Tuple[()]")
        # If we get here without IndexError, test passes
        assert result is not None
        assert isinstance(result, list)
    except IndexError as e:
        if "pop from empty list" in str(e):
            # This is the exact bug we're testing for
            pytest.fail("IndexError: pop from empty list - bug not fixed")
        else:
            raise  # Re-raise if it's a different IndexError


def test_normal_tuple_annotations_still_work():
    """Ensure normal tuple annotations continue working after fix."""
    # Test that we didn't break existing functionality
    result = _parse_annotation("Tuple[int, str]") 
    assert result is not None
    assert isinstance(result, list)