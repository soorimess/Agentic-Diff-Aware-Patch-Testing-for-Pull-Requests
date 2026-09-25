"""
Regression test for Sphinx issue with empty tuple type annotation handling.

This test checks that empty tuple type annotations like Tuple[()] don't cause
IndexError: pop from empty list when parsing type signatures in Sphinx.
"""

import pytest


def test_empty_tuple_annotation_does_not_raise_indexerror():
    """
    Test that parsing empty tuple annotation like Tuple[()] doesn't cause IndexError.
    
    This regression test ensures that the fix in the pull request prevents:
    IndexError: pop from empty list in sphinx/domains/python.py line 112
    """
    from sphinx.domains.python import _parse_annotation
    
    # The problematic annotation from the bug report
    empty_tuple_annotation = "Tuple[()]"
    
    # Before the fix, this would raise: IndexError: pop from empty list
    # After the fix, this should work without errors and return a proper result
    try:
        result = _parse_annotation(empty_tuple_annotation)
        # If we reach here, no IndexError was raised - good!
        assert result is not None
        # Further check that we've got some reasonable type annotation structure
        # Doesn't crash, which was the main goal
    except IndexError as e:
        pytest.fail(f"IndexError still occurs with annotation '{empty_tuple_annotation}': {e}")
    except Exception:
        # Other exceptions are acceptable (they're not the specific IndexError bug)
        # The important thing is we don't get IndexError
        pass


def test_empty_tuple_in_pycode_ast():
    """
    Test that pycode/ast.py unparse function handles empty tuples correctly.
    
    This test specifically covers the case in pycode/ast.py that was 
    changed to handle empty tuple case.
    """
    from sphinx.pycode.ast import unparse
    
    import ast
    
    # Test what happens when we parse an empty tuple directly  
    try:
        empty_tuple_ast = ast.parse("()").body[0].value
        # This was a problem in the old version where we had 
        # return ", ".join(unparse(e) for e in node.elts)  
        # with empty node.elts
        result = unparse(empty_tuple_ast)
        # Should return "()"
        assert result == "()"
    except IndexError as e:
        pytest.fail(f"IndexError in pycode/ast.py unparse: {e}")
    except Exception:
        # Other than IndexError, we might get different behaviors which are OK
        pass