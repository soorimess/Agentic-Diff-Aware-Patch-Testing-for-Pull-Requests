import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypeTests(SimpleTestCase):
    def test_br_compressed_response(self):
        """
        FileResponse should set the correct Content-Type for .br files.
        """
        with tempfile.NamedTemporaryFile(suffix=".html.br") as tmp:
            response = FileResponse(tmp)
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")

    def test_compress_compressed_response(self):
        """
        FileResponse should set the correct Content-Type for .Z files.
        """
        with tempfile.NamedTemporaryFile(suffix=".html.Z") as tmp:
            response = FileResponse(tmp)
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")