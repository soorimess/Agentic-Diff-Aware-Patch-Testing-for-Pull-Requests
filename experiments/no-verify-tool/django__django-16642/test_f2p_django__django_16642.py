"""
Regression tests for the bug where FileResponse incorrectly guesses
Mime Type for "br" and "Z" file types.

These tests assert that FileResponse behavior changed to properly handle
the "br" and "compress" encodings that were missing from content type mapping.
"""
import io
import tempfile
import os
from django.test import SimpleTestCase


class FileResponseMimeTypeRegressionTests(SimpleTestCase):
    def test_file_response_br_files_get_correct_content_type(self):
        """
        Test that .br files get Content-Type 'application/x-brotli' instead of 
        falling back to inappropriate defaults like 'text/html'.
        """
        # Create a simple test that ends up with an encoding of "br"
        # This mimics what happens when mimetypes.guess_type() returns (None, 'br')
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.br', delete=False) as f:
            f.write(b"dummy compressed content")
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as file_handle:
                # Create FileResponse on this temp file
                response = FileResponse(file_handle) 
            
            # The content type should be properly set to application/x-brotli
            # if the fix is in place - this is what we're testing
            content_type = response.headers.get('Content-Type', '')
            self.assertIn('application/x-brotli', content_type)
        finally:
            os.unlink(temp_file_path)

    def test_file_response_z_files_get_correct_content_type(self):
        """
        Test that .Z files get Content-Type 'application/x-compress' instead of 
        falling back to inappropriate defaults like 'text/html'.
        """
        # Create a simple test that ends up with an encoding of "compress"
        # This mimics what happens when mimetypes.guess_type() returns (None, 'compress')
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.Z', delete=False) as f:
            f.write(b"dummy compressed content")
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as file_handle:
                # Create FileResponse on this temp file
                response = FileResponse(file_handle)
                
            # The content type should be properly set to application/x-compress
            # if the fix is in place - this is what we're testing
            content_type = response.headers.get('Content-Type', '')
            self.assertIn('application/x-compress', content_type)
        finally:
            os.unlink(temp_file_path)