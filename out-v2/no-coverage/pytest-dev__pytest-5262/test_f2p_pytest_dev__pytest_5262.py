# -*- coding: utf-8 -*-
"""
Regression test for pytest-dev/pytest#5262

This test ensures that EncodedFile.mode does not include 'b' (binary) 
as this causes youtube-dl to fail when it tries to write bytes to 
pytest captured output.
"""
import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_no_binary_flag():
    """Test that EncodedFile.mode does not include 'b' flag."""
    # Create a mock buffer with binary mode (as would be created by real file operations)
    class MockBuffer:
        def __init__(self):
            self.mode = "rb+"  # This is what would be set by a real binary buffer
    
    mock_buffer = MockBuffer()
    encoded_file = EncodedFile(mock_buffer, "utf-8")
    
    # The fix ensures that mode property strips 'b' from the underlying buffer mode
    # Before fix: would return "rb+" (with 'b')  
    # After fix: should return "r+" (without 'b')
    assert encoded_file.mode == "r+"


def test_encodedfile_mode_strips_binary_flag_completely():
    """Test that various binary modes are properly stripped."""
    # Test different binary mode scenarios
    test_modes = ["rb", "wb", "ab", "rb+", "wb+", "ab+", "r+b", "w+b", "a+b"]
    
    for original_mode in test_modes:
        class MockBuffer:
            def __init__(self, mode):
                self.mode = mode
        
        mock_buffer = MockBuffer(original_mode)
        encoded_file = EncodedFile(mock_buffer, "utf-8")
        
        # The mode should not contain 'b' 
        expected_mode = original_mode.replace("b", "")
        assert encoded_file.mode == expected_mode, f"Failed for mode {original_mode}: got {encoded_file.mode}, expected {expected_mode}"