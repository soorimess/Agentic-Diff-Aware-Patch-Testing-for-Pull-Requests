import io
import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class TestFileResponseCompressionDetection(SimpleTestCase):
    """
    Regression test for Django issue where .br and .Z file extensions 
    are not properly detected for compression types.
    """
    
    def test_br_file_extension_content_type(self):
        """Test that .br files get proper content type detection."""
        # Create a temporary file with .br extension
        with tempfile.NamedTemporaryFile(suffix='.br', delete=False) as tmp:
            tmp.write(b'compressed content')
            tmp_path = tmp.name
        
        try:
            # Open in binary mode 
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # Before fix: this would be text/html (wrong)
                # After fix: this should be application/x-brotli (correct)
                content_type = response.headers.get('Content-Type', '')
                # The content type should be application/x-brotli for .br files
                # This will fail before the fix and pass after the fix
                self.assertEqual(content_type, 'application/x-brotli')
        finally:
            import os
            os.unlink(tmp_path)
    
    def test_z_file_extension_content_type(self):
        """Test that .Z files get proper content type detection."""
        # Create a temporary file with .Z extension
        with tempfile.NamedTemporaryFile(suffix='.Z', delete=False) as tmp:
            tmp.write(b'compressed content')
            tmp_path = tmp.name
        
        try:
            # Open in binary mode 
            with open(tmp_path, 'rb') as f:
                response = FileResponse(f)
                # Before fix: this would be text/html (wrong)
                # After fix: this should be application/x-compress (correct)
                content_type = response.headers.get('Content-Type', '')
                # The content type should be application/x-compress for .Z files
                self.assertEqual(content_type, 'application/x-compress')
        finally:
            import os
            os.unlink(tmp_path)