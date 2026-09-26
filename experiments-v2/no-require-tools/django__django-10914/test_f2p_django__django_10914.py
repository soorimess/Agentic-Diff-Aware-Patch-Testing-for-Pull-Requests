import os
import tempfile
import unittest
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.test import override_settings


class FileUploadPermissionsTest(unittest.TestCase):
    def setUp(self):
        self.storage_dir = tempfile.mkdtemp()
        self.old_umask = os.umask(0o027)  # Set umask to match test environment

    def tearDown(self):
        os.umask(self.old_umask)
        import shutil
        shutil.rmtree(self.storage_dir)

    def test_default_file_upload_permissions_with_temp_file(self):
        """
        Test that when using a temporary file (like TemporaryUploadedFile),
        the default FILE_UPLOAD_PERMISSIONS setting results in proper permissions.
        After the fix, this should be 0o644 instead of 0o0600.
        """
        # Create a temporary file that simulates a TemporaryUploadedFile
        # This is what happens when a file is uploaded and stored temporarily
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp_file.write("test content")
        temp_file.close()
        
        # Create a file-like object that mimics TemporaryUploadedFile
        # We'll create a minimal version that has the temporary_file_path method
        class MockTemporaryUploadedFile:
            def __init__(self, temp_path):
                self.temp_path = temp_path
                
            def temporary_file_path(self):
                return self.temp_path
                
            def chunks(self):
                yield b"test content"
                
        # Create a storage instance with default settings (FILE_UPLOAD_PERMISSIONS=None)
        storage = FileSystemStorage(self.storage_dir)
        
        # Save using a mock that has temporary_file_path (like TemporaryUploadedFile)
        mock_file = MockTemporaryUploadedFile(temp_file.name)
        fname = storage.save("test_file.txt", mock_file)
        full_path = storage.path(fname)
        
        # Get the actual permissions
        mode = os.stat(full_path)[0] & 0o777
        
        # After the fix, FILE_UPLOAD_PERMISSIONS=0o644, so chmod is applied
        # This should be 0o644, not 0o0600 (which was the old behavior)
        self.assertEqual(mode, 0o644)

    def test_explicit_file_upload_permissions(self):
        """
        Test that explicit FILE_UPLOAD_PERMISSIONS setting still works.
        """
        with override_settings(FILE_UPLOAD_PERMISSIONS=0o755):
            storage = FileSystemStorage(self.storage_dir)
            # Test with ContentFile (no temporary_file_path)
            from django.core.files.base import ContentFile
            fname = storage.save("test_file.txt", ContentFile("test content"))
            full_path = storage.path(fname)
            mode = os.stat(full_path)[0] & 0o777
            self.assertEqual(mode, 0o755)