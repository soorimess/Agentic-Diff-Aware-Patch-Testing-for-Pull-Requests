import pytest
from requests.auth import HTTPDigestAuth


def test_digest_auth_qop_parameter_quoted():
    """Test that qop parameter in Digest Auth header is quoted according to RFC2617."""
    # Create a digest auth object
    auth = HTTPDigestAuth('testuser', 'testpass')
    
    # Set up a mock challenge that includes qop parameter
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'qop': 'auth',  # This will trigger the qop handling code path
        'algorithm': 'MD5'
    }
    
    # Build the digest header - this is where the bug manifests
    header = auth.build_digest_header('GET', 'http://example.com/test')
    
    # Verify header contains the correct qop format with quotes
    # Per RFC2617, the qop value should be quoted
    assert 'qop="auth"' in header, f"Expected qop value to be quoted, got: {header}"
    
    # Verify header does NOT contain unquoted qop value (this is the bug)
    assert 'qop=auth' not in header, f"Bug: qop value is not quoted, got: {header}"