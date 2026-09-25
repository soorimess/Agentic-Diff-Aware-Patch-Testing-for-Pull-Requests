import pytest

# Regression test for psf/requests DigestAuth: ensure qop directive is quoted
# in the Digest header after the fix, and that the header structure remains intact.

from requests.auth import HTTPDigestAuth


def test_digest_qop_value_is_quoted_in_header():
    auth = HTTPDigestAuth('user', 'pass')
    # Inject a challenge that includes qop directive.
    auth.chal = {
        'realm': 'testrealm@host',
        'nonce': 'abcdef123456',
        'qop': 'auth',
    }

    header = auth.build_digest_header('GET', 'http://example.com/protected')

    assert isinstance(header, str)
    # The fix should produce a quoted qop value in the header.
    assert 'qop="auth"' in header
    # The header should maintain its standard Digest header structure starting with the username.
    assert header.startswith('Digest username="user"')
