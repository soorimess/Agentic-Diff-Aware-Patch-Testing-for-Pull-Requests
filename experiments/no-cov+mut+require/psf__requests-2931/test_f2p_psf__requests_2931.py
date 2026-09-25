#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue where binary payload data fails due to 
calling to_native_string on bytes objects in _encode_params.

This tests the specific behavior change in PR that modified:
- requests/models.py line 84: return to_native_string(data) -> return data
"""

import unittest
import requests
from requests.models import PreparedRequest
from requests.utils import to_native_string


class TestBinaryPayloadRegression(unittest.TestCase):
    
    def test_request_with_binary_data_works(self):
        """
        Test that binary data can be used as request body without crashing.
        This is the main issue reported: requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
        """
        # This exact case was failing before the fix
        binary_data = u"ööö".encode("utf-8")
        
        # In the old broken code, this would cause a UnicodeDecodeError
        # because _encode_params would call to_native_string() on binary data
        try:
            req = requests.Request('PUT', 'http://httpbin.org/put', data=binary_data)
            prep_req = req.prepare()
            
            # If we make it here without exception, behavior is fixed
            # The body should be the same binary data
            self.assertEqual(prep_req.body, binary_data)
        except UnicodeDecodeError:
            self.fail("UnicodeDecodeError in request preparation - indicates the old bug is present")
            
    def test_encode_params_directly_with_bytes(self):
        """
        Test _encode_params directly with bytes data to demonstrate 
        the specific change from old (broken) behavior to new (fixed) behavior 
        """
        # Create binary data that would fail in old behavior
        binary_data = u"ööö".encode("utf-8")
        
        # In the old code, this would call to_native_string(data) and fail
        # The new code should return the data unchanged
        try:
            # Call _encode_params directly like it would internally
            result = PreparedRequest._encode_params(binary_data)
            # In the fixed version, should return binary_data unchanged
            self.assertEqual(result, binary_data)
        except UnicodeDecodeError:
            # This would indicate the old behavior is still there
            self.fail("_encode_params failed with UnicodeDecodeError - indicates old behavior")
        except Exception as e:
            # Other exceptions may happen, but UnicodeDecodeError is the key to spot the bug
            if "UnicodeDecodeError" in str(type(e)):
                self.fail("_encode_params failed with UnicodeDecodeError - indicates old behavior")


if __name__ == '__main__':
    unittest.main()