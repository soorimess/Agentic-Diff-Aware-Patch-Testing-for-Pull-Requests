import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseCompressionTests(SimpleTestCase):
    def test_brotli_compression_content_type(self):
        """
        Test that .br files get proper content type for brotli compression.
        Before the fix, these would incorrectly return text/html or similar.
        """
        with tempfile.NamedTemporaryFile(suffix=".html.br") as tmp:
            response = FileResponse(tmp)
            # Should return application/x-brotli for .br files
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")

    def test_compress_compression_content_type(self):
        """
        Test that .Z files get proper content type for compress compression.
        Before the fix, these would incorrectly return text/html or similar.
        """
        with tempfile.NamedTemporaryFile(suffix=".html.Z") as tmp:
            response = FileResponse(tmp)
            # Should return application/x-compress for .Z files
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")