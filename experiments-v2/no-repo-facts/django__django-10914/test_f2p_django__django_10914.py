"""
Test for FILE_UPLOAD_PERMISSIONS default value change from None to 0o644.
This regression test ensures that the default file upload permissions are set to 0o644
instead of None, which would cause inconsistent permissions on uploaded files.
"""
import os
import tempfile
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase, override_settings


class FileUploadPermissionsDefaultTest(SimpleTestCase):
    """
    Test that FILE_UPLOAD_PERMISSIONS default value is 0o644 instead of None.
    """
    
    def test_default_file_upload_permissions(self):
        """
        Test that the default FILE_UPLOAD_PERMISSIONS setting is 0o644.
        """
        # Check that the default value is now 0o644 instead of None
        self.assertEqual(settings.FILE_UPLOAD_PERMISSIONS, 0o644)
    
    def test_file_upload_permissions_with_default_setting(self):
        """
        Test that files are saved with the default permissions (0o644) when
        no explicit FILE_UPLOAD_PERMISSIONS is set.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            storage = FileSystemStorage(tmp_dir)
            name = storage.save("test_file.txt", ContentFile("test content"))
            full_path = storage.path(name)
            
            # Check that the file exists
            self.assertTrue(os.path.exists(full_path))
            
            # Get the actual file permissions
            actual_mode = os.stat(full_path)[0] & 0o777
            # With default setting, permissions should be 0o644
            self.assertEqual(actual_mode, 0o644)
    
    def test_file_upload_permissions_explicit_none(self):
        """
        Test that when FILE_UPLOAD_PERMISSIONS is explicitly set to None,
        files get permissions based on system umask (this is the old behavior).
        """
        with override_settings(FILE_UPLOAD_PERMISSIONS=None):
            with tempfile.TemporaryDirectory() as tmp_dir:
                storage = FileSystemStorage(tmp_dir)
                name = storage.save("test_file.txt", ContentFile("test content"))
                full_path = storage.path(name)
                
                # Check that the file exists
                self.assertTrue(os.path.exists(full_path))
                
                # Get the actual file permissions
                actual_mode = os.stat(full_path)[0] & 0o777
                # With None setting, permissions should be based on umask
                # This test is more about ensuring the behavior is preserved
                # for backward compatibility
                self.assertEqual(actual_mode, 0o666 & ~os.umask(0))