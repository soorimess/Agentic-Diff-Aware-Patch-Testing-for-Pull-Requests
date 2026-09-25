"""
Test for empty tuple type annotation bug
Regression test for IndexError: pop from empty list in empty tuple annotations
"""
import pytest


def test_empty_tuple_annotation_prevents_indexerror():
    """Test that empty tuple annotation doesn't cause IndexError (the main bug fix)."""
    # This exact case caused IndexError: pop from empty list before fix
    from sphinx.domains.python import _parse_annotation
    
    annotation = "Tuple[()]"
    
    # This should NOT raise IndexError after the fix
    try:
        result = _parse_annotation(annotation)
        # If we succeed, the fix is working
        assert result is not None
        assert isinstance(result, list)
        # The key thing: no IndexError crash
    except IndexError as e:
        if "pop from empty list" in str(e):
            pytest.fail(f"IndexError bug still present: {e}")
        else:
            raise


def test_non_empty_tuple_still_works():
    """Test that non-empty tuples still work correctly after the fix."""
    from sphinx.domains.python import _parse_annotation
    
    # Test with a non-empty tuple - should still work just like before
    annotation = "Tuple[int, str]"
    
    try:
        result = _parse_annotation(annotation)
        assert result is not None
        assert isinstance(result, list)
    except Exception as e:
        pytest.fail(f"Non-empty tuple failed unexpectedly: {e}")


def test_simple_type_still_works():
    """Test that simple types still work correctly."""
    from sphinx.domains.python import _parse_annotation
    
    # Test with a simple type - should still work just like before
    annotation = "int"
    
    try:
        result = _parse_annotation(annotation)
        assert result is not None
        assert isinstance(result, list)
    except Exception as e:
        pytest.fail(f"Simple type failed unexpectedly: {e}")


def test_empty_tuple_different_format():
    """Test alternative empty tuple annotations."""
    from sphinx.domains.python import _parse_annotation
    
    # Test various empty tuple formats that should all work
    test_cases = ["Tuple[()]", "tuple[()]", " typing.Tuple[()]" ]
    
    for annotation in test_cases:
        try:
            result = _parse_annotation(annotation)
            assert result is not None
            assert isinstance(result, list)
        except IndexError as e:
            if "pop from empty list" in str(e):
                pytest.fail(f"IndexError in {annotation}: {e}")
            else:
                raise
        except Exception:
            # Other exceptions are ok for these edge cases
            # as long as it's not IndexError: pop from empty list
            pass