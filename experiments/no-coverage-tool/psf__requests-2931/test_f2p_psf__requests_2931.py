#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue PSF/requests#2931
Tests that binary payloads are handled correctly in PUT requests.

Before the fix, passing bytes to data parameter would cause UnicodeDecodeError
due to to_native_string being called incorrectly on bytes objects.
"""

import pytest
import requests
from requests.models import RequestEncodingMixin


def test_binary_payload_in_put_request():
    """Test that binary payload data does not cause UnicodeDecodeError."""
    # The bug was that when binary data (bytes) is passed to a request,
    # _encode_params would call to_native_string(data) which would try 
    # to decode bytes with ASCII encoding, causing a UnicodeDecodeError
    binary_data = u"ööö".encode("utf-8")
    
    # This should not raise a UnicodeDecodeError
    # Test the core functionality that was broken
    try:
        result = RequestEncodingMixin._encode_params(binary_data)
        # With the fix, it should return the bytes as-is 
        # (not run through to_native_string which would cause decode error)
        assert result is binary_data
    except UnicodeDecodeError as e:
        # This is the exact error we were trying to fix
        raise AssertionError(f"UnicodeDecodeError still occurs - binary data not handled properly: {e}")


def test_string_payload_still_works():
    """Test that string payloads still work correctly after the fix."""
    # String data should still be processed through to_native_string as expected
    string_data = u"ööö"
    
    # This should not raise any exception
    result = RequestEncodingMixin._encode_params(string_data)
    # String data should be handled by to_native_string but not cause issues
    assert isinstance(result, (str, bytes))


def test_exact_bug_report_case():
    """Test the exact case from the bug report that was failing."""
    # This is the exact test case from bug report:
    # requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
    try:
        binary_data = u"ööö".encode("utf-8")
        # After fix, this should work without raising exception
        result = RequestEncodingMixin._encode_params(binary_data)
        # Should return the exact same bytes object (not processed through to_native_string)
        assert result is binary_data
    except UnicodeDecodeError as e:
        # The failure case - this was the bug that needed fixing
        pytest.fail(f"UnicodeDecodeError still occurs with binary payload: {str(e)}")


def test_binary_params_in_url_prepare():
    """Test that binary parameters in URL preparation don't cause issues."""
    # Trying to fully test the scenario from the issue
    # The issue was specifically about binary data being passed to request
    # Make sure _encode_params works with the exact same bytes object
    binary_params = u"ööö".encode("utf-8")
    
    result = RequestEncodingMixin._encode_params(binary_params)
    # Should preserve the exact same bytes object
    assert result is binary_params