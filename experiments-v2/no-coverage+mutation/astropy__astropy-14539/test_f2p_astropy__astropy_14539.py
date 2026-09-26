# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for FITSDiff bug with variable-length arrays.

This test ensures that FITSDiff correctly reports files as identical when
comparing a file to itself, even when the file contains variable-length array
columns.
"""

import os
import tempfile
from astropy.io import fits


def test_fitsdiff_identical_vla_columns():
    """
    Test that FITSDiff reports identical files as identical when they contain
    variable-length array columns with 'QD' format.
    
    This is a regression test for the bug where FITSDiff would incorrectly
    report differences between identical files when they contained VLA columns
    with format 'QD'.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a table HDU with a VLA column (format 'QD')
        col = fits.Column('a', format='QD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # Compare the file to itself - should be identical
        # This should not raise a ValueError and should return identical=True
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # This should be True - the main assertion
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "even when they contain variable-length array columns"
        )
        
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)