import os
import tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


def test_file_upload_permissions_default_value():
    """
    Test that the default FILE_UPLOAD_PERMISSIONS setting is now 0o644.
    This addresses the issue where default None caused system-dependent permissions.
    """
    # Create a temp directory and test filesystem storage  
    storage_dir = tempfile.mkdtemp()
    
    try:
        storage = FileSystemStorage(storage_dir)
        name = storage.save("test_file.txt", ContentFile("test data"))
        full_path = storage.path(name)
        actual_mode = os.stat(full_path)[0] & 0o777
        assert actual_mode == 0o644, f"Expected 0o644 permissions, got {oct(actual_mode)}"
    finally:
        # Cleanup
        for root, dirs, files in os.walk(storage_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(storage_dir)