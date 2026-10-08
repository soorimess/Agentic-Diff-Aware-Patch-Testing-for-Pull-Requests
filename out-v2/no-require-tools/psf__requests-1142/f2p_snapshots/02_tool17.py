#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests.get always sending content-length header."""

import unittest
import requests
from requests.models import Request


class TestContentLengthHeader(unittest.TestCase):
    
    def test_get_request_should_not_have_content_length(self):
        """Test that GET requests do not automatically include Content-Length header."""
        # Create a request object
        req = Request()
        req.method = 'GET'
        req.url = 'http://example.com'
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header is NOT present for GET requests
        self.assertNotIn('Content-Length', prepared.headers)
    
    def test_head_request_should_not_have_content_length(self):
        """Test that HEAD requests do not automatically include Content-Length header."""
        # Create a request object
        req = Request()
        req.method = 'HEAD'
        req.url = 'http://example.com'
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header is NOT present for HEAD requests
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_post_request_should_have_content_length(self):
        """Test that POST requests DO include Content-Length header when body is present."""
        # Create a request object
        req = Request()
        req.method = 'POST'
        req.url = 'http://example.com'
        req.data = 'test data'
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header IS present for POST requests with data
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')  # Length of 'test data'
        
    def test_get_request_with_body_should_have_content_length(self):
        """Test that GET requests with body DO include Content-Length header."""
        # Create a request object
        req = Request()
        req.method = 'GET'
        req.url = 'http://example.com'
        req.data = 'test data'
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header IS present for GET requests with body
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')  # Length of 'test data'
        
    def test_put_request_should_have_content_length(self):
        """Test that PUT requests DO include Content-Length header when body is present."""
        # Create a request object
        req = Request()
        req.method = 'PUT'
        req.url = 'http://example.com'
        req.data = 'test data'
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header IS present for PUT requests with data
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')  # Length of 'test data'
        
    def test_get_request_with_empty_body_should_not_have_content_length(self):
        """Test that GET requests with empty body do not include Content-Length header."""
        # Create a request object
        req = Request()
        req.method = 'GET'
        req.url = 'http://example.com'
        req.data = ''
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header is NOT present for GET requests with empty body
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_head_request_with_empty_body_should_not_have_content_length(self):
        """Test that HEAD requests with empty body do not include Content-Length header."""
        # Create a request object
        req = Request()
        req.method = 'HEAD'
        req.url = 'http://example.com'
        req.data = ''
        
        # Prepare the request
        prepared = req.prepare()
        
        # Check that Content-Length header is NOT present for HEAD requests with empty body
        self.assertNotIn('Content-Length', prepared.headers)


if __name__ == '__main__':
    unittest.main()