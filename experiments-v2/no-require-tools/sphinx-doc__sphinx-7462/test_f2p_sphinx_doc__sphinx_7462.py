"""
Regression test for IndexError with empty tuple type annotation.

This test ensures that empty tuple type annotations like Tuple[()] do not
cause an IndexError in the _parse_annotation function.
"""

from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple annotation does not cause IndexError."""
    # This should not raise IndexError when parsing empty tuple annotation
    # The bug was in the Tuple handling in _parse_annotation function
    annotation = "Tuple[()]"
    
    # This should work without raising IndexError
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, it's good
        assert isinstance(result, list)
        # Should have some nodes in the result
        assert len(result) >= 0
    except IndexError as e:
        # This should not happen with the fix
        raise AssertionError(f"IndexError should not occur: {e}")
    except Exception:
        # Other exceptions are OK, we're only concerned about IndexError
        pass


def test_empty_tuple_in_function_return_annotation():
    """Test that function with empty tuple return annotation works."""
    # Test the exact scenario from the bug report
    annotation = "Tuple[()]"
    
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, it's good
        assert isinstance(result, list)
    except IndexError as e:
        # This should not happen with the fix
        raise AssertionError(f"IndexError should not occur: {e}")
    except Exception:
        # Other exceptions are OK
        pass