#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests issue where GET requests incorrectly get Content-Length header."""

import unittest
import requests
from requests.models import Request


class ContentLengthTestCase(unittest.TestCase):
    
    def test_get_request_should_not_have_content_length_header(self):
        """Test that GET requests do not automatically include Content-Length header."""
        # Create a GET request
        req = Request()
        req.method = 'GET'
        req.url = 'http://httpbin.org/get'
        
        # Prepare the request
        prepared = req.prepare()
        
        # The GET request should NOT have Content-Length header
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_head_request_should_not_have_content_length_header(self):
        """Test that HEAD requests do not automatically include Content-Length header."""
        # Create a HEAD request
        req = Request()
        req.method = 'HEAD'
        req.url = 'http://httpbin.org/head'
        
        # Prepare the request
        prepared = req.prepare()
        
        # The HEAD request should NOT have Content-Length header
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_post_request_should_have_content_length_header(self):
        """Test that POST requests still include Content-Length header."""
        # Create a POST request with data
        req = Request()
        req.method = 'POST'
        req.url = 'http://httpbin.org/post'
        req.data = 'test data'
        
        # Prepare the request
        prepared = req.prepare()
        
        # The POST request SHOULD have Content-Length header
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')


if __name__ == '__main__':
    unittest.main()