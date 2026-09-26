"""
Regression test for astropy issue #14539.

Tests that FITSDiff correctly reports identical files as identical,
especially when comparing files with variable-length array columns.
"""
import os
import tempfile
from astropy.io import fits


def test_fitsdiff_identical_files_with_vla():
    """Test that FITSDiff reports identical files as identical, even with VLA columns."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column (format 'QD')
        # This should trigger the bug - when comparing identical files
        # with Q format columns, it should not report differences
        col = fits.Column('a', format='QD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # Test that comparing a file to itself reports as identical
        # This should NOT raise an exception and should return True for identical
        diff = fits.FITSDiff(tmp_name, tmp_name)
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "but it reports them as different when VLA columns are present."
        )
        
    finally:
        # Clean up
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def test_fitsdiff_different_files_still_report_differences():
    """Test that FITSDiff still correctly reports differences between different files."""
    # Create two temporary files
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp1, \
         tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp2:
        tmp1_name = tmp1.name
        tmp2_name = tmp2.name
    
    try:
        # Create first file with one value
        col1 = fits.Column('a', format='QD', array=[[1], [0, 0]])
        hdu1 = fits.BinTableHDU.from_columns([col1])
        hdu1.writeto(tmp1_name, overwrite=True)
        
        # Create second file with different value
        col2 = fits.Column('a', format='QD', array=[[2], [0, 0]])
        hdu2 = fits.BinTableHDU.from_columns([col2])
        hdu2.writeto(tmp2_name, overwrite=True)
        
        # Test that different files are correctly reported as different
        diff = fits.FITSDiff(tmp1_name, tmp2_name)
        assert not diff.identical, (
            "FITSDiff should report different files as different, "
            "but it reports them as identical when VLA columns are present."
        )
        
    finally:
        # Clean up
        for fname in [tmp1_name, tmp2_name]:
            if os.path.exists(fname):
                os.unlink(fname)


def test_fitsdiff_with_p_format_vla():
    """Test that FITSDiff also works correctly with P format VLA columns."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column (format 'PD')
        # This should also work correctly
        col = fits.Column('a', format='PD', array=[[0.0], [0.0, 0.0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # Test that comparing a file to itself reports as identical
        diff = fits.FITSDiff(tmp_name, tmp_name)
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "even when using P format VLA columns."
        )
        
    finally:
        # Clean up
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)