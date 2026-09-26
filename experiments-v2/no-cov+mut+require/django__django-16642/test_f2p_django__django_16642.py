import os
import tempfile
from django.http import FileResponse
from django.test import TestCase


class FileResponseMimeTypeTests(TestCase):
    def test_br_file_type(self):
        """Test that .br files get proper content type instead of text/html"""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Create FileResponse for the .br file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                content_type = response.headers.get('Content-Type', '')
            
            # Before the fix, this would be 'text/html'
            # After the fix, this should be 'application/x-brotli'
            self.assertEqual(content_type, 'application/x-brotli')
        finally:
            os.unlink(tmp_path)
    
    def test_z_file_type(self):
        """Test that .Z files get proper content type instead of text/html"""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Create FileResponse for the .Z file
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                content_type = response.headers.get('Content-Type', '')
            
            # Before the fix, this would be 'text/html' 
            # After the fix, this should be 'application/x-compress'
            self.assertEqual(content_type, 'application/x-compress')
        finally:
            os.unlink(tmp_path)