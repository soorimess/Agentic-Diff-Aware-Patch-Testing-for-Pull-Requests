#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for requests issue where binary payload fails due to 
calling to_native_string on bytes data.
"""

import unittest
import requests
from requests.models import PreparedRequest


class TestBinaryPayloadRegression(unittest.TestCase):
    
    def test_binary_payload_in_encode_params(self):
        """Test that binary payload data works correctly in _encode_params"""
        # This is the exact case from the bug report
        # u"ööö".encode("utf-8") produces bytes
        binary_data = u"ööö".encode("utf-8")
        
        # Create a PreparedRequest to test _encode_params directly
        req = PreparedRequest()
        
        # This should not raise an exception
        # The bug was that to_native_string would be called on bytes data
        # which would try to decode it with ascii encoding and fail
        try:
            result = req._encode_params(binary_data)
            # If we get here without exception, the fix works
            # The result should be the same bytes object
            self.assertEqual(result, binary_data)
        except UnicodeDecodeError:
            # This is the error that would occur with the old code
            self.fail("UnicodeDecodeError raised when processing binary data in _encode_params")
    
    def test_binary_payload_in_request(self):
        """Test that binary payload works in actual request"""
        # This tests the exact case from the bug report
        binary_data = u"ööö".encode("utf-8")
        
        # This should not raise an exception
        # The bug was that the request would fail due to to_native_string 
        # being called on binary data in _encode_params
        try:
            # We can't actually make the HTTP request in this test environment,
            # but we can test that the internal processing doesn't fail
            from requests.models import PreparedRequest
            req = PreparedRequest()
            
            # Test that the data can be processed without UnicodeDecodeError
            # This simulates what happens internally when preparing a request
            req.prepare_method('PUT')
            req.prepare_url('http://httpbin.org/put', None)
            
            # The key test is that _encode_params doesn't fail on binary data
            result = req._encode_params(binary_data)
            self.assertEqual(result, binary_data)
            
        except UnicodeDecodeError as e:
            self.fail("UnicodeDecodeError raised when processing binary data in request: %s" % str(e))


if __name__ == '__main__':
    unittest.main()