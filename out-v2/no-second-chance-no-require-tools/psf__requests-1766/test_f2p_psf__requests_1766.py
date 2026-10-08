import pytest
from requests.auth import HTTPDigestAuth


def test_digest_auth_qop_parameter_is_quoted():
    """Test that qop parameter in Digest Auth is quoted according to RFC2617.
    
    Before the fix: qop=auth (unquoted)
    After the fix:  qop="auth" (quoted)
    
    This ensures compliance with RFC2617 which requires qop-options to be
    quoted with double quotes.
    """
    # Create a digest auth instance
    auth = HTTPDigestAuth('user', 'pass')
    
    # Mock the challenge parameters that would be set during a 401 response
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth',  # This triggers the qop parameter in the header
        'algorithm': 'MD5',
        'opaque': 'test-opaque'
    }
    
    # Test the build_digest_header method directly
    method = 'GET'
    url = 'http://example.com/test'
    
    # Call build_digest_header to get the Authorization header
    auth_header = auth.build_digest_header(method, url)
    
    # Verify that qop is quoted (the fix)
    assert 'qop="auth"' in auth_header
    # Verify that unquoted version is NOT present
    assert 'qop=auth' not in auth_header
    
    # Verify other components are still present
    assert 'nc=00000001' in auth_header  # Nonce count should be present
    assert 'cnonce="' in auth_header  # cnonce should be quoted