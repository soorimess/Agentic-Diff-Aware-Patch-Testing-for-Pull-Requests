# -*- coding: utf-8 -*-
"""
Regression test for pytest-dev/pytest#5262
Tests that EncodedFile.mode does not include 'b' (binary) suffix.
"""
import io
import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_no_binary_suffix():
    """Test that EncodedFile.mode strips 'b' from underlying buffer mode."""
    # Create a buffer with binary mode (this simulates what happens in real usage)
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    
    # Create EncodedFile wrapping the buffer
    encoded_file = EncodedFile(buffer, encoding="utf-8")
    
    # Before the fix, this would return "wb+" (with binary indicator)
    # After the fix, this should return "w+" (without binary indicator)
    assert encoded_file.mode == "w+"
    
    # Test with different modes
    buffer2 = io.BytesIO()
    buffer2.mode = "rb+"
    encoded_file2 = EncodedFile(buffer2, encoding="utf-8")
    assert encoded_file2.mode == "r+"
    
    # Test with read-only mode
    buffer3 = io.BytesIO()
    buffer3.mode = "rb"
    encoded_file3 = EncodedFile(buffer3, encoding="utf-8")
    assert encoded_file3.mode == "r"


def test_encodedfile_write_still_works_with_strings():
    """Test that EncodedFile can still write strings (the main functionality)."""
    buffer = io.BytesIO()
    encoded_file = EncodedFile(buffer, encoding="utf-8")
    
    # This should work - writing strings
    encoded_file.write("Hello, world!")
    
    # Verify content was written
    buffer.seek(0)
    content = buffer.read().decode("utf-8")
    assert content == "Hello, world!"


def test_encodedfile_write_raises_with_bytes():
    """Test that EncodedFile still raises TypeError when writing bytes (as expected)."""
    buffer = io.BytesIO()
    encoded_file = EncodedFile(buffer, encoding="utf-8")
    
    # This should raise TypeError in Python 3
    with pytest.raises(TypeError, match="write\\(\\) argument must be str, not bytes"):
        encoded_file.write(b"Hello, world!")


def test_encodedfile_mode_is_property():
    """Test that EncodedFile.mode is a property, not just an attribute."""
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    encoded_file = EncodedFile(buffer, encoding="utf-8")
    
    # Check that mode is a property (not just a direct attribute)
    assert hasattr(encoded_file, 'mode')
    # mode should return a string, not be callable
    mode_value = encoded_file.mode
    assert isinstance(mode_value, str)
    assert mode_value == "w+"