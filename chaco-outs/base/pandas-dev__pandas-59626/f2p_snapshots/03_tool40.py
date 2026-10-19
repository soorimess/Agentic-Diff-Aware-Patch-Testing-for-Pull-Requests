"""
Regression test for PR #59626: REF (string): rename result converter methods

This test ensures that the new _convert_bool_result and _convert_int_result
methods exist and are accessible on ArrowStringArray.
"""
import pytest

from pandas.core.arrays.string_arrow import ArrowStringArray


class TestArrowStringArrayResultConverters:
    """Test that the new result converter methods exist on ArrowStringArray."""

    def test_convert_bool_result_exists(self):
        """Test that _convert_bool_result method exists on ArrowStringArray."""
        # Create ArrowStringArray properly using _from_sequence
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        # This should fail before the change and pass after
        assert hasattr(arr, "_convert_bool_result")
        
    def test_convert_int_result_exists(self):
        """Test that _convert_int_result method exists on ArrowStringArray."""
        # Create ArrowStringArray properly using _from_sequence
        arr = ArrowStringArray._from_sequence(["a", "b", "c"])
        # This should fail before the change and pass after
        assert hasattr(arr, "_convert_int_result")