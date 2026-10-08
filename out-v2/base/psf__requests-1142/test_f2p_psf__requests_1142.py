#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests.get always sending content-length header."""

import unittest
import requests
from requests.models import PreparedRequest


class TestContentLengthHeader(unittest.TestCase):
    
    def test_get_request_has_no_content_length_header(self):
        """Test that GET requests do not automatically include Content-Length header."""
        # Create a prepared request for a GET request with no body
        req = requests.Request('GET', 'http://httpbin.org/get')
        prepared = req.prepare()
        
        # The Content-Length header should NOT be present for GET requests
        self.assertNotIn('Content-Length', prepared.headers)
    
    def test_head_request_has_no_content_length_header(self):
        """Test that HEAD requests do not automatically include Content-Length header."""
        # Create a prepared request for a HEAD request with no body
        req = requests.Request('HEAD', 'http://httpbin.org/head')
        prepared = req.prepare()
        
        # The Content-Length header should NOT be present for HEAD requests
        self.assertNotIn('Content-Length', prepared.headers)
    
    def test_post_request_has_content_length_header(self):
        """Test that POST requests still include Content-Length header when appropriate."""
        # Create a prepared request for a POST request with data
        req = requests.Request('POST', 'http://httpbin.org/post', data='test data')
        prepared = req.prepare()
        
        # The Content-Length header should be present for POST requests with data
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
    
    def test_get_request_with_body_has_content_length_header(self):
        """Test that GET requests with body data include Content-Length header."""
        # Create a prepared request for a GET request with body data
        req = requests.Request('GET', 'http://httpbin.org/get', data='test data')
        prepared = req.prepare()
        
        # The Content-Length header should be present for GET requests with body
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
    
    def test_put_request_with_no_body_has_content_length_header(self):
        """Test that PUT requests with no body DO include Content-Length header."""
        # Create a prepared request for a PUT request with no body
        req = requests.Request('PUT', 'http://httpbin.org/put')
        prepared = req.prepare()
        
        # The Content-Length header should be present for PUT requests (not GET/HEAD)
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '0')
        
    def test_get_request_header_name_is_correct_case(self):
        """Test that GET requests don't set Content-Length header with wrong case."""
        # Create a prepared request for a GET request with no body
        req = requests.Request('GET', 'http://httpbin.org/get')
        prepared = req.prepare()
        
        # Check that no header with similar name exists (like CONTENT-LENGTH)
        # This tests that we're not just missing the header but that we're not setting
        # a header with a different case name that would still be problematic
        header_names = list(prepared.headers.keys())
        self.assertNotIn('CONTENT-LENGTH', [h.upper() for h in header_names])
        self.assertNotIn('Content-Length', [h.upper() for h in header_names])


if __name__ == '__main__':
    unittest.main()