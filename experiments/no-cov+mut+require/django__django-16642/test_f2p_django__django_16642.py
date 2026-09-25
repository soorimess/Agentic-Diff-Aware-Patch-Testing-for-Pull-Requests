import os
import tempfile
from django.http import FileResponse
from django.test import SimpleTestCase


class FileResponseCompressionTests(SimpleTestCase):
    def test_br_file_gets_correct_content_type(self):
        """Test that .br files get application/x-brotli content type"""
        with tempfile.NamedTemporaryFile(suffix=".br", delete=False) as tmp:
            tmp.write(b"some compressed data")
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before the fix, this would return "text/html"
            # After the fix, this should return "application/x-brotli"
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_path)

    def test_Z_file_gets_correct_content_type(self):
        """Test that .Z files get application/x-compress content type"""  
        with tempfile.NamedTemporaryFile(suffix=".Z", delete=False) as tmp:
            tmp.write(b"some compressed data")
            tmp_path = tmp.name
        
        try:
            response = FileResponse(open(tmp_path, "rb"))
            # Before the fix, this would return "text/html"
            # After the fix, this should return "application/x-compress"
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_path)