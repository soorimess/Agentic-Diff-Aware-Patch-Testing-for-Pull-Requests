# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for bug in FITSDiff where identical files with Q format columns 
are incorrectly reported as different.

This addresses the exact issue and fix described in the bug report:
- Problem: `io.fits.FITSDiff` may sometimes report differences between identical files
- Root cause: Improper handling of VLAs (variable-length arrays) when format contains 'Q' 
- Fix: Change condition from `elif "P" in col.format:` to `elif "P" in col.format or "Q" in col.format:`

The key behavior being tested:
1. When comparing identical files with Q format columns, no ValueError should occur
2. This ensures proper VLA comparison logic is applied instead of falling back to failed array comparison
3. Files with Q format columns are treated consistently with P format columns for VLA handling
"""

import tempfile
import numpy as np
from astropy.io import fits


def test_fitsdiff_q_format_columns_no_valueerror():
    """
    Test ensuring FITSDiff handles Q format columns without ValueError.
    
    Before fix: files with Q format columns would raise ValueError when comparing
                identical files due to improper VLA handling.
    
    After fix:  files with Q format columns properly use VLA comparison logic and
                don't raise ValueError.
    
    This is the core behavior change that addresses the bug report.
    """
    # Reproduce the exact case from bug report
    col = fits.Column('a', format='QD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + '/diffbug.fits'
        hdu.writeto(filename, overwrite=True)
        
        # This should not raise ValueError about ambiguous comparisons
        # which would happen if Q format fell through to "else" clause 
        # and tried to use np.where(arra != arrb) 
        diff = fits.FITSDiff(filename, filename)
        # Test passes if no ValueError is raised - indicating fix works


def test_fitsdiff_p_format_columns_still_work():
    """
    Regression test ensuring P format columns continue to work correctly.
    
    The fix should not break existing P format column handling.
    """
    col = fits.Column('a', format='PD', array=[[0], [0, 0]])
    hdu = fits.BinTableHDU.from_columns([col])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = tmpdir + '/diffbug_p.fits'
        hdu.writeto(filename, overwrite=True)
        
        # P format columns work correctly and shouldn't be affected
        diff = fits.FITSDiff(filename, filename)
        # Test passes if no ValueError is raised - P format already worked