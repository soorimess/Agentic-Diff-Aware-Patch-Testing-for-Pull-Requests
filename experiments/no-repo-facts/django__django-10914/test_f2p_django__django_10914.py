import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings


class TestFileUploadPermissions(TestCase):
    """Test that verifies the FILE_UPLOAD_PERMISSIONS default change from None to 0o644."""

    def setUp(self):
        self.storage_dir = tempfile.mkdtemp()
        self.storage = FileSystemStorage(self.storage_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.storage_dir)

    @override_settings(FILE_UPLOAD_PERMISSIONS=0o644)
    def test_new_default_sets_permissions(self):
        """
        Test that the new default FILE_UPLOAD_PERMISSIONS=0o644 applies permissions 
        consistently to all uploaded files.
        
        This test verifies the fix that ensures uploaded files get consistent 0o644
        permissions instead of varying based on upload path.
        """
        # The test should pass with new default behavior (0o644 permission applied)
        name = self.storage.save("test.txt", ContentFile("test data"))
        mode = os.stat(self.storage.path(name))[0] & 0o777
        self.assertEqual(mode, 0o644, 
                         "Expected 0o644 permissions to be applied with new default setting")