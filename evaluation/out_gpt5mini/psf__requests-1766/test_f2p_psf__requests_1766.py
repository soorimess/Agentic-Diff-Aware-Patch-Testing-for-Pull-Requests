import re
from requests.auth import HTTPDigestAuth


def test_qop_value_is_quoted_in_digest_header():
    """The qop value in the Digest Authorization header should be quoted.

    RFC2617 requires the qop-options directive to be a quoted string. The
    client must therefore send qop="auth" (with double quotes) in the
    Authorization header when qop is used. This test would have caught
    a regression where the header was emitted as qop=auth (unquoted).
    """
    auth = HTTPDigestAuth('user', 'pass')

    # Prime the challenge as if received from a server. Include qop so the
    # build path that appends qop to the header is exercised.
    auth.chal = {
        'realm': 'testrealm@host.com',
        'nonce': 'dcd98b7102dd2f0e8b11d0f600bfb0c093',
        'qop': 'auth',
    }

    header = auth.build_digest_header('GET', 'http://example.com/dir/index.html')

    # The qop token must be quoted according to RFC2617: qop="auth"
    assert 'qop="auth"' in header, 'qop value must be double-quoted in header: %r' % header
