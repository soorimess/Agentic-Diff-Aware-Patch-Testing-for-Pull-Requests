import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_br_file_response_content_type(self):
        """Test that .br files get proper content type instead of text/html."""
        with tempfile.NamedTemporaryFile(suffix=".html.br", delete=False) as tmp:
            tmp.write(b"fake content")
            tmp.flush()
            response = FileResponse(tmp)
            # Before fix: would be "text/html" (fallback from mimetypes.guess_type)
            # After fix: should be "application/x-brotli" 
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")

    def test_z_file_response_content_type(self):
        """Test that .Z files get proper content type instead of text/html."""
        with tempfile.NamedTemporaryFile(suffix=".html.Z", delete=False) as tmp:
            tmp.write(b"fake content")
            tmp.flush()
            response = FileResponse(tmp)
            # Before fix: would be "text/html" (fallback from mimetypes.guess_type)
            # After fix: should be "application/x-compress"
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")