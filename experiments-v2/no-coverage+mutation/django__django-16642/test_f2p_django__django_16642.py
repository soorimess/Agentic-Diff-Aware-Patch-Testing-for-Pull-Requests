import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_br_compressed_file_response(self):
        """Test that .br files get proper content type instead of application/octet-stream."""
        with tempfile.NamedTemporaryFile(suffix=".br", delete=False) as tmp:
            response = FileResponse(tmp)
            # Before fix: this would return "application/octet-stream" 
            # After fix: this should return "application/x-brotli"
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")

    def test_compress_file_response(self):
        """Test that .Z files get proper content type instead of application/octet-stream."""
        with tempfile.NamedTemporaryFile(suffix=".Z", delete=False) as tmp:
            response = FileResponse(tmp)
            # Before fix: this would return "application/octet-stream"
            # After fix: this should return "application/x-compress"
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")