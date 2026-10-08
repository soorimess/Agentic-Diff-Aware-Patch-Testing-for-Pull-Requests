#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Regression test for PSF requests issue #1766:
Quote qop options in Digest Auth according to RFC2617
"""

import unittest
from requests.auth import HTTPDigestAuth


class TestDigestAuthQopQuoting(unittest.TestCase):
    
    def test_digest_auth_qop_quoted(self):
        """Test that qop value is quoted with double quotes in Digest header"""
        # Create a digest auth object
        auth = HTTPDigestAuth('user', 'pass')
        
        # Set up a challenge that includes qop (this simulates what happens after a 401)
        auth.chal = {
            'realm': 'test-realm',
            'nonce': 'test-nonce',
            'qop': 'auth',
            'algorithm': 'MD5',
            'opaque': 'test-opaque'
        }
        
        # Build the digest header
        header = auth.build_digest_header('GET', 'http://example.com/test')
        
        # The qop value should be quoted according to RFC2617
        # After fix: ', qop="auth", nc='
        self.assertIn(', qop="auth",', header)
        
        # Ensure it's not the unquoted version
        self.assertNotIn(', qop=auth,', header)
        
        # Ensure qop parameter is present at all
        self.assertIn('qop=', header)
        
        # Ensure the header contains the full digest structure
        self.assertTrue(header.startswith('Digest '))
        self.assertIn('username="user"', header)
        self.assertIn('realm="test-realm"', header)
        self.assertIn('nonce="test-nonce"', header)
        self.assertIn('uri="/test"', header)
        self.assertIn('opaque="test-opaque"', header)
        self.assertIn('algorithm="MD5"', header)


if __name__ == '__main__':
    unittest.main()