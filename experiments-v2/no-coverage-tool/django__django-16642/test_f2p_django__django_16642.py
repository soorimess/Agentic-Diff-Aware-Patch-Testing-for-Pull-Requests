import tempfile
import os
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_brotli_file_response_mime_type(self):
        """Test that .br files get correct MIME type."""
        with tempfile.NamedTemporaryFile(suffix=".html.br", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before fix: this would be text/html (from mimetypes.guess_type)
            # After fix: this should be application/x-brotli
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_path)

    def test_compress_file_response_mime_type(self):
        """Test that .Z files get correct MIME type."""
        with tempfile.NamedTemporaryFile(suffix=".html.Z", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before fix: this would be text/html (from mimetypes.guess_type)  
            # After fix: this should be application/x-compress
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_path)