from django.conf import settings
from django.test import TestCase


class FileUploadPermissionTests(TestCase):
    def test_file_upload_permissions_default_is_0o644(self):
        """Test that FILE_UPLOAD_PERMISSIONS defaults to 0o644"""
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)