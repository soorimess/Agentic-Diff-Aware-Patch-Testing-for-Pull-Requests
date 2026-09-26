import tempfile
import os
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseMimeTypesTest(SimpleTestCase):
    def test_br_file_type(self):
        """Test that .br files get correct content type."""
        with tempfile.NamedTemporaryFile(suffix=".html.br", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, "rb") as f:
                response = FileResponse(f)
                # Before the fix, this would be "text/html" 
                # After the fix, this should be "application/x-brotli"
                self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_path)

    def test_z_file_type(self):
        """Test that .Z files get correct content type."""
        with tempfile.NamedTemporaryFile(suffix=".html.Z", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, "rb") as f:
                response = FileResponse(f)
                # Before the fix, this would be "text/html" 
                # After the fix, this should be "application/x-compress"
                self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_path)