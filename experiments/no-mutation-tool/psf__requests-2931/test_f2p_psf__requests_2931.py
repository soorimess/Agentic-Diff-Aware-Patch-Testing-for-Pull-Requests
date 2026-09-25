#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for bug where binary payload fails due to calling to_native_string."""

import unittest
from requests.models import PreparedRequest


class TestBinaryPayloadEncoding(unittest.TestCase):
    """Test that validates the exact fix for handling binary data in encoding."""
    
    def test_bytes_data_returned_as_is_in_encode_params(self):
        """
        Test that demonstrates the primary behavior change in _encode_params.
        
        Before fix: When binary data passed to _encode_params, it called 
        to_native_string(data) which would try to decode bytes using ASCII
        encoding and fail with UnicodeDecodeError.
        
        After fix: Binary data is returned unchanged.
        """
        # Exactly reproduce the bug case: binary payload from UTF-8 encoding
        binary_data = u"ööö".encode("utf-8")
        
        # Test the function with the buggy behavior fixed
        req = PreparedRequest()
        
        # This demonstrates the specific fix: 
        # Line 84 changed from: return to_native_string(data)  
        # To: return data
        result = req._encode_params(binary_data)
        
        # This verifies the fix - binary data comes back unchanged
        self.assertEqual(result, binary_data)


if __name__ == '__main__':
    unittest.main()