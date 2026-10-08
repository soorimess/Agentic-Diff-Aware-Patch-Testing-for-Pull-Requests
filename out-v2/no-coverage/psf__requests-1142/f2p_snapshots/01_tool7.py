#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests issue 1142 - GET requests should not send Content-Length header"""

import unittest
import requests
from requests.models import Request


class TestContentLengthHeader(unittest.TestCase):
    
    def test_get_request_has_no_content_length_header(self):
        """Test that GET requests do not include Content-Length header"""
        # Create a GET request with no body data
        req = Request(method='GET', url='http://httpbin.org/get')
        prepared = req.prepare()
        
        # The Content-Length header should not be present for GET requests
        self.assertNotIn('Content-Length', prepared.headers)
    
    def test_post_request_has_content_length_header(self):
        """Test that POST requests do include Content-Length header"""
        # Create a POST request with body data
        req = Request(method='POST', url='http://httpbin.org/post', data='test data')
        prepared = req.prepare()
        
        # The Content-Length header should be present for POST requests
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')  # 'test data' is 9 characters
    
    def test_get_request_with_explicit_body_has_content_length(self):
        """Test that GET requests with explicit body data do include Content-Length header"""
        # Create a GET request with body data
        req = Request(method='GET', url='http://httpbin.org/get', data='test data')
        prepared = req.prepare()
        
        # The Content-Length header should be present for GET requests with body
        self.assertIn('Content-Length', prepared.headers)
        self.assertEqual(prepared.headers['Content-Length'], '9')  # 'test data' is 9 characters


if __name__ == '__main__':
    unittest.main()