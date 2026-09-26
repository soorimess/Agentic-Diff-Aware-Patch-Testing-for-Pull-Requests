import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.core.files.base import ContentFile


class FileUploadPermissionsTest(SimpleTestCase):
    def test_file_upload_permissions_default_is_644(self):
        """
        Test that FILE_UPLOAD_PERMISSIONS default is 0o644.
        This verifies the fix that changed the default from None to 0o644.
        """
        # Create a storage instance with default settings
        storage = FileSystemStorage()
        
        # Check that the default file permissions mode is 0o644
        self.assertEqual(storage.file_permissions_mode, 0o644)
        
        # Test that when we save a file, it gets the correct permissions
        temp_dir = tempfile.mkdtemp()
        try:
            # Create a storage instance with explicit location
            storage = FileSystemStorage(location=temp_dir)
            
            # Save a file using storage
            name = storage.save('test_file.txt', ContentFile(b"test content"))
            
            # Get the full path of the saved file
            full_path = storage.path(name)
            
            # Check the permissions - they should be 0o644 now (the new default)
            stat_result = os.stat(full_path)
            permissions = stat_result.st_mode & 0o777
            
            # With the fix, permissions should be 0o644 (the new default)
            self.assertEqual(permissions, 0o644, 
                           f"Expected permissions 0o644, got {permissions:o}")
            
        finally:
            # Clean up
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)