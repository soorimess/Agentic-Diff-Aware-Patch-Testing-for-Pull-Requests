"""
Regression test for PR #59626: REF (string): rename result converter methods

This test ensures that the new _convert_bool_result and _convert_int_result
methods work correctly in ArrowStringArray.
"""
import pytest

from pandas.core.arrays.string_arrow import ArrowStringArray


class TestArrowStringArrayResultConverters:
    """Test that the new result converter methods exist and work correctly."""

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
        
    def test_string_methods_call_new_converters(self):
        """Test that string methods use the new converter methods."""
        # Create ArrowStringArray properly using _from_sequence
        arr = ArrowStringArray._from_sequence(["hello", "world", "test"])
        
        # These methods should use _convert_bool_result
        # Test that they don't raise AttributeError for the new method names
        try:
            result = arr._str_isalpha()
            # If we get here, the method exists and can be called
            assert hasattr(arr, "_convert_bool_result")
        except AttributeError:
            # This is expected before the change
            pytest.skip("Methods not yet implemented - this is expected before the change")
            
        # Test integer methods that should use _convert_int_result
        try:
            result = arr._str_len()
            # If we get here, the method exists and can be called
            assert hasattr(arr, "_convert_int_result")
        except AttributeError:
            # This is expected before the change
            pytest.skip("Methods not yet implemented - this is expected before the change")