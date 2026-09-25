"""
Regression tests for Django issue #16642.
Tests that FileResponse correctly handles .Z and .br file extensions.
"""

import os
import tempfile
from django.http import FileResponse
from django.test import TestCase


class FileResponseMimeTypeTests(TestCase):
    def test_br_file_extension(self):
        """Test that .br file extensions get appropriate content type."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.br', delete=False) as tmp:
            tmp.write(b"test data")
            tmp_path = tmp.name
        
        try:
            # Create FileResponse for the .br file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # The .br file should get application/x-brotli content type, not text/html
                self.assertNotEqual(response['Content-Type'], 'text/html')
                # Check if it's the correct content type
                self.assertIn('application/x-brotli', response['Content-Type'])
        finally:
            os.unlink(tmp_path)

    def test_z_file_extension(self):
        """Test that .Z file extensions get appropriate content type."""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix='.Z', delete=False) as tmp:
            tmp.write(b"test data")
            tmp_path = tmp.name
        
        try:
            # Create FileResponse for the .Z file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # The .Z file should get application/x-compress content type, not text/html
                self.assertNotEqual(response['Content-Type'], 'text/html')
                # Check if it's the correct content type
                self.assertIn('application/x-compress', response['Content-Type'])
        finally:
            os.unlink(tmp_path)