#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue #2931.
Request with binary payload fails due to calling to_native_string
"""

import unittest
from requests.models import PreparedRequest


class TestBinaryPayload(unittest.TestCase):
    def test_binary_data_handling_in_encode_params(self):
        """
        Test that binary data (bytes) passed to _encode_params doesn't cause 
        UnicodeDecodeError by calling to_native_string on bytes.
        """
        req = PreparedRequest()
        
        # This is the exact scenario from the bug report
        # Binary data with non-ASCII characters
        binary_data = u"ööö".encode("utf-8")
        
        # Before the fix, this would raise UnicodeDecodeError
        # because to_native_string(bytes) tries to decode with ASCII
        # After the fix, this should work and return bytes as-is
        
        # The test is that we can call _encode_params without getting an exception
        try:
            result = req._encode_params(binary_data)
            # If we get here without exception, the fix works
            # The fix ensures we return data directly instead of to_native_string(data)
            self.assertEqual(result, binary_data)
        except UnicodeDecodeError:
            # This shows the bug exists - the old behavior
            self.fail("UnicodeDecodeError occurred when processing binary data in _encode_params")
            
    def test_string_data_still_works(self):
        """Ensure string data continues to work correctly"""
        req = PreparedRequest()
        
        # String data should work as before
        string_data = u"hello world"
        result = req._encode_params(string_data)
        self.assertEqual(result, string_data)


if __name__ == '__main__':
    unittest.main()