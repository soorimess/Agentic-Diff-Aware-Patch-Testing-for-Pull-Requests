"""
Regression test for Django ticket #10914
Tests the behavioral change in FILE_UPLOAD_PERMISSIONS handling.
"""
from django.test import TestCase


class TestFileUploadPermissions(TestCase):
    def test_file_upload_permissions_default_is_0o644(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS default is now 0o644 instead of None.
        This ensures consistent file permissions for uploaded files.
        """
        from django.conf import settings
        # After fix: permissions are set to 0o644 for all uploaded files
        # Before fix: permissions were not explicitly set, causing inconsistencies
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)