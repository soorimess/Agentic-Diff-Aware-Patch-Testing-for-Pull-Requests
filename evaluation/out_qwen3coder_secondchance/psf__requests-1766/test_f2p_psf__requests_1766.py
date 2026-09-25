"""
Regression test for PSF requests issue 1766:
Quote qop options in Digest Auth

This test ensures that the qop parameter in the Digest authentication header
is quoted with double quotes as required by RFC2617.
"""

import pytest
from requests.auth import HTTPDigestAuth


def test_digest_auth_qop_is_quoted():
    """Test that qop parameter in Digest header is quoted with double quotes."""
    
    # Create a digest auth instance  
    auth = HTTPDigestAuth('user', 'pass')
    
    # Set up a mock challenge that includes qop
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce', 
        'qop': 'auth',
        'algorithm': 'MD5'
    }
    
    # Mock URL for building header
    url = 'http://example.com/test'
    
    # Build the digest header
    header = auth.build_digest_header('GET', url)
    
    # The fix is to ensure qop value is quoted as per RFC2617
    # Before fix: 'qop=auth' 
    # After fix:  'qop="auth"'
    assert header is not None, "Header should not be None"
    
    # Verify qop value is quoted
    assert 'qop="auth"' in header, f"qop should be quoted: {header}"
    
    # Verify that unquoted version is not present
    assert 'qop=auth' not in header, f"qop should be quoted, found unquoted: {header}"


def test_digest_auth_no_qop_parameter():
    """Test that when qop is not present, no qop parameter is included."""
    
    # Create a digest auth instance
    auth = HTTPDigestAuth('user', 'pass')
    
    # Set up a mock challenge without qop
    auth.chal = {
        'realm': 'test-realm',
        'nonce': 'test-nonce',
        'algorithm': 'MD5'
    }
    
    # Mock URL for building header
    url = 'http://example.com/test'
    
    # Build the digest header  
    header = auth.build_digest_header('GET', url)
    
    # No qop parameter should be present at all
    assert header is not None, "Header should not be None"
    assert 'qop=' not in header


if __name__ == '__main__':
    pytest.main([__file__, '-v'])