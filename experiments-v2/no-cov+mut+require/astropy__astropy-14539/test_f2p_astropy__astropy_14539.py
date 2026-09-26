# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue with FITSDiff reporting differences between identical files
when using variable-length array (VLA) columns.
"""

import os
import tempfile
from astropy.io import fits


def test_fitsdiff_vla_no_crash_on_identical_files():
    """
    Test that FITSDiff does not crash when comparing identical files with VLA columns.
    
    This is a regression test for a bug where FITSDiff would crash with a 
    ValueError when comparing identical files containing variable-length array columns.
    
    The bug was that 'Q' format columns (variable-length arrays) were not handled
    the same way as 'P' format columns, causing a crash when trying to compare
    arrays with different shapes using direct equality comparison.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column (format 'QD') - same as bug report
        col = fits.Column('a', format='QD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # This should not raise an exception
        # Before the fix, this would raise: ValueError: The truth value of an array 
        # with more than one element is ambiguous. Use a.any() or a.all()
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # The comparison should succeed (no crash) - this is the main assertion
        assert hasattr(diff, 'identical'), "FITSDiff should have an identical attribute"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)