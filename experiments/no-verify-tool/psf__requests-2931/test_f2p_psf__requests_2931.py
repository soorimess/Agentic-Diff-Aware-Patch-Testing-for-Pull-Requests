#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test for issue #2931 - Request with binary payload fails due to calling to_native_string."""

import unittest
from requests.models import PreparedRequest


class TestBinaryPayloadHandling(unittest.TestCase):
    def test_encode_params_with_bytes_returns_bytes_unchanged(self):
        """Test that _encode_params returns bytes directly without conversion.
        
        The bug was that _encode_params called to_native_string(data) on bytes,
        which would try to decode bytes as ASCII and fail with UnicodeDecodeError
        for non-ASCII byte sequences.
        
        With the fix, bytes should be returned as-is.
        """
        req = PreparedRequest()
        
        # Binary payload data containing non-ASCII unicode characters 
        binary_data = u"ööö".encode("utf-8")
        
        # This call should not raise UnicodeDecodeError, which was the bug
        # In the buggy version, to_native_string(data) would try to decode bytes as ASCII
        try:
            result = req._encode_params(binary_data)
            # If we get here, no exception was raised
            # The fix ensures bytes are returned without conversion
            self.assertIsInstance(result, bytes)
            # The bytes should be the same object (identity check) or equal
            self.assertEqual(result, binary_data)
        except UnicodeDecodeError:
            self.fail("UnicodeDecodeError when processing bytes in _encode_params - the fix is not working correctly")

    def test_encode_params_with_str_still_works(self):
        """Test that string handling is unchanged (backward compatibility)."""
        req = PreparedRequest()
        
        # String data should be processed through to_native_string as before
        str_data = u"test"
        result = req._encode_params(str_data)
        
        # Should return a string (not bytes)
        self.assertIsInstance(result, str)
        
    def test_specific_bug_case(self):
        """Test that reproduces the exact scenario from the bug report."""
        # This is the case that worked in 2.8.1 but not in 2.9
        # requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
        binary_data = u"ööö".encode("utf-8")
        
        # The test directly verifies that this operation doesn't 
        # trigger the UnicodeDecodeError that was the bug
        req = PreparedRequest()
        
        # If to_native_string gets called on bytes with ASCII encoding,
        # it will raise UnicodeDecodeError - this is our regression test
        try:
            # This internal call path that goes through _encode_params 
            # is what was causing the bug
            req.prepare_url("http://httpbin.org/put", binary_data)  
            # If we reach here without exception, the behavior is correct
            self.assertTrue(True)
        except UnicodeDecodeError as e:
            self.fail("UnicodeDecodeError in prepare_url - bug not fixed: {}".format(e))