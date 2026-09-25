"""
Regression test for Sphinx bug with empty tuple type annotations.

This test verifies that empty tuple type annotations like `Tuple[()]`
are properly handled without raising IndexError: pop from empty list.
The bug: IndexError when parsing empty tuple annotations.
"""

import pytest
from sphinx.domains.python import _parse_annotation


def test_empty_tuple_annotation_raises_indexerror_in_buggy_version():
    """
    Test that reproduces the IndexError bug when parsing empty tuple annotations.
    
    This should fail (raise IndexError) on the buggy code but pass on the fixed version.
    The test expects this to succeed only after the fix is applied.
    """
    
    # Parse an empty tuple annotation - this should work after the fix
    # but used to crash with "IndexError: pop from empty list"
    
    try:
        result = _parse_annotation("Tuple[()]")
        # If we reach here without IndexError, the fix is working
        assert result is not None
        # Basic verification - the result should be non-empty
        assert len(result) > 0
    except IndexError as e:
        if "pop from empty list" in str(e):
            # This is the exact bug we're testing for - 
            # it should only happen in the buggy version
            pytest.fail(f"IndexError: pop from empty list occurred - "
                       f"this shows the bug is present: {e}")
        else:
            raise  # Some unrelated IndexError


def test_non_empty_tuple_annotation_still_works():
    """Ensure non-empty tuple annotations still work correctly after fix."""
    # Test that normal tuple annotations still work  
    result = _parse_annotation("Tuple[int, str]")
    assert result is not None
    
    result = _parse_annotation("Tuple[int]")  
    assert result is not None


def test_empty_tuple_variations():
    """Test various forms of empty tuple annotations."""
    # Different ways empty tuple annotations can appear
    test_cases = [
        "Tuple[()]",
        "typing.Tuple[()]", 
        "tuple[()]",  # Python 3.9+ syntax
    ]
    
    for annotation in test_cases:
        # These should all work without IndexError
        result = _parse_annotation(annotation)
        assert result is not None


if __name__ == "__main__":
    # Run manually for verification
    test_empty_tuple_annotation_raises_indexerror_in_buggy_version()
    test_non_empty_tuple_annotation_still_works() 
    test_empty_tuple_variations()
    print("All manual tests completed!")