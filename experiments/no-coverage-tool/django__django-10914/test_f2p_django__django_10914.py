from django.test import TestCase
from django.conf import settings


class TestFileUploadPermissions(TestCase):
    def test_file_upload_permissions_default_is_0o644(self):
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)