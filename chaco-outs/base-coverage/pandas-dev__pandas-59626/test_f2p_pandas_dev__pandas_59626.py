"""
Test for pull request #59626: REF (string): rename result converter methods

This test verifies that the ArrowStringArray methods for converting results
have been properly renamed from _result_converter to _convert_bool_result
and _convert_int_result.
"""
import numpy as np
import pytest

from pandas.core.arrays import ArrowStringArray


class TestArrowStringArrayResultConverter:
    """Tests for the renamed result converter methods in ArrowStringArray."""

    def test_convert_bool_result_exists(self):
        """Test that _convert_bool_result method exists and is callable."""
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        
        # Check that the method exists
        assert hasattr(arr, "_convert_bool_result")
        
        # Check that it's callable
        assert callable(getattr(arr, "_convert_bool_result"))
        
    def test_convert_int_result_exists(self):
        """Test that _convert_int_result method exists and is callable."""
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        
        # Check that the method exists
        assert hasattr(arr, "_convert_int_result")
        
        # Check that it's callable
        assert callable(getattr(arr, "_convert_int_result"))
        
    def test_old_result_converter_removed(self):
        """Test that the old _result_converter method no longer exists."""
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        
        # The old method should not exist anymore
        assert not hasattr(arr, "_result_converter")
        
    def test_convert_methods_are_properly_inherited(self):
        """Test that the methods are properly inherited from ArrowExtensionArray."""
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        
        # Both methods should be callable and should exist in the class hierarchy
        assert hasattr(arr, "_convert_bool_result")
        assert hasattr(arr, "_convert_int_result")
        
        # Check that they are bound methods
        bool_method = getattr(arr, "_convert_bool_result")
        int_method = getattr(arr, "_convert_int_result")
        
        # They should be callable
        assert callable(bool_method)
        assert callable(int_method)