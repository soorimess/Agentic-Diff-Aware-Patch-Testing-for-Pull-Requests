#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for qop options quoting in Digest Auth."""

import unittest
from requests.auth import HTTPDigestAuth


class TestDigestAuthQopQuoting(unittest.TestCase):
    """Test that qop options are properly quoted in Digest Authentication."""

    def test_qop_option_quoted(self):
        """Test that qop value is quoted with double quotes according to RFC2617."""
        # Create a digest auth object
        auth = HTTPDigestAuth('user', 'pass')
        
        # Mock the challenge parameters that would be set during a 401 response
        auth.chal = {
            'realm': 'test-realm',
            'nonce': 'test-nonce',
            'qop': 'auth',
            'algorithm': 'MD5'
        }
        
        # Build the digest header
        header = auth.build_digest_header('GET', 'http://example.com/test')
        
        # The qop value should be quoted according to RFC2617
        # Before the fix: 'qop=auth' (unquoted)  
        # After the fix: 'qop="auth"' (quoted)
        self.assertIn('qop="auth"', header, 
                     'qop value should be quoted with double quotes according to RFC2617')
        
        # Ensure it's not unquoted
        self.assertNotIn('qop=auth', header,
                       'qop value should not be unquoted')


if __name__ == '__main__':
    unittest.main()