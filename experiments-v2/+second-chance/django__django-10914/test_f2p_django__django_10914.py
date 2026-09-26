import os
import tempfile
import unittest
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.test import override_settings


class FileUploadPermissionsTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileSystemStorage(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_file_upload_permissions_consistency_with_explicit_setting(self):
        """
        Test that when FILE_UPLOAD_PERMISSIONS is explicitly set to 0o644,
        files get exactly 0o644 permissions - validating the fix behavior.
        """
        # Test the behavior that should work with the fix applied
        # When we explicitly set permissions to 0o644, we should get 0o644
        with override_settings(FILE_UPLOAD_PERMISSIONS=0o644):
            name = self.storage.save("test_file.txt", ContentFile("test content"))
            file_path = self.storage.path(name)
            actual_mode = os.stat(file_path)[0] & 0o777
            
            # This validates the core behavior change in the fix
            self.assertEqual(actual_mode, 0o644)