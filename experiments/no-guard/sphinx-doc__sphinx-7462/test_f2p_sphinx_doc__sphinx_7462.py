"""
Test for handling empty tuple type annotations in Sphinx.

This regression test ensures that empty tuple type annotations like
Tuple[()] don't cause an IndexError and are properly handled.
"""

import ast
import pytest

from sphinx.domains.python import _parse_annotation
from sphinx.pycode.ast import unparse as pycode_unparse


def test_empty_tuple_annotation_no_indexerror():
    """Test that empty tuple annotations do not raise IndexError."""
    # This is the case that caused IndexError: pop from empty list in the original code
    annotation = "Tuple[()]"
    
    # After fix, this should NOT raise an IndexError
    try:
        result = _parse_annotation(annotation)
        # If we get here without exception, that's good
        assert result is not None
    except IndexError as e:
        if "pop from empty list" in str(e):
            pytest.fail(f"IndexError still raised: {e}")
        else:
            raise  # Re-raise if it's a different IndexError


def test_empty_tuple_annotation_returns_valid_result():
    """Test that empty tuple annotations return a valid result."""
    # This tests that the function correctly parses empty tuple annotations
    annotation = "Tuple[()]"
    
    # Should parse successfully without raising IndexError
    result = _parse_annotation(annotation)
    
    # Result should be a list of nodes (not None or error)
    assert isinstance(result, list)
    # Should contain reasonable nodes
    assert len(result) >= 0


def test_empty_tuple_in_subscript_handling():
    """Test that empty tuple handling in subscript works correctly."""
    # Test that we can parse a function annotation with empty tuple 
    try:
        # This checks that the test case from bug report works
        # def foo() -> Tuple[()]: return ()
        result = _parse_annotation("Tuple[()]")
        assert result is not None
        assert isinstance(result, list)
    except IndexError as e:
        if "pop from empty list" in str(e):
            pytest.fail(f"IndexError still raised in subscript handling: {e}")
        else:
            raise  # Re-raise different errors


def test_empty_tuple_unparse_pycode():
    """Test that pycode ast unparse handles empty tuples correctly."""
    # Test the pycode version specific to the second part of the bug fix
    empty_tuple = ast.Tuple(elts=[])
    
    # This should return "()" without error, not crash with IndexError
    result = pycode_unparse(empty_tuple)
    assert result == "()"


def test_non_empty_tuple_unparse_pycode():
    """Test that pycode ast unparse handles non-empty tuples correctly."""
    # Test the pycode version with non-empty tuples to hit the if branch
    non_empty_tuple = ast.Tuple(elts=[ast.Name(id="str")])
    
    # This should return "str" without error 
    result = pycode_unparse(non_empty_tuple)
    assert result == "str"


def test_empty_tuple_in_subscript_pycode():
    """Test that empty tuple in subscript works in pycode ast."""
    # Create AST for Tuple[()]
    name = ast.Name(id='Tuple')
    empty_tuple = ast.Tuple(elts=[])
    subscript = ast.Subscript(value=name, slice=empty_tuple, ctx=ast.Load())
    
    # This should return "Tuple[()]" without error
    result = pycode_unparse(subscript)
    assert result == "Tuple[()]"