import unittest
from django.conf import settings


class FileUploadPermissionsTest(unittest.TestCase):
    def test_file_upload_permissions_default_value(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS default value is 0o644.
        This ensures consistent file permissions across all upload methods.
        """
        # The fix changes FILE_UPLOAD_PERMISSIONS from None to 0o644
        # This test verifies the fix is in place
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)