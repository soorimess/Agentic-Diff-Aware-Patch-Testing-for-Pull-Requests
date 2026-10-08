"""
Regression test for pytest issue where EncodedFile mode incorrectly
includes 'b' (binary) mode character.

This test verifies that EncodedFile.mode does not include 'b' 
when the underlying buffer has binary mode, which is needed for
compatibility with libraries like youtube-dl that check mode to 
determine whether to write bytes or strings.
"""

import io
from _pytest.capture import EncodedFile


def test_encodedfile_mode_property_exists_and_strips_binary_flag():
    """Test that EncodedFile.mode property exists and strips 'b' from underlying buffer mode."""
    # Create a buffer with binary mode (like BytesIO would have)
    buffer = io.BytesIO()
    buffer.mode = "wb+"  # Binary write mode
    
    # Create EncodedFile with this buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # The bug: mode property doesn't exist, so __getattr__ returns buffer.mode = "wb+"
    # The fix: mode property should return "w+" (without 'b')
    # This is important for compatibility with youtube-dl and similar libraries
    
    # Check that mode property exists
    assert hasattr(EncodedFile, 'mode'), "EncodedFile should have a mode property"
    
    # Check that mode property strips 'b' character
    actual_mode = encoded_file.mode
    assert "b" not in actual_mode, f"Mode should not contain 'b', but got '{actual_mode}'"
    
    # For a binary buffer with write mode, it should be "w+" (text mode)
    expected_mode = "w+"
    assert actual_mode == expected_mode, f"Expected mode '{expected_mode}', got '{actual_mode}'"


def test_encodedfile_mode_compatibility_with_youtube_dl():
    """Test that EncodedFile mode is compatible with youtube-dl's mode checking logic."""
    # Create a buffer with binary mode (like BytesIO would have)
    buffer = io.BytesIO()
    buffer.mode = "wb+"  # Binary write mode
    
    # Create EncodedFile with this buffer
    encoded_file = EncodedFile(buffer, "utf-8")
    
    # youtube-dl checks mode to decide whether to write bytes or strings:
    # - if 'b' in mode, it writes bytes
    # - if 'b' not in mode, it writes strings
    
    # With the bug: mode contains 'b', so youtube-dl would write bytes
    # With the fix: mode doesn't contain 'b', so youtube-dl writes strings
    
    mode = encoded_file.mode
    assert "b" not in mode, "Mode should not contain 'b' for youtube-dl compatibility"
    
    # This should be "w+" so youtube-dl treats it as text mode and writes strings
    assert mode == "w+", f"Expected text mode 'w+', got '{mode}'"