#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue where binary payload fails due to calling to_native_string
"""

import requests
from requests.models import PreparedRequest


def test_binary_data_in_request_body():
    """Test that binary data (bytes) in request body works correctly."""
    # This is the exact case from the bug report
    # u"ööö".encode("utf-8") produces bytes that contain UTF-8 encoded data
    binary_data = u"ööö".encode("utf-8")
    
    # Create a request with binary data - this should work without raising an exception
    req = requests.Request('PUT', 'http://httpbin.org/put', data=binary_data)
    prepared = req.prepare()
    
    # The request should be prepared successfully without raising an exception
    # In the buggy version, this would raise a UnicodeDecodeError
    assert prepared.body == binary_data


if __name__ == '__main__':
    test_binary_data_in_request_body()
    print("Test passed!")