#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for bug related to binary payload handling in requests.

This is a test for the specific issue reported where a request with a binary
payload fails due to calling to_native_string on binary data.

The bug was introduced with https://github.com/kennethreitz/requests/issues/2844
and fixed by changing _encode_params to return data directly instead of
calling to_native_string(data) when data is bytes.
"""

import requests
from requests.models import PreparedRequest


def test_binary_payload_regression():
    """Test that binary payloads work correctly without to_native_string conversion."""
    # Create a prepared request with binary data
    req = PreparedRequest()
    
    # This is the specific case mentioned in the bug report
    binary_data = u"ööö".encode("utf-8")
    
    # This call should work (before the fix it would fail with UnicodeDecodeError)
    try:
        req.prepare(method='PUT', url='http://httpbin.org/put', data=binary_data)
        # If we get here without exception, the data should be preserved
        assert req.body == binary_data
        # More precisely, we want to show that _encode_params works on binary data
    except UnicodeDecodeError as e:
        # This is the error that would happen with old buggy code
        raise AssertionError("Binary payload causes UnicodeDecodeError - the bug is present: %s" % str(e))
    except Exception as e:
        # If it fails for any other reason, still demonstrate the issue
        raise AssertionError("Unexpected error with binary payload: %s" % str(e))


def test_encode_params_with_binary_data():
    """Test _encode_params directly with binary data to confirm fix works."""
    from requests.models import RequestEncodingMixin
    
    # Create an instance of the mixin to access _encode_params
    encoder = RequestEncodingMixin()
    
    # Binary data case from the bug report
    binary_data = u"ööö".encode("utf-8")
    
    # Test the _encode_params function directly
    # This would previously fail with UnicodeDecodeError in the OLD behavior
    result = encoder._encode_params(binary_data)
    
    # In the OLD behavior (with to_native_string), this would raise an error
    # In the NEW behavior (without to_native_string), this should work and return unchanged
    assert result == binary_data, "Binary data should be returned unchanged by _encode_params"


def test_encode_params_with_string_data():
    """Test that string data continues to work normally."""
    from requests.models import RequestEncodingMixin
    
    encoder = RequestEncodingMixin()
    
    # String data should work the same way
    string_data = "test data"
    result = encoder._encode_params(string_data)
    
    # String data should be processed normally
    # This tests that we don't break existing functionality
    assert result == string_data


if __name__ == "__main__":
    test_binary_payload_regression()
    test_encode_params_with_binary_data()
    test_encode_params_with_string_data()
    print("All tests pass!")