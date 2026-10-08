"""
Regression test for pytest issue where EncodedFile mode includes 'b' (binary)
when it shouldn't. This causes youtube-dl to fail when trying to write bytes
to pytest captured output.
"""

import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_strips_binary_flag():
    """Test that EncodedFile mode property strips 'b' from underlying buffer mode.
    
    This is needed because youtube-dl checks the mode to decide whether to write
    bytes or strings to the output stream. If the mode includes 'b', youtube-dl
    assumes it's a binary stream and writes bytes. If it doesn't, it writes strings.
    """
    # Create a mock buffer with binary mode to simulate real scenario
    class MockBuffer:
        def __init__(self, mode):
            self.mode = mode
    
    # Test various binary modes that would be encountered
    test_cases = [
        ("rb+", "r+"),
        ("wb+", "w+"), 
        ("ab+", "a+"),
        ("r+b", "r+"),
        ("w+b", "w+"),
        ("a+b", "a+"),
        ("rb", "r"),
        ("wb", "w"),
        ("ab", "a"),
    ]
    
    for input_mode, expected_mode in test_cases:
        buffer = MockBuffer(input_mode)
        encoded_file = EncodedFile(buffer, "utf-8")
        
        # The fix should strip 'b' from the mode
        actual_mode = encoded_file.mode
        assert actual_mode == expected_mode, (
            f"Mode should strip 'b' from {input_mode}: got {actual_mode}, expected {expected_mode}"
        )


def test_encodedfile_write_accepts_strings():
    """Test that EncodedFile write method still works correctly with strings."""
    # Create a mock buffer that captures what gets written
    class MockBuffer:
        def __init__(self):
            self.written_data = []
            
        def write(self, data):
            self.written_data.append(data)
            
        def flush(self):
            pass
            
        @property
        def mode(self):
            return "w+"  # This is what the buffer would actually have
    
    buffer = MockBuffer()
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # Test writing a string - should encode to bytes and write
    test_string = "Hello, world!"
    encoded_file.write(test_string)
    
    # The buffer should have received encoded bytes
    assert len(buffer.written_data) == 1
    assert isinstance(buffer.written_data[0], bytes)
    assert buffer.written_data[0] == test_string.encode("utf-8")


def test_encodedfile_mode_observes_binary_vs_text():
    """Test that the mode reflects the correct stream type for youtube-dl logic."""
    # This test specifically addresses the youtube-dl use case
    # youtube-dl checks mode to determine if it should write bytes or strings
    
    class MockBuffer:
        def __init__(self, mode):
            self.mode = mode
    
    # Test with binary mode - youtube-dl should see this as text mode (no 'b')
    binary_buffer = MockBuffer("rb+")  
    encoded_file = EncodedFile(binary_buffer, "utf-8")
    
    # After fix: mode should be "r+" (text mode) - youtube-dl will write strings
    # Before fix: mode would be "rb+" (binary mode) - youtube-dl would write bytes
    # But bytes writing would fail because the underlying buffer expects strings
    assert encoded_file.mode == "r+", "Mode should not include 'b' for youtube-dl compatibility"
    
    # Test with text mode
    text_buffer = MockBuffer("r+")  
    encoded_file2 = EncodedFile(text_buffer, "utf-8")
    assert encoded_file2.mode == "r+", "Text mode should remain unchanged"