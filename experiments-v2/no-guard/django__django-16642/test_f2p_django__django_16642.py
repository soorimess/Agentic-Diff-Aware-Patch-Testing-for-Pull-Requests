import os
import tempfile
import unittest
from django.http import FileResponse


class FileResponseMimeTypeTests(unittest.TestCase):
    def test_file_response_br_extension(self):
        """Test that .br files get correct MIME type."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Create FileResponse with .br file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
            
            # The content type should be application/x-brotli, not text/html
            self.assertEqual(response['Content-Type'], 'application/x-brotli')
        finally:
            # Clean up
            os.unlink(tmp_path)
    
    def test_file_response_z_extension(self):
        """Test that .Z files get correct MIME type."""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Create FileResponse with .Z file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
            
            # The content type should be application/x-compress, not text/html
            self.assertEqual(response['Content-Type'], 'application/x-compress')
        finally:
            # Clean up
            os.unlink(tmp_path)