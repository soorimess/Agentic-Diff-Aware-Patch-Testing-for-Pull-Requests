import pytest
from requests.auth import HTTPDigestAuth


def test_digest_auth_qop_quoting():
    """Test that qop value in Digest header is quoted according to RFC2617."""
    # Create a mock challenge with qop directive
    challenge = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth',
        'algorithm': 'MD5',
        'opaque': 'test-opaque'
    }
    
    # Create auth object
    auth = HTTPDigestAuth('user', 'pass')
    
    # Mock the challenge data
    auth.chal = challenge
    
    # Build the digest header
    digest_header = auth.build_digest_header('GET', 'http://example.com/test')
    
    # The header should contain qop="auth" (quoted) not qop=auth (unquoted)
    # This specifically tests the RFC2617 compliance
    assert 'qop="auth"' in digest_header
    assert 'qop=auth' not in digest_header
    
    # Verify that the header has proper structure with all required parameters
    assert 'username="user"' in digest_header
    assert 'realm="test-realm"' in digest_header
    assert 'nonce="test-nonce"' in digest_header
    assert 'uri="/test"' in digest_header
    assert 'algorithm="MD5"' in digest_header
    assert 'opaque="test-opaque"' in digest_header
    
    # Verify qop is properly quoted as per RFC2617
    # Find the qop parameter in the header
    qop_pos = digest_header.find('qop="auth"')
    assert qop_pos != -1
    
    # Make sure it's not just qop=auth
    assert 'qop=auth' not in digest_header


def test_digest_auth_qop_with_multiple_options():
    """Test that qop value is quoted even when there are multiple qop options."""
    # Create a mock challenge with multiple qop directives
    challenge = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth,auth-int',
        'algorithm': 'MD5'
    }
    
    # Create auth object
    auth = HTTPDigestAuth('user', 'pass')
    
    # Mock the challenge data
    auth.chal = challenge
    
    # Build the digest header
    digest_header = auth.build_digest_header('GET', 'http://example.com/test')
    
    # The header should contain qop="auth" (quoted) not qop=auth (unquoted)
    # Note: The actual qop value in the header should be the first one when multiple are present
    # but the format should still be quoted
    assert 'qop="auth"' in digest_header or 'qop="auth-int"' in digest_header
    assert 'qop=auth' not in digest_header