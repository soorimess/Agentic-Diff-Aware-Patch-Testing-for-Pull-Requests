import tempfile
import os
from django.http import FileResponse
from django.test import SimpleTestCase


class TestFileResponseBrAndZTypes(SimpleTestCase):
    def test_br_file_extension_content_type(self):
        """Test that .br files get application/x-brotli content type."""
        with tempfile.NamedTemporaryFile(suffix=".br", delete=False) as tmp:
            tmp_name = tmp.name
        try:
            response = FileResponse(open(tmp_name, "rb"))
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_name)

    def test_Z_file_extension_content_type(self):
        """Test that .Z files get application/x-compress content type.""" 
        with tempfile.NamedTemporaryFile(suffix=".Z", delete=False) as tmp:
            tmp_name = tmp.name
        try:
            response = FileResponse(open(tmp_name, "rb"))
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_name)

    def test_html_br_file_extension_content_type(self):
        """Test that .html.br files get application/x-brotli content type."""
        with tempfile.NamedTemporaryFile(suffix=".html.br", delete=False) as tmp:
            tmp_name = tmp.name
        try:
            response = FileResponse(open(tmp_name, "rb"))
            self.assertEqual(response.headers["Content-Type"], "application/x-brotli")
        finally:
            os.unlink(tmp_name)

    def test_html_Z_file_extension_content_type(self):
        """Test that .html.Z files get application/x-compress content type."""
        with tempfile.NamedTemporaryFile(suffix=".html.Z", delete=False) as tmp:
            tmp_name = tmp.name
        try:
            response = FileResponse(open(tmp_name, "rb"))
            self.assertEqual(response.headers["Content-Type"], "application/x-compress")
        finally:
            os.unlink(tmp_name)