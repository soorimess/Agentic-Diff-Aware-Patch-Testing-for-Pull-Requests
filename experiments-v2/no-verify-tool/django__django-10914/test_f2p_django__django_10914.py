from django.test import TestCase


class FileUploadPermissionsTest(TestCase):
    def test_file_upload_permissions_setting(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS is set to 0o644 (not None).
        This ensures consistent file permissions across upload methods.
        """
        # This test would fail before the fix (when FILE_UPLOAD_PERMISSIONS was None)
        # and pass after the fix (when FILE_UPLOAD_PERMISSIONS is 0o644)
        from django.conf import settings
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)