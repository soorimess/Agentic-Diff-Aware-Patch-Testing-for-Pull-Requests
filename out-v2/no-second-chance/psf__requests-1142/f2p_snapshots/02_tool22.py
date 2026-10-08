#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression test for requests issue #1142."""

import unittest
from requests.models import PreparedRequest


class TestContentLengthBehavior(unittest.TestCase):
    
    def test_get_request_without_body_no_content_length(self):
        """Test that GET requests without body do NOT have Content-Length header."""
        # Create a prepared request object
        req = PreparedRequest()
        req.method = 'GET'
        req.headers = {}
        req.body = None
        
        # Call prepare_content_length - this should NOT set Content-Length for GET requests
        req.prepare_content_length(None)
        
        # In the OLD buggy behavior, Content-Length would be set to '0'
        # In the NEW fixed behavior, Content-Length should NOT be present
        # This test will fail in the old version, pass in the new version
        self.assertNotIn('Content-Length', req.headers)
    
    def test_head_request_without_body_no_content_length(self):
        """Test that HEAD requests without body do NOT have Content-Length header."""
        # Create a prepared request object
        req = PreparedRequest()
        req.method = 'HEAD'
        req.headers = {}
        req.body = None
        
        # Call prepare_content_length - this should NOT set Content-Length for HEAD requests
        req.prepare_content_length(None)
        
        # In the OLD buggy behavior, Content-Length would be set to '0'  
        # In the NEW fixed behavior, Content-Length should NOT be present
        self.assertNotIn('Content-Length', req.headers)
    
    def test_post_request_without_body_has_content_length(self):
        """Test that POST requests without body HAVE Content-Length header."""
        # Create a prepared request object
        req = PreparedRequest()
        req.method = 'POST'
        req.headers = {}
        req.body = None
        
        # Call prepare_content_length - this SHOULD set Content-Length for POST requests
        req.prepare_content_length(None)
        
        # Content-Length should be set to '0' for POST requests
        self.assertIn('Content-Length', req.headers)
        self.assertEqual(req.headers['Content-Length'], '0')
    
    def test_put_request_without_body_has_content_length(self):
        """Test that PUT requests without body HAVE Content-Length header."""
        # Create a prepared request object
        req = PreparedRequest()
        req.method = 'PUT'
        req.headers = {}
        req.body = None
        
        # Call prepare_content_length - this SHOULD set Content-Length for PUT requests
        req.prepare_content_length(None)
        
        # Content-Length should be set to '0' for PUT requests
        self.assertIn('Content-Length', req.headers)
        self.assertEqual(req.headers['Content-Length'], '0')


if __name__ == '__main__':
    unittest.main()