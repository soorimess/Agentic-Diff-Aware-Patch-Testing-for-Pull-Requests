import pytest
from requests.auth import HTTPDigestAuth
from requests.compat import urlparse


def test_digest_auth_qop_quoted():
    """Test that qop parameter in Digest Auth is quoted according to RFC2617."""
    # Create a digest auth instance
    auth = HTTPDigestAuth('user', 'pass')
    
    # Mock the challenge parameters that would be set during a 401 response
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth',  # This is what triggers the qop parameter
        'algorithm': 'MD5',
        'opaque': 'test-opaque'
    }
    
    # Test the build_digest_header method directly
    # We need to simulate what happens when a request is made
    # Let's create a mock URL and method
    method = 'GET'
    url = 'http://example.com/test'
    
    # Call build_digest_header to get the Authorization header
    auth_header = auth.build_digest_header(method, url)
    
    # The fix ensures that qop is quoted as "auth" instead of auth
    # Before the fix: ', qop=auth, nc=00000001, cnonce="test-cnonce"'
    # After the fix:  ', qop="auth", nc=00000001, cnonce="test-cnonce"'
    
    # Verify that qop is quoted
    assert 'qop="auth"' in auth_header
    assert 'qop=auth' not in auth_header  # Should NOT contain unquoted version


def test_digest_auth_qop_unquoted_before_fix():
    """Test that demonstrates the old (incorrect) behavior before the fix."""
    # This test is for documentation - it would fail with the old code
    # but passes with the fixed code
    
    auth = HTTPDigestAuth('user', 'pass')
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth',
        'algorithm': 'MD5'
    }
    
    method = 'GET'
    url = 'http://example.com/test'
    
    auth_header = auth.build_digest_header(method, url)
    
    # This assertion should pass after the fix
    # The RFC requires qop to be quoted
    assert 'qop="auth"' in auth_header