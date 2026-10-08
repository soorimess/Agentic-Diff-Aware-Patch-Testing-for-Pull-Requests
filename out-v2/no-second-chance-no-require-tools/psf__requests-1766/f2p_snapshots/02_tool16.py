import pytest
from requests.auth import HTTPDigestAuth


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
    
    # Verify that other components are still present
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header
    assert 'realm="test-realm"' in auth_header
    assert 'nonce="test-nonce"' in auth_header
    assert 'algorithm="MD5"' in auth_header
    assert 'opaque="test-opaque"' in auth_header


def test_digest_auth_no_qop():
    """Test that digest auth works correctly when qop is not present."""
    # Create a digest auth instance
    auth = HTTPDigestAuth('user', 'pass')
    
    # Mock the challenge parameters without qop
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'algorithm': 'MD5'
        # No qop parameter
    }
    
    # Test the build_digest_header method directly
    method = 'GET'
    url = 'http://example.com/test'
    
    # Call build_digest_header to get the Authorization header
    auth_header = auth.build_digest_header(method, url)
    
    # Should not contain qop parameter at all
    assert 'qop=' not in auth_header