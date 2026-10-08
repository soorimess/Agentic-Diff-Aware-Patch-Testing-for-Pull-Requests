"""
Regression test for pytest issue where EncodedFile mode includes 'b' (binary)
when it shouldn't. This causes youtube-dl to fail when trying to write bytes
to pytest captured output.
"""

import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_property():
    """Test that EncodedFile mode property strips 'b' from underlying buffer mode."""
    # Create a mock buffer with binary mode
    class MockBuffer:
        def __init__(self, mode):
            self.mode = mode
    
    # Test with different buffer modes
    test_modes = ["rb+", "wb+", "ab+", "r+b", "w+b", "a+b"]
    
    for mode in test_modes:
        buffer = MockBuffer(mode)
        encoded_file = EncodedFile(buffer, "utf-8")
        
        # Before the fix, this would return the original mode with 'b'
        # After the fix, this should return the mode without 'b'
        actual_mode = encoded_file.mode
        expected_mode = mode.replace("b", "")
        
        assert actual_mode == expected_mode, f"Mode mismatch for {mode}: got {actual_mode}, expected {expected_mode}"


def test_encodedfile_write_behavior():
    """Test that EncodedFile write method still works correctly."""
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


def test_encodedfile_mode_observation():
    """Test the specific observable behavior that differs before/after fix."""
    # Create a mock buffer with binary mode to simulate the real scenario
    class MockBuffer:
        def __init__(self, mode):
            self.mode = mode
            
        def write(self, data):
            # This simulates what happens in the real write method
            if isinstance(data, str):
                # This is what happens in the real code when it's a string
                # It gets encoded to bytes
                pass
            elif isinstance(data, bytes):
                # This is what youtube-dl would try to write
                # If the mode includes 'b', this should work
                # If the mode doesn't include 'b', this should raise TypeError
                pass
    
    # Test the scenario that causes youtube-dl to fail
    buffer = MockBuffer("rb+")  # Binary mode - this is the problem case
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # The mode should NOT include 'b' after the fix
    actual_mode = encoded_file.mode
    expected_mode = "r+"  # Should not have 'b'
    
    assert actual_mode == expected_mode, f"Mode should not include 'b': got {actual_mode}"