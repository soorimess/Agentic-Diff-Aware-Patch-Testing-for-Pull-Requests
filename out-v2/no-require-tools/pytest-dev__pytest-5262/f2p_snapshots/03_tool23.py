"""
Regression test for pytest issue where EncodedFile mode includes 'b' (binary)
when it shouldn't. This causes youtube-dl to fail when trying to write bytes
to pytest captured output.
"""

from _pytest.capture import EncodedFile


def test_encodedfile_mode_strips_binary_flag():
    """Test that EncodedFile mode property strips 'b' from underlying buffer mode.
    
    This is needed because youtube-dl checks the mode to decide whether to write
    bytes or strings to the output stream. The mode should not include 'b' to 
    indicate text mode to youtube-dl.
    """
    # Create a mock buffer with binary mode to simulate real scenario
    class MockBuffer:
        def __init__(self, mode):
            self.mode = mode
    
    # Test that the mode property strips 'b' from binary modes
    test_cases = [
        ("rb+", "r+"),
        ("wb+", "w+"), 
        ("ab+", "a+"),
        ("r+b", "r+"),
        ("w+b", "w+"),
        ("a+b", "a+"),
    ]
    
    for input_mode, expected_mode in test_cases:
        buffer = MockBuffer(input_mode)
        encoded_file = EncodedFile(buffer, "utf-8")
        
        # The fix should strip 'b' from the mode so youtube-dl sees text mode
        actual_mode = encoded_file.mode
        assert actual_mode == expected_mode, (
            f"Mode should strip 'b' from {input_mode}: got {actual_mode}, expected {expected_mode}"
        )