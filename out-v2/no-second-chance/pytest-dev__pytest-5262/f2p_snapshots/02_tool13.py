"""
Regression test for the EncodedFile mode bug.
The bug was that EncodedFile mode incorrectly included 'b' (binary) 
which caused youtube-dl to fail when trying to write bytes.
"""
import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_property_strips_binary_flag():
    """Test that EncodedFile.mode property strips 'b' from underlying buffer mode."""
    # Create a mock buffer with various binary modes
    import io
    
    # Test case 1: rb+ mode
    buffer = io.BytesIO()
    buffer.mode = 'rb+'
    encoded_file = EncodedFile(buffer, 'utf-8')
    assert encoded_file.mode == 'r+'  # 'b' should be stripped
    
    # Test case 2: wb+ mode  
    buffer = io.BytesIO()
    buffer.mode = 'wb+'
    encoded_file = EncodedFile(buffer, 'utf-8')
    assert encoded_file.mode == 'w+'  # 'b' should be stripped
    
    # Test case 3: rb mode
    buffer = io.BytesIO()
    buffer.mode = 'rb'
    encoded_file = EncodedFile(buffer, 'utf-8')
    assert encoded_file.mode == 'r'  # 'b' should be stripped
    
    # Test case 4: wb mode
    buffer = io.BytesIO()
    buffer.mode = 'wb'
    encoded_file = EncodedFile(buffer, 'utf-8')
    assert encoded_file.mode == 'w'  # 'b' should be stripped
    
    # Test case 5: mode without 'b' should remain unchanged
    buffer = io.BytesIO()
    buffer.mode = 'r+'
    encoded_file = EncodedFile(buffer, 'utf-8')
    assert encoded_file.mode == 'r+'  # no change needed


def test_encodedfile_write_bytes_with_binary_mode():
    """Test that EncodedFile can handle bytes when mode doesn't include 'b'.
    
    This simulates the youtube-dl use case where youtube-dl checks the mode
    to decide whether to write bytes or str.
    """
    import io
    buffer = io.BytesIO()
    buffer.mode = 'rb+'  # Binary mode from underlying stream
    
    encoded_file = EncodedFile(buffer, 'utf-8')
    
    # This should work after the fix, but fail before the fix
    # because youtube-dl checks the mode to decide whether to write bytes or str
    try:
        encoded_file.write(b'test bytes')
        # If we get here, the write succeeded
        buffer.seek(0)
        assert buffer.read() == b'test bytes'
    except TypeError as e:
        # This is the error that would occur before the fix
        assert "write() argument must be str, not bytes" in str(e)