#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for issue where binary payload fails due to calling to_native_string
"""

import pytest


def test_binary_payload_put_request():
    """Test that PUT requests with binary data work correctly.
    
    This is a regression test for the bug where:
    requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
    failed in version 2.9 but worked in 2.8.1
    """
    # This should not raise an exception
    # The binary data contains non-ASCII characters that would cause 
    # to_native_string to fail with UnicodeDecodeError in the old code
    binary_data = u"ööö".encode("utf-8")
    
    # Test _encode_params directly since it's a static method
    from requests.models import RequestEncodingMixin
    
    # In the OLD code, this would raise UnicodeDecodeError because:
    # to_native_string(bytes) tries to decode bytes using ascii encoding
    # which fails for non-ASCII bytes like 0xc3
    
    # In the NEW code, this should work because:
    # return data (instead of return to_native_string(data)) 
    # just returns the bytes unchanged
    
    try:
        result = RequestEncodingMixin._encode_params(binary_data)
        # If we get here without exception, the fix works
        assert result == binary_data  # Should return data as-is
        assert isinstance(result, bytes)  # Should remain bytes type
    except UnicodeDecodeError:
        pytest.fail("UnicodeDecodeError raised when processing binary data in _encode_params")