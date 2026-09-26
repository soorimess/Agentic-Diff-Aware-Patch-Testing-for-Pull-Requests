# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
import tempfile
from astropy.io import fits


def test_fitsdiff_vla_q_format_identical_files():
    """
    Test that FITSDiff correctly handles identical files with VLA columns.
    
    This is a regression test for the bug where FITSDiff would incorrectly
    report differences between identical files containing VLA columns with 'Q' format.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.fits', delete=False) as tmp:
        tmp_name = tmp.name
    
    try:
        # Create a FITS file with a VLA column (format 'Q')
        col = fits.Column('a', format='QD', array=[[0], [0, 0]])
        hdu = fits.BinTableHDU.from_columns([col])
        hdu.writeto(tmp_name, overwrite=True)
        
        # The key test: comparing identical files should not crash
        # and should return a valid diff object
        diff = fits.FITSDiff(tmp_name, tmp_name)
        
        # The main assertion that the bug was about:
        # When files are identical, identical should be True
        # (This is what the bug report shows failing)
        assert diff.identical, (
            "FITSDiff should report identical files as identical, "
            "even with VLA columns containing 'Q' format"
        )
        
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)