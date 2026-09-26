import unittest
from django.conf.global_settings import FILE_UPLOAD_PERMISSIONS


class TestFileUploadPermissions(unittest.TestCase):
    def test_file_upload_permissions_default_is_0o644(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS defaults to 0o644.
        This ensures consistent file permissions regardless of upload method.
        The bug report described inconsistency where files could have different
        permissions depending on whether TemporaryUploadedFile or other upload methods
        were used.
        """
        # The core assertion: after the fix, this should be 0o644
        # This fixes the inconsistency issue where None would lead to 
        # different permission behaviors
        self.assertEqual(FILE_UPLOAD_PERMISSIONS, 0o644)