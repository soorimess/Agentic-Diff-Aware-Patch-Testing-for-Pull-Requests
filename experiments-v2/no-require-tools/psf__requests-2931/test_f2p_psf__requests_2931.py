#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue #2931:
Request with binary payload fails due to calling to_native_string
"""

import requests
from requests.models import PreparedRequest


def test_binary_payload_in_request_data():
    """Test that binary data can be passed as request data without failing."""
    # This is the exact case from the bug report that should work
    # u"ööö".encode("utf-8") creates bytes: b'\xc3\xb6\xc3\xb6\xc3\xb6'
    binary_data = u"ööö".encode("utf-8")
    
    # Create a PreparedRequest and try to prepare it with binary data
    req = PreparedRequest()
    
    # This should not raise an exception in the fixed version
    # but would raise an exception in the broken version
    try:
        req.prepare(method='PUT', url='http://httpbin.org/put', data=binary_data)
        # If we get here without exception, the test passes
        assert req.body == binary_data
    except Exception as e:
        # If it fails, we want to know what kind of error it is
        raise AssertionError("Binary data should be accepted as request body, but got exception: %s" % str(e))


def test_encode_params_with_binary_data():
    """Test _encode_params directly with binary data."""
    from requests.models import PreparedRequest
    
    # Test the _encode_params method directly with binary data
    binary_data = u"ööö".encode("utf-8")
    
    # This should work in the fixed version but fail in the broken version
    try:
        result = PreparedRequest._encode_params(binary_data)
        # In the fixed version, it should return the binary data as-is
        assert result == binary_data
    except Exception as e:
        raise AssertionError("Binary data should be handled by _encode_params without to_native_string conversion: %s" % str(e))


def test_encode_params_with_string_data():
    """Test that string data still works correctly."""
    from requests.models import PreparedRequest
    
    # Test with string data - should still work
    string_data = "test data"
    
    try:
        result = PreparedRequest._encode_params(string_data)
        # In the fixed version, it should return the string as-is
        assert result == string_data
    except Exception as e:
        raise AssertionError("String data should still work with _encode_params: %s" % str(e))


if __name__ == '__main__':
    test_binary_payload_in_request_data()
    test_encode_params_with_binary_data()
    test_encode_params_with_string_data()
    print("All tests passed!")