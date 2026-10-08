#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for qop options in Digest Auth - RFC2617 compliance"""

import unittest
from requests.auth import HTTPDigestAuth


class TestDigestAuthQopQuoting(unittest.TestCase):
    """Test that qop parameter in Digest authentication is quoted with double quotes"""

    def test_qop_parameter_quoted(self):
        """Test that qop=auth is quoted as qop=\"auth\" in the digest header"""
        # Create a digest auth object
        auth = HTTPDigestAuth('user', 'pass')
        
        # Set up a mock challenge that includes qop
        auth.chal = {
            'realm': 'test-realm',
            'nonce': 'test-nonce',
            'qop': 'auth',
            'algorithm': 'MD5'
        }
        
        # Build the digest header
        header = auth.build_digest_header('GET', 'http://example.com/test')
        
        # The qop parameter should now be quoted according to RFC2617
        # Before the fix: ', qop=auth, nc=' 
        # After the fix: ', qop="auth", nc='
        self.assertIn(', qop="auth",', header)
        self.assertNotIn(', qop=auth,', header)


if __name__ == '__main__':
    unittest.main()