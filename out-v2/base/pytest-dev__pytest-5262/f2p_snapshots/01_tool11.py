# -*- coding: utf-8 -*-
"""
Regression test for pytest-dev/pytest#5262
_pytest.capture.EncodedFile mode should not include `b` (binary)

This test ensures that EncodedFile.mode property strips 'b' from the underlying
buffer's mode, which fixes an issue where youtube-dl would try to write bytes
to a non-binary mode file.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_strips_binary_flag():
    """Test that EncodedFile.mode property strips 'b' from underlying buffer mode."""
    # Create a buffer with binary mode
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    
    # Create EncodedFile wrapping the buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # The mode should not contain 'b' 
    assert "b" not in encoded_file.mode
    assert encoded_file.mode == "w+"
    
    # Test with read binary mode
    buffer2 = io.BytesIO()
    buffer2.mode = "rb+"
    encoded_file2 = EncodedFile(buffer2, "utf-8")
    assert "b" not in encoded_file2.mode
    assert encoded_file2.mode == "r+"


def test_encodedfile_mode_preserves_non_binary_modes():
    """Test that EncodedFile.mode works correctly with non-binary modes."""
    # Test with text mode
    buffer = io.StringIO()
    buffer.mode = "w"
    
    encoded_file = EncodedFile(buffer, "utf-8")
    assert encoded_file.mode == "w"


def test_encodedfile_write_bytes_raises_typeerror():
    """Test that EncodedFile.write still raises TypeError for bytes (before fix)."""
    # Create a buffer with binary mode
    buffer = io.BytesIO()
    buffer.mode = "wb+"
    
    # Create EncodedFile wrapping the buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # This should raise TypeError because the mode doesn't contain 'b'
    # but the underlying buffer is binary, which is the core issue
    with pytest.raises(TypeError, match="write\\(\\) argument must be str, not bytes"):
        encoded_file.write(b"test bytes")


def test_youtube_dl_compatibility():
    """Test that reproduces the youtube-dl compatibility issue."""
    # This test simulates what youtube-dl does:
    # 1. Check if mode contains 'b' to decide whether to write bytes or str
    # 2. If mode doesn't contain 'b', it writes strings
    # 3. If mode contains 'b', it writes bytes
    
    buffer = io.BytesIO()
    buffer.mode = "wb+"  # This is what a real file would have
    
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # Before the fix, youtube-dl would see "wb+" and try to write bytes
    # But EncodedFile.write() only accepts strings, causing TypeError
    # After the fix, youtube-dl should see "w+" and write strings
    
    # The key assertion: mode should not contain 'b' so youtube-dl writes strings
    assert "b" not in encoded_file.mode
    assert encoded_file.mode == "w+"
    
    # This should work - writing a string (not bytes)
    try:
        encoded_file.write("test string")
        # If we get here without exception, it means youtube-dl would write strings
        # which EncodedFile can handle
    except TypeError:
        # This would be the old behavior that causes the bug
        pytest.fail("youtube-dl compatibility issue: EncodedFile.write() raised TypeError")