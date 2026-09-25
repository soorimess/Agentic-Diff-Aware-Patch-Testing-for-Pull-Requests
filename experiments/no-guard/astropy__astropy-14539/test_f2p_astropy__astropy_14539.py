"""
Regression test for astropy issue #14539.

This test ensures that FITSDiff correctly handles variable-length arrays
(VLAs) when comparing identical files.
"""
import tempfile
import os
from astropy.io import fits


def test_fitsdiff_identical_file_with_q_format():
    """Test that FITSDiff correctly reports identical files with Q format columns."""
    # Create a test file with Q format column (variable-length array)
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        hdu.writeto(tmp_path, overwrite=True)
        
        # This should not raise an exception and should report identical=True
        # The previous bug would cause a ValueError due to improper handling of VLAs
        diff = fits.FITSDiff(tmp_path, tmp_path)
        assert diff.identical, "FITSDiff should report identical files when comparing file to itself with Q format"
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_fitsdiff_identical_file_with_p_format():
    """Test that FITSDiff correctly reports identical files with P format columns."""
    # Create a test file with P format column (another type of variable-length array)
    col = fits.Column('b', format='PD', array=[[1.0], [2.0, 3.0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        hdu.writeto(tmp_path, overwrite=True)
        
        # This should not raise an exception and should report identical=True  
        diff = fits.FITSDiff(tmp_path, tmp_path)
        assert diff.identical, "FITSDiff should report identical files when comparing file to itself with P format"
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_fitsdiff_different_files_q_format():
    """Test that FITSDiff correctly detects differences in Q format columns."""
    # Create first file with Q format column  
    col1 = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu1 = fits.BinTableHDU.from_columns([col1])
    
    # Create second file with different data in Q format
    col2 = fits.Column('a', format='QD', array=[[1], [0, 0]])  
    hdu2 = fits.BinTableHDU.from_columns([col2])
    
    # Write to temporary files
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp1, \
         tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp2:
        tmp1_path = tmp1.name
        tmp2_path = tmp2.name
    
    try:
        hdu1.writeto(tmp1_path, overwrite=True)
        hdu2.writeto(tmp2_path, overwrite=True)
        
        # This should return False - files are different
        diff = fits.FITSDiff(tmp1_path, tmp2_path)
        assert not diff.identical, "FITSDiff should report different Q format files as non-identical"
        
    finally:
        # Clean up
        for path in [tmp1_path, tmp2_path]:
            if os.path.exists(path):
                os.unlink(path)