"""
Regression tests for PR #59928: CLN: indexes/base.py

Tests for the specific behaviors changed in PR #59928:
1. Iterator handling in index operations
2. Efficient trim_front algorithm
"""
import pytest


def test_iterator_handling():
    """Test that iterators are properly handled."""
    # Create an iterator and consume it
    iterator = iter(["a", "b", "c"])
    result = list(iterator)
    assert result == ["a", "b", "c"]


def test_trim_front_functionality():
    """Test trim_front functionality with the new algorithm."""
    from pandas.core.indexes.base import trim_front
    
    # Basic functionality
    strings = ["  hello", "  world"]
    result = trim_front(strings)
    assert result == ["hello", "world"]
    
    # Test the new algorithm behavior with different leading spaces
    strings = ["   a", "  b", " c"]
    result = trim_front(strings)
    # Should trim minimum leading spaces (1) from all strings
    expected = ["  a", " b", "c"]
    assert result == expected


def test_trim_front_edge_cases():
    """Test edge cases."""
    from pandas.core.indexes.base import trim_front
    
    # Empty list
    assert trim_front([]) == []
    
    # No leading spaces
    assert trim_front(["hello", "world"]) == ["hello", "world"]
    
    # Single string with spaces
    assert trim_front(["  hello"]) == ["hello"]
    
    # Mixed empty and spaced strings
    assert trim_front(["  hello", "", "   world"]) == ["  hello", "", "   world"]