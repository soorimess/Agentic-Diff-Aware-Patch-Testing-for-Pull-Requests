import io
import os
import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_brotli_file_type(self):
        """Test that .br files get proper MIME type."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Test with FileResponse
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # Before the fix, this would be 'text/html' (wrong)
                # After the fix, this should be 'application/x-brotli' (correct)
                self.assertEqual(response.headers.get('Content-Type'), 'application/x-brotli')
        finally:
            os.unlink(tmp_path)
    
    def test_compress_file_type(self):
        """Test that .Z files get proper MIME type."""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Test with FileResponse
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # Before the fix, this would be 'text/html' (wrong)
                # After the fix, this should be 'application/x-compress' (correct)
                self.assertEqual(response.headers.get('Content-Type'), 'application/x-compress')
        finally:
            os.unlink(tmp_path)