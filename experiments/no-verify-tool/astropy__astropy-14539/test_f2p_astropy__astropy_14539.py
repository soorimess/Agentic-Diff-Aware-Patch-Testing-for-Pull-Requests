"""
Regression test for astropy issue with FITSDiff reporting differences in identical files.

This test ensures that identical FITS files with variable-length array columns 
are correctly identified as identical, not reported as different.

Before the fix, FITSDiff would incorrectly process VLA columns with 'Q' format
by falling through to a generic comparison that would fail.
After the fix, VLA columns with both 'P' and 'Q' formats are treated appropriately.
"""
import tempfile
import os
from astropy.io import fits


def test_fitsdiff_identical_files_no_vla_comparison_error():
    """
    Test that identical files with Q format variable-length arrays 
    don't raise ValueError during comparison.
    
    This is the core of the bug: the VLA handling was missing for 'Q' format, 
    causing the routine to fall through to incorrect code path that fails on
    VLA comparisons.
    """
    # Create a test FITS file with Q format variable-length array (the issue case)
    col = fits.Column('a', format='QD', array=[[0], [0, 0]]) 
    hdu = fits.BinTableHDU.from_columns([col])
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        hdu.writeto(tmp_name, overwrite=True)
        
        # Before the fix: This would raise ValueError: The truth value of an 
        # array with more than one element is ambiguous
        # After the fix: This should complete successfully
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # Verify the file is correctly identified as identical
        # The main test point is that an error doesn't happen, but also for consistency:
        assert diff.identical, "Identical files with VLA columns should be reported as identical"
        
    finally:
        # Clean up
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def test_vla_format_handling_logic():
    """
    Test logic that distinguishes between P and Q format VLA handling.
    
    The bug fix added 'Q' in addition to 'P' to trigger special comparison logic
    for both types of variable-length arrays.
    """
    col_p = fits.Column('a', format='PD', array=[[0], [0, 0]])  # P format  
    col_q = fits.Column('a', format='QD', array=[[0], [0, 0]])  # Q format
    
    # Verify we can at least create the columns
    assert col_p.format == 'PD'
    assert col_q.format == 'QD'
    
    # Both should be detected properly for their respective handling paths
    # The real test is in whether they complete without error on comparison
    hdu_p = fits.BinTableHDU.from_columns([col_p])
    hdu_q = fits.BinTableHDU.from_columns([col_q])
    
    # P format test
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp_p:
        tmp_p_name = tmp_p.name
    
    # Q format test  
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp_q:
        tmp_q_name = tmp_q.name
    
    try:
        hdu_p.writeto(tmp_p_name, overwrite=True)
        hdu_q.writeto(tmp_q_name, overwrite=True)
        
        # Both should be able to be compared without ValueError
        diff_p = fits.FITSDiff(tmp_p_name, tmp_p_name)  # P format
        diff_q = fits.FITSDiff(tmp_q_name, tmp_q_name)  # Q format
        
        assert diff_p.identical, "P format identical files should be identical"
        assert diff_q.identical, "Q format identical files should be identical"
        
    finally:
        for fname in [tmp_p_name, tmp_q_name]:
            if os.path.exists(fname):
                os.unlink(fname)