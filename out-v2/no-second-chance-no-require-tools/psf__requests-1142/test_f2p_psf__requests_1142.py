#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests issue #1142.

Tests that GET requests do not automatically include Content-Length header,
while other methods do include it when appropriate.
"""

import unittest
import requests
from requests.models import Request


class TestContentLengthHeader(unittest.TestCase):
    
    def test_get_request_no_content_length(self):
        """GET requests should not have Content-Length header set automatically."""
        # Create a GET request with no body data
        req = Request(method='GET', url='http://example.com')
        prepared = req.prepare()
        
        # Check that Content-Length header is not present
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_post_request_with_content_length(self):
        """POST requests with data should have Content-Length header."""
        # Create a POST request with body data
        req = Request(method='POST', url='http://example.com', data='test data')
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
        
    def test_get_request_with_body_has_content_length(self):
        """GET requests with body data should have Content-Length header."""
        # Create a GET request with body data
        req = Request(method='GET', url='http://example.com', data='test data')
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
        
    def test_head_request_no_content_length(self):
        """HEAD requests should not have Content-Length header set automatically."""
        # Create a HEAD request with no body data
        req = Request(method='HEAD', url='http://example.com')
        prepared = req.prepare()
        
        # Check that Content-Length header is not present
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_put_request_with_content_length(self):
        """PUT requests with data should have Content-Length header."""
        # Create a PUT request with body data
        req = Request(method='PUT', url='http://example.com', data='test data')
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
        
    def test_post_request_no_body_has_content_length(self):
        """POST requests without data should have Content-Length header set to '0'."""
        # Create a POST request with no body data
        req = Request(method='POST', url='http://example.com')
        prepared = req.prepare()
        
        # Check that Content-Length header is present and set to '0'
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '0')
        
    def test_put_request_no_body_has_content_length(self):
        """PUT requests without data should have Content-Length header set to '0'."""
        # Create a PUT request with no body data
        req = Request(method='PUT', url='http://example.com')
        prepared = req.prepare()
        
        # Check that Content-Length header is present and set to '0'
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '0')


if __name__ == '__main__':
    unittest.main()