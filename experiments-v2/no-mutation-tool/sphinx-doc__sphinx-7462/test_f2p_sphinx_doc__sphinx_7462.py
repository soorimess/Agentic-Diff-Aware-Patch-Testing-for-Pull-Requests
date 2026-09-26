"""
Regression test for empty tuple type annotation IndexError.

This test ensures that empty tuple type annotations like Tuple[()] don't
cause an IndexError in the python domain's unparse function.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation():
    """Test that empty tuple annotation doesn't raise IndexError."""
    # This should not raise IndexError - the main bug fix
    result = _parse_annotation("Tuple[()]")
    assert isinstance(result, list)
    # If we get here without IndexError, the fix works
    assert len(result) >= 0  # Should be a valid list


def test_empty_tuple_annotation_with_complex_types():
    """Test empty tuple with more complex type annotations."""
    # This should not raise IndexError - the main bug fix
    result = _parse_annotation("Tuple[(), int]")
    assert isinstance(result, list)
    # If we get here without IndexError, the fix works
    assert len(result) >= 0  # Should be a valid list


def test_empty_tuple_in_nested_context():
    """Test empty tuple in nested type contexts."""
    # This should not raise IndexError - the main bug fix  
    result = _parse_annotation("List[Tuple[()]]")
    assert isinstance(result, list)
    # If we get here without IndexError, the fix works
    assert len(result) >= 0  # Should be a valid list


def test_non_empty_tuple_still_works():
    """Ensure non-empty tuples still work correctly."""
    result = _parse_annotation("Tuple[int, str]")
    assert isinstance(result, list)
    # Should have some elements
    assert len(result) >= 3


def test_pycode_ast_empty_tuple_direct():
    """Test pycode ast unparse with empty tuple directly."""
    from sphinx.pycode.ast import unparse
    import ast
    
    # Test the pycode/ast.py fix directly
    empty_tuple = ast.Tuple(elts=[])
    result = unparse(empty_tuple)
    # Should return "()" not an empty string
    assert result == "()"


def test_pycode_ast_non_empty_tuple_direct():
    """Test pycode ast unparse with non-empty tuple directly."""
    from sphinx.pycode.ast import unparse
    import ast
    
    # Test that non-empty tuples still work
    non_empty_tuple = ast.Tuple(elts=[ast.Name(id='int'), ast.Name(id='str')])
    result = unparse(non_empty_tuple)
    assert result == "int, str"


if __name__ == "__main__":
    test_empty_tuple_annotation()
    test_empty_tuple_annotation_with_complex_types()
    test_empty_tuple_in_nested_context()
    test_non_empty_tuple_still_works()
    test_pycode_ast_empty_tuple_direct()
    test_pycode_ast_non_empty_tuple_direct()
    print("All tests passed!")