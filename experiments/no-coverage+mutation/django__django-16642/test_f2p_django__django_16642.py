"""
Regression test for Django issue: Improper guessing of Mime Type for "br" and "Z" file types

Before the fix, FileResponse would incorrectly set content type to text/html for files
with .br and .Z extensions, even though these files have proper content types.
"""
import os
import tempfile
from django.http import FileResponse
from django.test import TestCase


class FileResponseMimeTypeTest(TestCase):
    def test_file_response_br_extension(self):
        """Test that .br files get proper content type instead of text/html."""
        # Create a temporary .br file
        with tempfile.NamedTemporaryFile(suffix='.html.br', delete=False) as tmp:
            tmp_path = tmp.name
            # Write some content to the file
            tmp.write(b'<html><body>test</body></html>')
            
        try:
            # Create FileResponse - this should set proper content type
            response = FileResponse(open(tmp_path, 'rb'))
            # Verify content type is NOT text/html (the buggy behavior)
            self.assertNotEqual(response['Content-Type'], 'text/html')
            # After the fix, it should properly identify as application/x-brotli
            self.assertEqual(response['Content-Type'], 'application/x-brotli')
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_file_response_z_extension(self):
        """Test that .Z files get proper content type instead of text/html."""
        # Create a temporary .Z file  
        with tempfile.NamedTemporaryFile(suffix='.html.Z', delete=False) as tmp:
            tmp_path = tmp.name
            # Write some content to the file
            tmp.write(b'<html><body>test</body></html>')
            
        try:
            # Create FileResponse - this should set proper content type
            response = FileResponse(open(tmp_path, 'rb'))
            # Verify content type is NOT text/html (the buggy behavior) 
            self.assertNotEqual(response['Content-Type'], 'text/html')
            # After the fix, it should properly identify as application/x-compress
            self.assertEqual(response['Content-Type'], 'application/x-compress')
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)