import os
import tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase, override_settings


class FileUploadPermissionsTest(SimpleTestCase):
    def setUp(self):
        self.storage_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: os.system(f"rm -rf {self.storage_dir}"))

    @override_settings(FILE_UPLOAD_PERMISSIONS=0o644)
    def test_file_upload_permissions_explicit_0o644(self):
        """Test that files get 0o644 permissions when explicitly set."""
        storage = FileSystemStorage(self.storage_dir)
        name = storage.save("test_file.txt", ContentFile("test data"))
        actual_mode = os.stat(storage.path(name))[0] & 0o777
        # With FILE_UPLOAD_PERMISSIONS=0o644, we should always get 0o644
        self.assertEqual(actual_mode, 0o644)

    @override_settings(FILE_UPLOAD_PERMISSIONS=None)
    def test_file_upload_permissions_none_behavior(self):
        """Test that files get permissions based on umask when FILE_UPLOAD_PERMISSIONS is None."""
        storage = FileSystemStorage(self.storage_dir)
        name = storage.save("test_file.txt", ContentFile("test data"))
        actual_mode = os.stat(storage.path(name))[0] & 0o777
        # With FILE_UPLOAD_PERMISSIONS=None, permissions should be 0o666 & ~umask
        expected_mode = 0o666 & ~os.umask(0)
        self.assertEqual(actual_mode, expected_mode)
        
    def test_default_file_upload_permissions_is_0o644(self):
        """Test that the default FILE_UPLOAD_PERMISSIONS is 0o644 (after the change)."""
        from django.conf import settings
        # This test will pass after the change and fail before the change
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)