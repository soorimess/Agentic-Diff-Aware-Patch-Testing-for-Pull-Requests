"""
Regression test for pytest issue where EncodedFile mode incorrectly 
includes 'b' (binary) character.
"""
import io
from _pytest.capture import EncodedFile


def test_encodedfile_mode_no_binary_flag():
    """Test that EncodedFile.mode does not include 'b' for binary mode."""
    # Create a buffer with binary mode
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    
    # Create EncodedFile wrapping this buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # The mode should not contain 'b' even though the underlying buffer has 'b'
    assert "b" not in encoded_file.mode
    assert encoded_file.mode == "w+"


def test_encodedfile_mode_preserves_non_binary_modes():
    """Test that EncodedFile.mode preserves non-binary modes correctly."""
    # Test with text mode
    buffer = io.StringIO()
    buffer.mode = "r+"
    
    encoded_file = EncodedFile(buffer, "utf-8")
    assert encoded_file.mode == "r+"


def test_encodedfile_write_bytes_raises_typeerror():
    """Test that EncodedFile.write() raises TypeError when passed bytes (before fix)."""
    # Create a buffer with binary mode
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    
    # Create EncodedFile wrapping this buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # This should raise TypeError because EncodedFile expects strings, not bytes
    # This is the core issue that youtube-dl hits
    try:
        encoded_file.write(b"test bytes")
        # If we get here without exception, that's unexpected
        assert False, "Expected TypeError when writing bytes to EncodedFile"
    except TypeError as e:
        assert "write() argument must be str, not bytes" in str(e)