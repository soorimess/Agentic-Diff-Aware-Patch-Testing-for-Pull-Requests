"""
Regression test for Django issue with FileResponse and compression file types.

This test ensures that FileResponse properly handles .Z and .br file extensions
by mapping them to appropriate content types instead of leaving them as text/html.
"""
import os
from django.http import FileResponse
from django.test import TestCase


class FileResponseCompressionTest(TestCase):
    def test_file_response_br_extension_sets_correct_content_type(self):
        """Test that .br files get application/x-brotli content type, not text/html."""
        # Create a file named .br to simulate a brotli-compressed file
        file_path = "/tmp/test.html.br"
        
        # Create the file
        with open(file_path, 'wb') as f:
            f.write(b'fake brotli compressed data')
        
        try:
            # This is the scenario described in the bug report:
            # FileResponse(open('test.html.br', 'rb')) should NOT produce content-type=text/html
            with open(file_path, 'rb') as f:
                response = FileResponse(f)
                # This would fail before the fix:
                # .br files would incorrectly be assigned content-type='text/html'
                # After fix, they should be content-type='application/x-brotli'  
                self.assertEqual(response.headers['Content-Type'], 'application/x-brotli')
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)
    
    def test_file_response_z_extension_sets_correct_content_type(self):
        """Test that .Z files get application/x-compress content type, not text/html."""
        # Create a file named .Z to simulate a compress-compressed file  
        file_path = "/tmp/test.html.Z"
        
        # Create the file
        with open(file_path, 'wb') as f:
            f.write(b'fake compress compressed data')
        
        try:
            # This is the scenario described in the bug report:
            # FileResponse(open('test.html.Z', 'rb')) should NOT produce content-type=text/html
            with open(file_path, 'rb') as f:
                response = FileResponse(f)
                # This would fail before the fix:
                # .Z files would incorrectly be assigned content-type='text/html' 
                # After fix, they should be content-type='application/x-compress'
                self.assertEqual(response.headers['Content-Type'], 'application/x-compress')
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)