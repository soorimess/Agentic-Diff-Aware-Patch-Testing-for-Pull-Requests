#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for quoted qop options in Digest Auth (issue #1766)."""

import unittest
from requests.auth import HTTPDigestAuth


class TestDigestAuthQopQuoting(unittest.TestCase):
    """Test that qop parameter in Digest Auth is properly quoted."""

    def test_qop_parameter_is_quoted(self):
        """Test that qop=auth is quoted as qop=\"auth\" in the digest header."""
        # Create a digest auth instance
        auth = HTTPDigestAuth('user', 'pass')
        
        # Mock the challenge data that would be set by handle_401
        auth.chal = {
            'realm': 'test-realm',
            'nonce': 'test-nonce',
            'qop': 'auth',  # This is what triggers the qop parameter
            'algorithm': 'MD5'
        }
        
        # Build the digest header
        header = auth.build_digest_header('GET', 'http://example.com/test')
        
        # The qop parameter should be quoted according to RFC2617
        # Before fix: ', qop=auth, nc=' 
        # After fix:  ', qop="auth", nc='
        self.assertIn(', qop="auth",', header)
        
        # Ensure it's not unquoted
        self.assertNotIn(', qop=auth,', header)


if __name__ == '__main__':
    unittest.main()