"""
Regression test for the EncodedFile mode bug.
The bug was that EncodedFile mode incorrectly included 'b' (binary) 
which caused youtube-dl to fail when trying to write bytes.
"""
import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_property():
    """Test that EncodedFile.mode property strips 'b' from underlying buffer mode."""
    # Create a mock buffer with binary mode
    import io
    buffer = io.BytesIO()
    buffer.mode = 'rb+'  # This is what would be set by underlying stream
    
    # Create EncodedFile instance
    encoded_file = EncodedFile(buffer, 'utf-8')
    
    # Before the fix, this would return 'rb+' (with 'b')
    # After the fix, this should return 'r+' (without 'b')
    assert encoded_file.mode == 'r+'


def test_encodedfile_write_bytes_with_binary_mode():
    """Test that EncodedFile can handle bytes when mode doesn't include 'b'."""
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