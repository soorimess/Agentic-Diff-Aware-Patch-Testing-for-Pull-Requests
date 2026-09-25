"""
Regression test for Django MIME type guessing for "br" and "Z" file types.
Tests that FileResponse correctly sets content types for .br and .Z files.
"""
import os
import tempfile
from django.http import FileResponse


def test_br_file_mime_type():
    """Test that .br files get correct MIME type."""
    # Create a temporary .br file 
    with tempfile.NamedTemporaryFile(suffix='.br', delete=False) as tmp_file:
        tmp_file.write(b"test content")
        tmp_file_path = tmp_file.name

    try:
        # Create FileResponse for .br file
        response = FileResponse(open(tmp_file_path, 'rb'))
        # Before fix: content-type would be 'text/html' (default)
        # After fix: content-type should be 'application/x-brotli'
        assert response['Content-Type'] == 'application/x-brotli'
    finally:
        os.unlink(tmp_file_path)


def test_z_file_mime_type():
    """Test that .Z files get correct MIME type."""
    # Create a temporary .Z file
    with tempfile.NamedTemporaryFile(suffix='.Z', delete=False) as tmp_file:
        tmp_file.write(b"test content")
        tmp_file_path = tmp_file.name

    try:
        # Create FileResponse for .Z file
        response = FileResponse(open(tmp_file_path, 'rb'))
        # Before fix: content-type would be 'text/html' (default)
        # After fix: content-type should be 'application/x-compress'
        assert response['Content-Type'] == 'application/x-compress'
    finally:
        os.unlink(tmp_file_path)