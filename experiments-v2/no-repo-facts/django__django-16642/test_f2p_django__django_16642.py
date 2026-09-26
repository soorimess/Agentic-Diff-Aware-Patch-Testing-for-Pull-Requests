import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class TestFileResponseCompressionTypes(SimpleTestCase):
    def test_br_compression_type(self):
        """Test that .br files get proper content type instead of text/html."""
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp:
            response = FileResponse(tmp)
            # Should not be text/html for .br files
            self.assertNotEqual(response.headers["Content-Type"], "text/html")
            # Should have proper brotli content type
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")

    def test_compress_compression_type(self):
        """Test that .Z files get proper content type instead of text/html."""
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp:
            response = FileResponse(tmp)
            # Should not be text/html for .Z files
            self.assertNotEqual(response.headers["Content-Type"], "text/html")
            # Should have proper compress content type
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")