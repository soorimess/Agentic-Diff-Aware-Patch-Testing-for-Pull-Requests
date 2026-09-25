"""
Regression test for Django issue #10914:
FILE_UPLOAD_PERMISSIONS default value regression test.

This test verifies that the default value for FILE_UPLOAD_PERMISSIONS has been
changed from None to 0o644 to ensure consistent file permissions across different
upload methods (temporary vs memory-based files).
"""

# A minimal test that follows Django project's patterns
def test_file_upload_permissions_default():
    """
    Validate that FILE_UPLOAD_PERMISSIONS defaults to 0o644.
    
    Before fix: FILE_UPLOAD_PERMISSIONS = None
    After fix:  FILE_UPLOAD_PERMISSIONS = 0o644
    
    This ensures consistent file permissions regardless of whether
    a file is uploaded as TemporaryUploadedFile or InMemoryUploadedFile.
    """
    # The test simply checks that this is the expected value
    # This will fail with current code (None) and pass with fixed code (0o644) 
    import django.conf.global_settings as gs
    assert gs.FILE_UPLOAD_PERMISSIONS == 0o644