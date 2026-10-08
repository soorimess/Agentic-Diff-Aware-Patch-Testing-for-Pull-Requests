#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for qop options quoting in Digest Auth.

This test verifies that the qop parameter in Digest authentication headers
is properly quoted with double quotes according to RFC2617.
"""

import unittest
from requests.auth import HTTPDigestAuth
from requests.compat import urlparse


class TestDigestAuthQopQuoting(unittest.TestCase):
    
    def test_digest_auth_qop_is_quoted(self):
        """Test that qop parameter in Digest header is quoted with double quotes."""
        # Create a mock challenge that includes qop
        auth = HTTPDigestAuth('user', 'pass')
        
        # Mock the challenge data that would be received from a server
        auth.chal = {
            'realm': 'test-realm',
            'nonce': 'test-nonce',
            'qop': 'auth',  # This should be quoted in the header
            'algorithm': 'MD5'
        }
        
        # Build a digest header
        header = auth.build_digest_header('GET', 'http://example.com/test')
        
        # The header should contain qop="auth" (quoted) not qop=auth (unquoted)
        self.assertIn('qop="auth"', header)
        self.assertNotIn('qop=auth', header)


if __name__ == '__main__':
    unittest.main()