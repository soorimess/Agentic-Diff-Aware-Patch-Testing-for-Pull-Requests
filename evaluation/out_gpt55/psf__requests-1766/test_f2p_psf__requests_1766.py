# -*- coding: utf-8 -*-

from requests.auth import HTTPDigestAuth


def test_digest_auth_qop_value_is_quoted():
    auth = HTTPDigestAuth('user', 'pass')
    auth.chal = {
        'realm': 'testrealm@host.com',
        'nonce': 'abc123',
        'qop': 'auth',
    }

    header = auth.build_digest_header('GET', 'http://example.com/digest')

    assert ', qop="auth", nc=' in header
