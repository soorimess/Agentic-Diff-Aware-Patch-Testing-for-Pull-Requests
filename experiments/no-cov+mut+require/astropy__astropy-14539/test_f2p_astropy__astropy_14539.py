# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Regression tests for FITSDiff bug with Q format variable-length arrays"""

import numpy as np
import pytest
from astropy.io import fits


def test_fitsdiff_q_format_identical():
    """
    Test that FITSDiff correctly reports identical files when 
    comparing identical files with Q-format variable-length array columns.
    
    This is a regression test for astropy/astropy#14539 where 
    FITSDiff would incorrectly report differences between identical files
    when one or more columns had Q-format (variable-length array) data.
    """
    
    # Create a FITS file with Q-format column (variable-length array)
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    hdu.writeto('test_q_format.fits', overwrite=True)
    
    # Compare the file to itself - this should report identical=True
    # Previously this would fail/raise exception due to the fix in the code
    diff = fits.FITSDiff('test_q_format.fits', 'test_q_format.fits')
    
    # The key assertion: identical should be True for identical files
    assert diff.identical is True, (
        "FITSDiff should report identical=True when comparing identical files "
        "with Q-format column, but reported False"
    )


def test_fitsdiff_q_format_different_files():
    """
    Test that FITSDiff correctly reports differences between 
    different files with Q-format variable-length array columns.
    """
    
    # Create two different FITS files with Q-format columns
    col1 = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu1 = fits.BinTableHDU.from_columns([col1])
    hdu1.writeto('test_q1.fits', overwrite=True)
    
    col2 = fits.Column('a', format='QD', array=[[1], [1, 1]])  # Different values
    hdu2 = fits.BinTableHDU.from_columns([col2])
    hdu2.writeto('test_q2.fits', overwrite=True)
    
    # Compare the different files - this should report identical=False
    diff = fits.FITSDiff('test_q1.fits', 'test_q2.fits')
    
    # The key assertion: identical should be False for different files
    assert diff.identical is False, (
        "FITSDiff should report identical=False when comparing different files "
        "with Q-format columns, but reported True"
    )


def test_fitsdiff_p_format_still_works():
    """
    Test that FITSDiff still correctly handles P-format columns after the fix.
    This ensures we haven't broken existing P-format functionality.
    """
    
    # Create a FITS file with P-format column 
    # (Note: P format is more complex to create directly but we can test 
    # that the normal case works as expected)
    col = fits.Column('a', format='PD', array=[[0.0], [0.0, 0.0]])
    hdu = fits.BinTableHDU.from_columns([col])
    hdu.writeto('test_p_format.fits', overwrite=True)
    
    # Compare the file to itself
    diff = fits.FITSDiff('test_p_format.fits', 'test_p_format.fits')
    
    # This should also work without error
    assert diff.identical is True


if __name__ == "__main__":
    # For debugging purposes
    test_fitsdiff_q_format_identical()
    test_fitsdiff_q_format_different_files()
    test_fitsdiff_p_format_still_works()
    print("All tests passed!")