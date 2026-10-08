#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests issue #1142 - GET requests should not send Content-Length header"""

import unittest
import requests
from requests.models import Request


class TestContentLengthHeader(unittest.TestCase):
    
    def test_get_request_has_no_content_length_header(self):
        """Test that GET requests do not automatically include Content-Length header"""
        # Create a request object
        req = Request()
        req.method = 'GET'
        req.url = 'http://example.com'
        
        # Prepare the request (this should not set Content-Length for GET)
        prepared = req.prepare()
        
        # Check that Content-Length header is not present
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_head_request_has_no_content_length_header(self):
        """Test that HEAD requests do not automatically include Content-Length header"""
        # Create a request object
        req = Request()
        req.method = 'HEAD'
        req.url = 'http://example.com'
        
        # Prepare the request (this should not set Content-Length for HEAD)
        prepared = req.prepare()
        
        # Check that Content-Length header is not present
        self.assertNotIn('Content-Length', prepared.headers)
        
    def test_post_request_with_body_has_content_length_header(self):
        """Test that POST requests with body do include Content-Length header"""
        # Create a request object
        req = Request()
        req.method = 'POST'
        req.url = 'http://example.com'
        req.data = b'test data'
        
        # Prepare the request (this should set Content-Length for POST with body)
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
        
    def test_get_request_with_explicit_body_has_content_length_header(self):
        """Test that GET requests with explicit body still include Content-Length header"""
        # Create a request object
        req = Request()
        req.method = 'GET'
        req.url = 'http://example.com'
        req.data = b'test data'
        
        # Prepare the request (this should set Content-Length for GET with body)
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')
        
    def test_post_request_with_no_body_has_content_length_zero(self):
        """Test that POST requests with no body set Content-Length to 0"""
        # Create a request object
        req = Request()
        req.method = 'POST'
        req.url = 'http://example.com'
        # No data provided
        
        # Prepare the request (this should set Content-Length to 0 for POST)
        prepared = req.prepare()
        
        # Check that Content-Length header is present and correct
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '0')