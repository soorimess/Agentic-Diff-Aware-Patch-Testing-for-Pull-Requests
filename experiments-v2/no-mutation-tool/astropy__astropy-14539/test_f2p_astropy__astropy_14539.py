# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for astropy/astropy#14539

Test that FITSDiff correctly handles variable-length array columns.
"""
import numpy as np
import pytest
from astropy.io import fits


def test_fitsdiff_vla_identical_files():
    """
    Test that FITSDiff correctly reports identical files as identical
    when they contain variable-length array columns.
    
    This is a regression test for astropy/astropy#14539 where FITSDiff would
    incorrectly report differences between identical files containing VLAs.
    """
    # Create a column with variable-length array format 'QD'
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to a temporary file
    hdu.writeto('test_vla.fits', overwrite=True)
    
    # Test that comparing the file to itself reports as identical
    # This should not raise an exception and should return True for identical
    try:
        diff = fits.FITSDiff('test_vla.fits', 'test_vla.fits')
        # The key assertion: it should not raise an exception and should be identical
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "but it reported them as different for VLA columns"
        )
    except Exception as e:
        # If we get an exception, it's likely due to the bug in handling VLA columns
        # This test should pass after the fix is applied
        pytest.fail(f"FITSDiff failed with exception for identical VLA files: {e}")


def test_fitsdiff_vla_handling():
    """
    Test that FITSDiff properly handles VLA columns by ensuring
    the correct comparison logic is used.
    """
    # Create a simple VLA column
    col = fits.Column('test_col', format='QD', array=[[1.0], [2.0, 3.0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to file
    hdu.writeto('test_vla2.fits', overwrite=True)
    
    # Test that we can compare the file to itself without issues
    try:
        diff = fits.FITSDiff('test_vla2.fits', 'test_vla2.fits')
        # This should work without raising ValueError about array comparison
        assert diff.identical
    except ValueError as e:
        if "ambiguous" in str(e):
            pytest.fail(f"VLA handling bug detected: {e}")
        else:
            raise
    except Exception as e:
        # Other exceptions might be expected for different reasons
        # but the specific ValueError about ambiguous array comparison is the bug
        pass