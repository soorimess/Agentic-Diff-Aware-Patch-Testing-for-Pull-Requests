import io
import os
import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class TestFileResponseMimeTypes(SimpleTestCase):
    def test_file_response_br_extension(self):
        """Test that .br files get proper content type."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp_file:
            tmp_file.write(b'<html><body>test</body></html>')
            tmp_file_path = tmp_file.name
            
        try:
            with open(tmp_file_path, 'rb') as f:
                response = FileResponse(f)
                content_type = response.headers.get('Content-Type')
                # The fix should map 'br' -> 'application/x-brotli'
                self.assertEqual(content_type, 'application/x-brotli')
        finally:
            # Clean up
            os.unlink(tmp_file_path)
    
    def test_file_response_z_extension(self):
        """Test that .Z files get proper content type."""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp_file:
            tmp_file.write(b'<html><body>test</body></html>')
            tmp_file_path = tmp_file.name
            
        try:
            with open(tmp_file_path, 'rb') as f:
                response = FileResponse(f)
                content_type = response.headers.get('Content-Type')
                # The fix should map 'compress' -> 'application/x-compress'
                self.assertEqual(content_type, 'application/x-compress')
        finally:
            # Clean up
            os.unlink(tmp_file_path)
            
    def test_file_response_other_extensions_unchanged(self):
        """Test that other file extensions still work as before."""
        # Create a temporary .html file
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            tmp_file.write(b'<html><body>test</body></html>')
            tmp_file_path = tmp_file.name
            
        try:
            with open(tmp_file_path, 'rb') as f:
                response = FileResponse(f)
                content_type = response.headers.get('Content-Type')
                # Regular .html files should still return text/html
                self.assertEqual(content_type, 'text/html')
        finally:
            # Clean up
            os.unlink(tmp_file_path)