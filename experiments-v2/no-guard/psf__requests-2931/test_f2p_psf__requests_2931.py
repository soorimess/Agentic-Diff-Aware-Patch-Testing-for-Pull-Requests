#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue where binary payload fails due to calling to_native_string
in _encode_params function.

This test ensures that binary data passed to _encode_params does not get converted
to string via to_native_string, which would cause UnicodeDecodeError.
"""

import requests
from requests.models import PreparedRequest


def test_binary_payload_does_not_raise_unicode_decode_error():
    """Test that binary data in _encode_params doesn't cause UnicodeDecodeError"""
    # This is the core issue: binary data passed to _encode_params should not be 
    # converted via to_native_string which tries to decode bytes as ASCII
    
    req = PreparedRequest()
    
    # Binary data that would cause issues if converted to string
    binary_data = u"ööö".encode("utf-8")
    
    # Before the fix, this would raise UnicodeDecodeError because 
    # _encode_params would call to_native_string(binary_data) which tries to decode
    # bytes using ASCII encoding
    try:
        result = req._encode_params(binary_data)
        # After the fix, it should return the binary data as-is
        assert result == binary_data
        assert isinstance(result, bytes)
    except UnicodeDecodeError:
        raise AssertionError("Binary payload should not cause UnicodeDecodeError in _encode_params")


def test_string_payload_works_normally():
    """Test that string data in _encode_params works correctly"""
    req = PreparedRequest()
    
    # String data should work normally
    string_data = "test string"
    
    try:
        result = req._encode_params(string_data)
        # Should return the string as-is
        assert result == string_data
        assert isinstance(result, str)
    except Exception as e:
        raise AssertionError("String payload should work in _encode_params: %s" % str(e))


def test_dict_payload_works_normally():
    """Test that dict data in _encode_params works correctly"""
    req = PreparedRequest()
    
    # Dict data should work as before
    dict_data = {"key": "value"}
    
    try:
        result = req._encode_params(dict_data)
        # Should return properly encoded data
        assert isinstance(result, str) or isinstance(result, bytes)
    except Exception as e:
        raise AssertionError("Dict payload should work in _encode_params: %s" % str(e))


def test_request_with_binary_payload_works():
    """Test the exact scenario from the bug report"""
    # The exact code from the bug report that should work:
    # requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
    
    try:
        # This should not raise an exception
        from requests.models import Request
        req = Request('PUT', "http://httpbin.org/put", data=u"ööö".encode("utf-8"))
        prepared = req.prepare()
        # If we get here without exception, the binary data handling is correct
    except UnicodeDecodeError:
        raise AssertionError("Binary payload in request should not cause UnicodeDecodeError")
    except Exception as e:
        # Other exceptions are OK, we're mainly testing the UnicodeDecodeError
        if "UnicodeDecodeError" in str(type(e)):
            raise AssertionError("Binary payload in request should not cause UnicodeDecodeError")