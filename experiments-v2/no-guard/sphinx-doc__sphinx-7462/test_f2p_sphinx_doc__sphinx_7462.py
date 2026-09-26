"""
Regression test for empty tuple type annotation bug.

This test ensures that empty tuple type annotations like Tuple[()] don't cause
IndexError: pop from empty list in sphinx/domains/python.py
"""

from sphinx.domains.python import _parse_annotation


def test_empty_tuple_type_annotation():
    """
    Test that empty tuple type annotations like Tuple[()] are handled correctly.
    
    This reproduces the bug reported where parsing Tuple[()] would cause:
    IndexError: pop from empty list in sphinx/domains/python.py line 112
    """
    # The bug occurs when Sphinx tries to parse empty tuple type annotations
    # This should not raise IndexError: pop from empty list
    try:
        result = _parse_annotation("Tuple[()]")
        # If we get here without exception, the bug is fixed
        assert result is not None
        # The result should be a list of nodes (not None)
        assert isinstance(result, list)
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError("IndexError: pop from empty list occurred - bug reproduced")
        else:
            raise  # Re-raise if it's a different IndexError


def test_empty_tuple_in_function_signature():
    """
    Test that empty tuple annotations in function signatures work properly.
    
    This tests the specific case mentioned in the bug report where a function
    has a return type annotation of Tuple[()]
    """
    try:
        # Test with a more complete function signature scenario
        result = _parse_annotation("Callable[[], Tuple[()]]")
        assert result is not None
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError("IndexError: pop from empty list occurred in function annotation - bug reproduced")
        else:
            raise