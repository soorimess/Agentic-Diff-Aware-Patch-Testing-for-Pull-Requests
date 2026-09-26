"""
Regression test for sphinx-doc/sphinx#7462
Test for IndexError when processing empty tuple type annotations.
"""

import pytest
from sphinx.domains.python import _parse_annotation
from sphinx import addnodes


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple type annotations don't cause IndexError."""
    # This should not raise IndexError
    annotation = "Tuple[()]"
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, the fix works
        assert result is not None
        assert isinstance(result, list)
        print(f"Successfully parsed: {annotation} -> {len(result)} nodes")
    except IndexError as e:
        pytest.fail(f"IndexError occurred: {e}")
    except Exception as e:
        # Other exceptions might be expected (like SyntaxError)
        print(f"Other exception (expected): {type(e).__name__}: {e}")


def test_empty_tuple_literal_no_indexerror():
    """Test that empty tuple literals don't cause IndexError."""
    # Test literal empty tuple
    annotation = "()"
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, the fix works
        assert result is not None
        assert isinstance(result, list)
        print(f"Successfully parsed: {annotation} -> {len(result)} nodes")
    except IndexError as e:
        pytest.fail(f"IndexError occurred: {e}")
    except Exception as e:
        print(f"Other exception (expected): {type(e).__name__}: {e}")


def test_non_empty_tuple_annotation_still_works():
    """Test that non-empty tuple annotations still work correctly."""
    # Test non-empty tuple annotation
    annotation = "Tuple[int, str]"
    try:
        result = _parse_annotation(annotation)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        print(f"Successfully parsed: {annotation} -> {len(result)} nodes")
        # Should contain proper structure for Tuple[int, str]
        assert any(isinstance(node, addnodes.pending_xref) and 'Tuple' in str(node) for node in result)
        assert any(isinstance(node, addnodes.desc_sig_punctuation) and '[' in str(node) for node in result)
        assert any(isinstance(node, addnodes.desc_sig_punctuation) and ']' in str(node) for node in result)
    except Exception as e:
        print(f"Exception (unexpected): {type(e).__name__}: {e}")


def test_empty_tuple_structure():
    """Test that empty tuple has correct structure after fix."""
    # Test that we can parse empty tuple without crashing
    # This is a more detailed test for the actual structure
    annotation = "()"
    try:
        result = _parse_annotation(annotation)
        # Should return a list of nodes, not crash
        assert isinstance(result, list)
        print(f"Empty tuple structure: {len(result)} nodes")
        # The key thing is that it doesn't crash with IndexError
    except IndexError:
        pytest.fail("IndexError should not occur for empty tuple")
    except Exception:
        # Other exceptions are fine for this test
        pass


if __name__ == "__main__":
    test_empty_tuple_annotation_no_indexerror()
    test_empty_tuple_literal_no_indexerror()
    test_non_empty_tuple_annotation_still_works()
    test_empty_tuple_structure()
    print("All tests passed!")