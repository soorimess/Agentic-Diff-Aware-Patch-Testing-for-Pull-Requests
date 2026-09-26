# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for astropy/astropy#14539

FITSDiff may sometimes report differences between identical files when 
comparing files with variable-length array columns (format 'Q').
"""
import numpy as np
import pytest
from astropy.io import fits
from astropy.io.fits.diff import FITSDiff
from astropy.io.fits.tests.conftest import FitsTestCase


class TestFitSDiffVLARegression(FitsTestCase):
    def test_fitsdiff_identical_vla_columns_q_format(self):
        """Test that FITSDiff correctly handles 'Q' format VLA columns (the bug fix)."""
        # Test with 'Q' format (the bug case)
        col_q = fits.Column('c', format='QD', array=[[0], [0, 0]])
        hdu_q = fits.BinTableHDU.from_columns([col_q])
        hdu_q.writeto(self.temp('diffbug_q.fits'), overwrite=True)
        
        # Compare the file to itself - should be identical
        diff_q = FITSDiff(self.temp('diffbug_q.fits'), self.temp('diffbug_q.fits'))
        assert diff_q.identical, "FITSDiff should handle 'Q' format VLA columns correctly"
        
    def test_fitsdiff_identical_vla_columns_p_format(self):
        """Test that FITSDiff correctly handles 'P' format VLA columns (existing functionality)."""
        # Test with 'P' format (should already work)
        col_p = fits.Column('b', format='PD', array=[[1.0], [1.0, 2.0]])
        hdu_p = fits.BinTableHDU.from_columns([col_p])
        hdu_p.writeto(self.temp('diffbug_p.fits'), overwrite=True)
        
        # Compare the file to itself - should be identical
        diff_p = FITSDiff(self.temp('diffbug_p.fits'), self.temp('diffbug_p.fits'))
        assert diff_p.identical, "FITSDiff should handle 'P' format VLA columns correctly"