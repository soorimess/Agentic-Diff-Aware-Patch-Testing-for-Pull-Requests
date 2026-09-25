"""
Regression test for IndexError with empty tuple type annotations.

This test ensures that empty tuple type annotations like Tuple[()] 
don't cause an IndexError: pop from empty list.
"""

import ast
from sphinx.domains.python import _parse_annotation
from sphinx.pycode.ast import unparse as pycode_unparse


def test_empty_tuple_annotation_parsing():
    """Test that empty tuple annotations can be parsed without IndexError."""
    # The bug occurs when parsing type annotations that have empty tuples like Tuple[()]
    # In sphinx/domains/python.py line 113: result.pop() was called without checking
    # if result was empty, which happens when node.elts is empty
    
    try:
        # This call should succeed (not raise IndexError)
        result = _parse_annotation("Tuple[()]")
        # If we get here, the fix is working - no IndexError was thrown
        assert result is not None
        # The most basic assertion: shouldn't crash with IndexError 
        assert len(result) >= 0  # should at least return some structure (may be empty)
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError(f"Empty tuple annotation parsing still raises IndexError: {e}")
        else:
            raise  # Some other IndexError, we raise it


def test_empty_tuple_annotation_variants():
    """Test various empty tuple annotation formats."""
    annotations = [
        "Tuple[()]",
        "tuple[()]",
    ]
    
    for annotation in annotations:
        try:
            result = _parse_annotation(annotation)
            # If we reach here, the fix is in place 
            assert result is not None
            assert len(result) >= 0
        except IndexError as e:
            if "pop from empty list" in str(e):
                raise AssertionError(f"Empty tuple annotation {annotation} still raises IndexError: {e}")
            else:
                raise


def test_pycode_empty_tuple_handling():
    """Test that empty tuple is handled properly in pycode ast module."""
    # In sphinx/pycode/ast.py line 118 was: return ", ".join(unparse(e) for e in node.elts) 
    # This path was also a potential issue when elts was empty
    
    # Create AST node representing empty tuple to test specific case
    empty_tuple = ast.Tuple(elts=[], ctx=ast.Load())
    
    try:
        # This should not raise IndexError or have broken behavior
        result = pycode_unparse(empty_tuple)
        assert result is not None
        # Check that empty tuple case returns appropriate string
        # The fix should make it return "()" for empty tuple annotation
        assert result == "()"  # This is the expected output in fixed version
    except IndexError as e:
        if "pop from empty list" in str(e):
            raise AssertionError(f"pycode AST unparse raises IndexError: {e}")
        else:
            raise