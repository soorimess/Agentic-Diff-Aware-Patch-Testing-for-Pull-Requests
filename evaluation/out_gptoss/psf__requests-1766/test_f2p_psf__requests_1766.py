import pytest
from requests.auth import HTTPDigestAuth

# Test to ensure Authorization header contains quoted qop value ("auth")
# This should fail before the patch (which incorrectly omitted quotes).
# After the patch, the header will correctly contains qop="auth".

def test_digest_auth_header_quoted_qop():
    auth = HTTPDigestAuth('user', 'pass')
    # Mock a challenge that includes qop
    auth.chal = {
        'realm': 'TestRealm',
        'nonce': 'abcdef',
        'qop': 'auth',
    }
    # Ensure we start with a new nonce count
    auth.last_nonce = ''  # force nonce_count to reset to 1
    header = auth.build_digest_header('GET', 'http://example.com/')
    # The qop token should be quoted per RFC, i.e. "auth"
    assert 'qop="auth"' in header
    # Quoting behaviour specifically
    assert 'qop=auth' not in header
