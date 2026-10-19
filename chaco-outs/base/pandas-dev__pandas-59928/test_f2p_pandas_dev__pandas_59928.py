"""
Regression tests for PR #59928:
- Use `is_iterator` instead of one off `ensure_has_len`
- Just process data twice instead of n times in `trim_front`
"""

import pytest


def test_reindex_iterator_handling():
    """Test reindex with iterator targets - core functionality change.
    
    This test verifies the specific change from ensure_has_len to is_iterator
    in the reindex method, ensuring correct handling of iterator targets.
    """
    from pandas import Index
    
    # Create test index
    idx = Index(['a', 'b', 'c', 'd', 'e', 'f'])
    
    # Test with iterator (generator) - this exercises the is_iterator logic
    target_gen = (x for x in ['f', 'c', 'a', 'e', 'b'])
    
    # This should work correctly with the new implementation
    result = idx.reindex(target_gen)
    
    # Verify correct behavior
    expected_index = Index(['f', 'c', 'a', 'e', 'b'])
    expected_values = [5, 2, 0, 4, 1]
    
    assert result[0].equals(expected_index)
    assert list(result[1]) == expected_values


def test_trim_front_algorithm_behavior():
    """Test trim_front algorithm behavior - demonstrates the improved approach.
    
    The trim_front function was changed from a loop-based approach to a 
    minimum-leading-spaces approach for better efficiency.
    """
    from pandas.core.indexes.base import trim_front
    
    # Test cases that demonstrate the algorithmic improvement
    test_cases = [
        # Basic case
        ([" a", " b", " c"], ["a", "b", "c"]),
        
        # Multiple leading spaces  
        (["   a", "  b", " c"], ["  a", " b", "c"]),
        
        # Mixed leading spaces
        (["  a", "   b", " c", "    d"], [" a", "  b", "c", "   d"]),
        
        # Edge cases
        ([], []),
        (["a", "b", "c"], ["a", "b", "c"]),
        (["   ", "  ", " "], ["  ", " ", ""]),
    ]
    
    for input_strings, expected in test_cases:
        result = trim_front(input_strings)
        assert result == expected, f"Failed for input {input_strings}: expected {expected}, got {result}"


def test_trim_front_specific_cases():
    """Test specific cases that show the algorithm works correctly."""
    from pandas.core.indexes.base import trim_front
    
    # Test case that shows the specific improvement
    # Old algorithm: would process multiple iterations
    # New algorithm: processes once 
    input_data = ["    x", "   y", "  z", " a"]
    result = trim_front(input_data)
    
    # Should remove minimum leading spaces (1) from all strings
    expected = ["   x", "  y", " z", "a"]
    assert result == expected
    
    # Test with no leading spaces
    result2 = trim_front(["a", "b", "c"])
    assert result2 == ["a", "b", "c"]
    
    # Test with all spaces
    result3 = trim_front(["   ", "  ", " "])
    assert result3 == ["  ", " ", ""]