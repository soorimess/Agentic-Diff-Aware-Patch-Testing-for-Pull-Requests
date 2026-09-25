"""
Regression test for Django ticket #10914: Set default FILE_UPLOAD_PERMISSIONS to 0o644.
"""

import os
import shutil
import tempfile
from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


class FileUploadPermissionsTest(TestCase):
    
    def setUp(self):
        self.storage_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.storage_dir)
        
    def test_file_upload_permissions_default_is_0o644(self):
        """
        Verifies the new default behavior: FILE_UPLOAD_PERMISSIONS now defaults to 0o644.
        This ensures consistent file permissions across upload handlers.
        """
        # Test that files get 0o644 permissions by default 
        storage = FileSystemStorage(self.storage_dir)
        name = storage.save("test_file.txt", ContentFile("test data"))
        actual_mode = os.stat(storage.path(name))[0] & 0o777
        self.assertEqual(actual_mode, 0o644)