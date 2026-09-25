import io
import os
import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_br_file_extension_mime_type(self):
        """Test that .br files get proper MIME type application/x-brotli."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix=".br", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before fix: would be text/html (default)
            # After fix: should be application/x-brotli
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_path)

    def test_z_file_extension_mime_type(self):
        """Test that .Z files get proper MIME type application/x-compress."""
        # Create a temporary .Z file
        with tempfile.NamedTemporaryFile(suffix=".Z", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before fix: would be text/html (default)
            # After fix: should be application/x-compress
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_path)