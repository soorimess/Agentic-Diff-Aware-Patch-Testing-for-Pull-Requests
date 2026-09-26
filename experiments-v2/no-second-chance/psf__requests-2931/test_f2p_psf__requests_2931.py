#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for PSF requests issue #2931
Tests that binary payloads work correctly with PUT requests.
"""

import requests
from requests.models import PreparedRequest


def test_binary_payload_in_put_request():
    """Test that binary payload data works with PUT requests (issue #2931)"""
    # This should work - binary data in PUT request
    data = u"ööö".encode("utf-8")
    
    # Create a prepared request to test the encoding behavior
    req = PreparedRequest()
    
    # This should not raise an exception
    try:
        req.prepare(method='PUT', url='http://httpbin.org/put', data=data)
        # If we get here without exception, the binary data was handled correctly
        assert req.body == data
    except Exception as e:
        # If this fails, it's the bug we're testing for
        raise AssertionError("Binary payload handling failed: %s" % str(e))


def test_encode_params_with_binary_data():
    """Test that _encode_params handles binary data correctly"""
    from requests.models import RequestEncodingMixin
    
    # Test with binary data (this is what was failing)
    binary_data = u"ööö".encode("utf-8")
    
    # This should not call to_native_string on binary data
    result = RequestEncodingMixin._encode_params(binary_data)
    
    # The result should be the same binary data (not processed by to_native_string)
    assert result == binary_data


def test_encode_params_with_string_data():
    """Test that _encode_params still works with string data"""
    from requests.models import RequestEncodingMixin
    
    # Test with string data 
    string_data = "test=123"
    
    # This should work as before
    result = RequestEncodingMixin._encode_params(string_data)
    
    # The result should be processed by to_native_string
    assert isinstance(result, str) or isinstance(result, bytes)


def test_encode_params_with_bytes_data():
    """Test that _encode_params with bytes data returns bytes (the main fix)"""
    from requests.models import RequestEncodingMixin
    
    # Test with bytes data - this is the specific case that was broken
    binary_data = u"test=ööö".encode("utf-8")
    
    # Before the fix, this would call to_native_string(binary_data) which would fail
    # After the fix, it should return the binary data directly
    result = RequestEncodingMixin._encode_params(binary_data)
    
    # Should return the same bytes object
    assert result is binary_data