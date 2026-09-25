"""
Regression test for Django ticket #10914 - FILE_UPLOAD_PERMISSIONS default change.
"""

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.test import TestCase


class FileUploadPermissionsTest(TestCase):
    def test_file_upload_permissions_set_to_644(self):
        """
        Test that files are saved with 0o644 permissions when FILE_UPLOAD_PERMISSIONS=0o644.
        This is the behavior change introduced by the fix that sets the default from None to 0o644.
        """
        # Save existing setting to restore later
        old_setting = getattr(settings, 'FILE_UPLOAD_PERMISSIONS', None)
        
        try:
            # Set the new default behavior
            settings.FILE_UPLOAD_PERMISSIONS = 0o644
            
            # Create test file content
            content = b"test content for file permissions"
            
            # Setup file storage
            storage = FileSystemStorage()
            
            # Create temporary uploaded file (uses file_move_safe path in storage._save)
            temp_file = TemporaryUploadedFile(
                name='test_file.txt',
                content_type='text/plain',
                size=len(content),
                charset=None
            )
            
            # Write content to temporary file
            temp_file.file.write(content)
            temp_file.file.flush()
            temp_file.file.seek(0)
            
            # Save file - this should apply chmod with 0o644 permissions
            file_name = storage.save('test_permissions.txt', temp_file)
            full_path = storage.path(file_name)
            
            # Get and verify file permissions
            stat_info = os.stat(full_path)
            file_permissions = stat_info.st_mode & 0o777
            
            # Verify the new default behavior works correctly
            self.assertEqual(file_permissions, 0o644)
            
        finally:
            # Always restore the original setting
            settings.FILE_UPLOAD_PERMISSIONS = old_setting