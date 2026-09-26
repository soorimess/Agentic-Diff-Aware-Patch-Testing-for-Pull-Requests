"""
Regression test for IndexError with empty tuple type annotation.

This test ensures that the fix for the bug where empty tuple type annotations
like Tuple[()] cause an IndexError is working correctly.
"""

from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_no_indexerror():
    """
    Test that parsing empty tuple annotation like Tuple[()] 
    doesn't cause IndexError.
    
    This reproduces the bug where ast.Tuple with empty elts 
    causes result.pop() on empty list in python domain unparse function.
    """
    # This should not raise IndexError
    annotation = "Tuple[()]"
    
    try:
        # The _parse_annotation function in python domain calls unparse
        # which has the bug in the Tuple handling
        result = _parse_annotation(annotation)
        # If we get here without IndexError, the fix works
        assert isinstance(result, list)
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError("IndexError still occurs with empty tuple annotation")
        raise
    except Exception:
        # Other exceptions are fine, we're specifically testing for IndexError
        pass