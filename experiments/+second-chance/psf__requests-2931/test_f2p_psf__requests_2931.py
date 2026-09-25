#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for the binary payload issue in requests.

This test verifies the fix for: 
Request with binary payload fails due to calling to_native_string
Reported in https://github.com/kennethreitz/requests/issues/2844
"""

import unittest
from requests.models import PreparedRequest


class TestBinaryPayloadEncoding(unittest.TestCase):
    
    def test_binary_payload_in_encode_params(self):
        """Test that binary data (bytes) can be passed to _encode_params without error.
        
        This tests the core issue: when passing bytes as data (like from encoding a string)
        to requests, it should work correctly. In the old code, _encode_params would 
        try to call to_native_string(bytes) which would fail because bytes need encoding spec.
        """
        # Create a PreparedRequest instance
        req = PreparedRequest()
        
        # Binary data like what u"ööö".encode("utf-8") produces
        binary_data = u"ööö".encode("utf-8")
        
        # This should not raise an exception - the data should be passed through directly
        # In the broken version, this would call _encode_params with bytes 
        # which would call to_native_string(bytes) and that would fail on Python 3
        try:
            result = req._encode_params(binary_data)
            # Should return bytes unchanged (the fix)  
            self.assertEqual(result, binary_data)
            self.assertIsInstance(result, bytes)
        except Exception as e:
            self.fail("Failed to handle binary data in _encode_params: {}".format(e))


if __name__ == '__main__':
    unittest.main()