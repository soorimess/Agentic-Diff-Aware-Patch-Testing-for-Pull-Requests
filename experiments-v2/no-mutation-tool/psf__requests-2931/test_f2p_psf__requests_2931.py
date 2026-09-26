#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for the binary payload issue in requests."""

import unittest
import requests
from requests.models import PreparedRequest


class TestBinaryPayload(unittest.TestCase):
    """Test cases for binary payload handling."""

    def test_binary_payload_with_non_ascii_bytes(self):
        """Test that binary payloads with non-ASCII bytes work correctly."""
        # This is the case mentioned in the bug report
        # The issue occurs when data is bytes containing non-ASCII characters
        data = u"ööö".encode("utf-8")
        
        # Create a prepared request to test the _encode_params method directly
        req = PreparedRequest()
        req.prepare(method='PUT', url='http://httpbin.org/put', data=data)
        
        # This should not raise an exception
        self.assertIsNotNone(req.body)

    def test_binary_payload_handling_in_encode_params(self):
        """Test the _encode_params method directly with binary data."""
        from requests.models import RequestEncodingMixin
        
        # Test with bytes data that contains non-ASCII characters
        data = u"ööö".encode("utf-8")
        
        # This should work without raising an exception
        result = RequestEncodingMixin._encode_params(data)
        # The result should be the same bytes object (since we don't call to_native_string anymore)
        self.assertEqual(result, data)

    def test_binary_payload_with_special_characters(self):
        """Test binary payload with various special characters."""
        # Test with binary data that contains various non-ASCII characters
        data = "café".encode("utf-8")
        
        req = PreparedRequest()
        req.prepare(method='PUT', url='http://httpbin.org/put', data=data)
        
        # This should not raise an exception
        self.assertIsNotNone(req.body)
        
    def test_binary_payload_with_invalid_utf8(self):
        """Test binary payload with invalid UTF-8 bytes."""
        # Create some invalid UTF-8 bytes
        data = b'\xff\xfe\xfd'
        
        req = PreparedRequest()
        req.prepare(method='PUT', url='http://httpbin.org/put', data=data)
        
        # This should not raise an exception
        self.assertIsNotNone(req.body)
        
    def test_prepare_url_with_bytes_params(self):
        """Test that prepare_url handles bytes params correctly."""
        # Test the prepare_url method directly with bytes params
        # This exercises the new code path in prepare_url where params = to_native_string(params)
        req = PreparedRequest()
        
        # This should trigger the new code path in prepare_url
        # where params = to_native_string(params) is called
        params = b"key=value"
        req.prepare_url('http://httpbin.org/get', params)
        
        # Should not raise an exception
        self.assertIsNotNone(req.url)
        
    def test_prepare_url_with_string_params(self):
        """Test that prepare_url handles string params correctly."""
        # Test the prepare_url method directly with string params
        req = PreparedRequest()
        
        # This should also trigger the new code path in prepare_url
        params = "key=value"
        req.prepare_url('http://httpbin.org/get', params)
        
        # Should not raise an exception
        self.assertIsNotNone(req.url)


if __name__ == '__main__':
    unittest.main()