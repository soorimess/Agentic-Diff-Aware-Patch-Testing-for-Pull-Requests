"""
Regression test for PSF requests issue #2931 - 
Request with binary payload fails due to calling to_native_string
"""
import requests
from requests.models import PreparedRequest

def test_binary_payload_in_data():
    """Test that binary payloads in data parameter work correctly."""
    # This is the case mentioned in the bug report
    # Binary payload from encoding a unicode string
    binary_data = u"ööö".encode("utf-8")
    
    # The failing case: this should not raise an exception
    # Before the fix, this would fail with a TypeError from to_native_string
    try:
        req = requests.Request(method='PUT', url='http://httpbin.org/put', data=binary_data)
        prepared = req.prepare()
        # Verify the data is sent correctly
        assert prepared.body == binary_data
        assert isinstance(prepared.body, bytes)
    except UnicodeDecodeError as e:
        # This was the specific error before the fix 
        raise AssertionError(f"UnicodeDecodeError still occurs: {e}")

def test_encode_params_with_bytes():
    """Test _encode_params with bytes data - the core of the bug."""
    from requests.models import PreparedRequest
    
    # Test that _encode_params handles bytes correctly (this is where the bug was)
    req = PreparedRequest()
    
    # This should work with bytes objects passed to _encode_params
    binary_data = u"ööö".encode("utf-8")
    
    # This should not raise an exception 
    result = req._encode_params(binary_data)
    
    # The result should be the same bytes object (not passed through to_native_string)
    assert result == binary_data
    assert isinstance(result, bytes)

def test_binary_payload_in_request_body():
    """Test binary payload handling in the full request flow."""
    # The most important test - the actual reported issue
    # This should work without raising UnicodeDecodeError
    try:
        response = requests.put("http://httpbin.org/put", data=u"ööö".encode("utf-8"))
        # If we reach here, it worked!
        assert response.status_code == 200 or response.status_code == 405
    except UnicodeDecodeError as e:
        raise AssertionError(f"UnicodeDecodeError still occurs in real requests: {e}")
    except Exception:
        # Other exceptions are fine, we're only interested in the UnicodeDecodeError
        pass

def test_prepare_url_bytes_params():
    """
    Directly test the prepare_url params handling that was added in the diff.
    Specifically tests the new lines that were introduced:
    if isinstance(params, (str, bytes)):
        params = to_native_string(params)  
    """
    # Create a PreparedRequest and call prepare_url directly with bytes
    # This should trigger the exact line 389 in prepare_url method 
    req = PreparedRequest()
    
    # This should call to_native_string(params) when params is bytes
    try:
        req.prepare_url('http://example.com', b'binary_params')
        # If we get here without UnicodeDecodeError, it worked
    except UnicodeDecodeError as e:
        # This error would happen if the bytes were processed incorrectly
        raise AssertionError(f"UnicodeDecodeError in prepare_url params handling: {e}")
    except Exception:
        # Other exceptions are fine - we specifically test the UnicodeDecodeError
        pass

if __name__ == "__main__":
    test_binary_payload_in_data()
    test_encode_params_with_bytes()
    test_binary_payload_in_request_body() 
    test_prepare_url_bytes_params()
    print("All tests passed!")