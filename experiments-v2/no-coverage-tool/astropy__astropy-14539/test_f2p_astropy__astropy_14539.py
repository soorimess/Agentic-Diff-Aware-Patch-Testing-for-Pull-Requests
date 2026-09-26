# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for issue where FITSDiff incorrectly reports differences
between identical files containing variable-length arrays.
"""
import numpy as np
import os
from astropy.io import fits


def test_fitsdiff_identical_vla_files():
    """
    Test that FITSDiff correctly reports identical files as identical,
    even when they contain variable-length arrays with 'Q' format.
    
    This is a regression test for astropy/astropy#14539.
    """
    # Create a column with variable-length array format 'QD'
    # This format contains 'Q' which should be handled specially in diff.py
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    filename = 'diffbug.fits'
    hdu.writeto(filename, overwrite=True)
    
    try:
        # Compare the file to itself - should be identical
        # This test verifies that the fix for astropy/astropy#14539 works
        # The bug was that FITSDiff would raise an error or incorrectly report differences
        # when comparing identical files containing Q format columns
        diff = fits.FITSDiff(filename, filename)
        
        # With the fix, this should not raise an exception and should report identical=True
        # The main assertion is that it doesn't crash with the ValueError
        # and that it correctly identifies identical files
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "even when they contain variable-length arrays with 'Q' format"
        )
        
    except ValueError as e:
        if "ambiguous" in str(e) and "array with more than one element" in str(e):
            # This is the specific error that the bug report describes
            # If we get this error, it means the fix hasn't been applied yet
            raise AssertionError(
                "The bug still exists: FITSDiff fails with ValueError when "
                "comparing identical files with Q format columns. "
                "The fix should handle Q format columns like P format columns."
            )
        else:
            raise
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)