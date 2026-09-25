"""
Regression test for Django #10914: FILE_UPLOAD_PERMISSIONS default should be 0o644.
"""
import os
import tempfile
import shutil
from django.test import SimpleTestCase


class FileUploadPermissionsTest(SimpleTestCase):
    def test_file_upload_permissions_default_value(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS is set to 0o644 (the fix) rather than None.
        """
        from django.conf import settings
        # This directly tests the specific change in global_settings.py
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)