# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for FITSDiff issue with variable-length arrays

This test ensures that FITSDiff correctly handles identical files
containing variable-length array (VLA) columns, which previously
reported differences between identical files due to improper handling
of Q-format columns.
"""

import tempfile
import os
from astropy.io import fits
from astropy.io.fits.diff import FITSDiff


def test_fitsdiff_identical_q_format_vla_files():
    """
    Test that identical FITS files containing Q-format variable-length array columns 
    are correctly identified as identical.
    
    This is a regression test for the issue where FITSDiff would incorrectly report
    differences between identical files containing Q-format columns, caused by
    improper handling of variable-length arrays.
    
    Before the fix: Comparing identical files with Q-format columns would raise
    ValueError due to array comparison issues.
    
    After the fix: Should work correctly and report files as identical.
    """
    # Create test data with Q-format VLA column - this is the specific case 
    # that was broken before the fix was applied
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, 'test1.fits')
        file2 = os.path.join(tmpdir, 'test2.fits')
        
        # Write same data to both files
        hdu.writeto(file1, overwrite=True)
        hdu.writeto(file2, overwrite=True)
        
        # This should work correctly with the fix applied
        # Before fix: would raise ValueError because "Q" format columns fall 
        # through to else clause and trigger direct array comparison causing error
        diff = FITSDiff(file1, file2)
        assert diff.identical, "Identical files with Q-format VLA columns should be identified as identical"