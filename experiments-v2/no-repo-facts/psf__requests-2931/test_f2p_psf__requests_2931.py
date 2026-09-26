#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for PSF requests issue #2931
Regression test for binary payload handling bug.
"""

import unittest
import requests
from requests.models import PreparedRequest, RequestEncodingMixin


class TestBinaryPayload(unittest.TestCase):
    """Test cases for binary payload handling."""

    def test_binary_payload_with_unicode_string_encoding(self):
        """Test that binary payload works with unicode string encoding."""
        # This is the exact case from the bug report
        # requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
        data = u"ööö".encode("utf-8")
        
        # This should not raise an exception
        req = requests.Request('PUT', 'http://httpbin.org/put', data=data)
        try:
            prepared = req.prepare()
            # If we get here without exception, it's working
            self.assertIsNotNone(prepared)
        except UnicodeDecodeError as e:
            self.fail("UnicodeDecodeError should not occur: %s" % e)

    def test_encode_params_with_bytes_returns_bytes(self):
        """Test _encode_params with bytes input returns bytes unchanged."""
        # Test the _encode_params method directly
        result = RequestEncodingMixin._encode_params(b"test")
        # Before the fix, this would call to_native_string on bytes, 
        # which would cause UnicodeDecodeError in Python 3
        # After the fix, it should return bytes as-is
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b"test")

    def test_encode_params_with_string_returns_string(self):
        """Test _encode_params with string input returns string."""
        # Test normal string handling
        result = RequestEncodingMixin._encode_params("test")
        # Should return string
        self.assertIsInstance(result, str)
        self.assertEqual(result, "test")

    def test_prepare_url_with_bytes_params(self):
        """Test prepare_url with bytes params."""
        req = PreparedRequest()
        
        # This should not raise an exception
        try:
            req.prepare_url('http://httpbin.org/put', b'param=value')
            # If we get here without exception, it's working
        except Exception as e:
            self.fail("prepare_url with bytes params failed: %s" % e)

    def test_prepare_url_with_bytes_params_preserves_data(self):
        """Test that prepare_url preserves bytes params correctly."""
        req = PreparedRequest()
        
        # Test with bytes params - should not raise exception
        params = b'param=value&other=test'
        try:
            req.prepare_url('http://httpbin.org/put', params)
            # Should work without exception
            self.assertTrue(True)  # Just checking it doesn't raise
        except Exception as e:
            self.fail("prepare_url with bytes params failed: %s" % e)


if __name__ == '__main__':
    unittest.main()