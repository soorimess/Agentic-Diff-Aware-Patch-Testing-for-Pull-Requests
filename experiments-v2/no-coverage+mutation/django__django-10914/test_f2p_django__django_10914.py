import unittest
from django.conf import settings
from django.test import override_settings


class FileUploadPermissionsTest(unittest.TestCase):
    def test_file_upload_permissions_default_changed_to_0o644(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS default changed from None to 0o644.
        This test verifies the specific change made in the pull request.
        """
        # This test verifies the exact change: FILE_UPLOAD_PERMISSIONS = None -> FILE_UPLOAD_PERMISSIONS = 0o644
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)