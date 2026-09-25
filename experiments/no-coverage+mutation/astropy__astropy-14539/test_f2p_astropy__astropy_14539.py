# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for astropy issue #14539

This test ensures that FITSDiff correctly handles variable-length array columns
with format 'Q', which was causing a ValueError when comparing identical files.
"""
import numpy as np
from astropy.io import fits
import tempfile
import os


def test_fitsdiff_q_format_no_ambiguous_error():
    """
    Test that FITSDiff handles Q format columns correctly to prevent
    'The truth value of an array with more than one element is ambiguous' error.
    
    The bug was that FITSDiff would incorrectly try to directly compare
    variable-length array data (Q format) using np.where(arra != arrb) which
    would result in a ValueError for multi-element arrays.
    
    After the fix: Q format columns are handled with the proper comparison logic
    using np.allclose instead of direct array comparison.
    """
    # Create a column with variable-length array format 'QD'
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Create temp file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        filename = tmp.name
    
    try:
        # Write to file
        hdu.writeto(filename, overwrite=True)
        
        # This used to raise ValueError: The truth value of an array with more than one 
        # element is ambiguous. Now it should work without issue.
        diff = fits.FITSDiff(filename, filename)
        
        # With the fix, identical files should be properly identified as identical  
        assert diff.identical, (
            "FITSDiff should report identical files as identical for Q format columns."
        )
        
    finally:
        # Clean up
        if os.path.exists(filename):
            os.unlink(filename)