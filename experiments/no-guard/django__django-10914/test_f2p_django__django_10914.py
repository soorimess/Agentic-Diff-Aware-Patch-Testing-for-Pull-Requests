"""
Test for Django PR changing default FILE_UPLOAD_PERMISSIONS to 0o644.
"""

from django.test import TestCase
from django.conf import settings


class TestFileUploadPermissions(TestCase):
    def test_file_upload_permissions_default_is_0o644(self):
        """Ensure FILE_UPLOAD_PERMISSIONS defaults to 0o644."""
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)