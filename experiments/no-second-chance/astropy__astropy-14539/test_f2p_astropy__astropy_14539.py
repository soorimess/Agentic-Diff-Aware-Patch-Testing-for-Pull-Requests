# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for FITSDiff bug with Q format columns.

This test ensures that FITSDiff properly handles Q format columns
(variable-length arrays) when comparing identical files. Previously,
this would raise a ValueError due to incorrect handling of variable-
length arrays.
"""

import pytest
from astropy.io import fits


def test_fitsdiff_identical_q_format_columns():
    """
    Test that FITSDiff correctly handles identical files with Q format columns.
    
    This is a regression test for astropy/astropy#14539 where FITSDiff
    would raise ValueError when comparing identical files containing
    Q format columns (variable-length arrays).
    """
    # Create a column with Q format (variable-length arrays)  
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to file
    hdu.writeto('test_q_format.fits', overwrite=True)
    
    # This should not raise an exception and should report identical=True
    diff = fits.FITSDiff('test_q_format.fits', 'test_q_format.fits')
    
    # Verify the files are identical
    assert diff.identical is True


def test_fitsdiff_different_q_format_columns():
    """
    Test that FITSDiff still correctly identifies differences with Q format columns.
    """
    # Create two different files with Q format columns
    col1 = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu1 = fits.BinTableHDU.from_columns([col1])
    hdu1.writeto('test_q_format1.fits', overwrite=True)
    
    col2 = fits.Column('a', format='QD', array=[[1], [0, 0]])  # Different first value
    hdu2 = fits.BinTableHDU.from_columns([col2])
    hdu2.writeto('test_q_format2.fits', overwrite=True)
    
    # This should detect differences
    diff = fits.FITSDiff('test_q_format1.fits', 'test_q_format2.fits')
    
    # Verify the files are different
    assert diff.identical is False