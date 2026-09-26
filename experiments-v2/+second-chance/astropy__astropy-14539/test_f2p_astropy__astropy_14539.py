"""
Regression test for astropy/astropy#14539

Tests that FITSDiff correctly identifies identical files when they contain
variable-length array (VLA) columns with format 'Q'.
"""
import os
import tempfile
from astropy.io import fits


def test_fitsdiff_vla_q_format_handling():
    """
    Test that FITSDiff properly handles VLA columns with 'Q' format.
    
    The bug was that when comparing identical files containing VLA columns
    with 'Q' format, FITSDiff would raise a ValueError instead of correctly
    identifying them as identical.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column using 'Q' format - exactly as in bug report
        col = fits.Column('a', format='QD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # This should not raise an exception and should report identical
        # The bug was that this would raise ValueError: The truth value of an array 
        # with more than one element is ambiguous
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # This should be True - files are identical
        assert diff.identical, (
            "FITSDiff should report identical files when comparing "
            "the same file with VLA column using 'Q' format"
        )
        
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def test_fitsdiff_vla_p_format_still_works():
    """
    Test that FITSDiff still works correctly with 'P' format VLA columns.
    
    This ensures that our fix doesn't break existing functionality for 'P' format.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column using 'P' format 
        col = fits.Column('a', format='PD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # This should not raise an exception and should report identical
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # This should be True - files are identical
        assert diff.identical, (
            "FITSDiff should report identical files when comparing "
            "the same file with VLA column using 'P' format"
        )
        
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)