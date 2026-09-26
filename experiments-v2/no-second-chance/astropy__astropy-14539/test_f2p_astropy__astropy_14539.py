"""
Regression test for FITSDiff bug with variable-length arrays (VLA).

This test ensures that FITSDiff correctly identifies identical files
when comparing a file to itself, even when the file contains
variable-length array columns (format 'Q' or 'P').
"""

import numpy as np
import os
from astropy.io import fits
from astropy.io.fits.diff import FITSDiff


def test_fitsdiff_identical_vla_files_q_format():
    """
    Test that FITSDiff reports identical files as identical when comparing
    a file to itself, even with Q format variable-length array columns.
    
    This is a regression test for a bug where FITSDiff would incorrectly
    report differences between identical files when they contained
    variable-length array columns (format 'Q').
    """
    # Create a table HDU with a variable-length array column in 'Q' format
    # This reproduces the exact scenario from the bug report
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    filename = 'diffbug.fits'
    hdu.writeto(filename, overwrite=True)
    
    try:
        # Test that comparing the file to itself reports as identical
        # This should not raise an exception
        diff = FITSDiff(filename, filename)
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "but reported them as different for Q format VLA columns"
        )
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)


def test_fitsdiff_identical_vla_files_p_format():
    """
    Test that FITSDiff reports identical files as identical when comparing
    a file to itself, even with P format variable-length array columns.
    
    This is a regression test for a bug where FITSDiff would incorrectly
    report differences between identical files when they contained
    variable-length array columns (format 'P').
    """
    # Create a table HDU with a variable-length array column in 'P' format
    col = fits.Column('b', format='PD', array=[[1.0], [2.0, 3.0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    filename = 'diffbug_p.fits'
    hdu.writeto(filename, overwrite=True)
    
    try:
        # Test that comparing the file to itself reports as identical
        # This should not raise an exception
        diff = FITSDiff(filename, filename)
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "but reported them as different for P format VLA columns"
        )
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)


def test_fitsdiff_exact_bug_report_scenario():
    """
    Test the exact scenario from the bug report to ensure it's fixed.
    
    This recreates the exact code from the bug report to make sure
    the reported issue is resolved.
    """
    # This is the exact code from the bug report
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    filename = 'diffbug.fits'
    hdu.writeto(filename, overwrite=True)
    
    try:
        # This should not raise an exception and should report identical
        diff = FITSDiff(filename, filename)
        assert diff.identical, "Files should be identical according to FITSDiff"
        
        # Also test the printdiff functionality mentioned in the bug report
        # (This is just to make sure we don't break the print functionality)
        report = diff.report()
        assert 'identical' in report.lower() or 'no differences' in report.lower()
    finally:
        if os.path.exists(filename):
            os.remove(filename)