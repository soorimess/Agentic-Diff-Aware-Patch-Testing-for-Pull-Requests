"""
Regression test for issue where PV keywords are incorrectly ignored when SIP
keywords are present in WCS headers.

This test ensures that when both SIP and PV keywords are present in a header,
the PV keywords are not automatically removed by the WCS parser, which was
the behavior before the fix.
"""

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.wcs import FITSFixedWarning


def test_pv_keywords_preserved_with_sip():
    """
    Test that PV keywords are preserved when SIP coefficients are present.
    
    This is a regression test for the issue where PV keywords (like PV1_0, PV1_1, PV1_2)
    were being removed when SIP distortion parameters were also present, even when
    they should be used for distortion correction.
    """
    # Create a header with both SIP and PV keywords as described in the issue
    header_dict = {
        'SIMPLE': True,
        'BITPIX': -32,
        'NAXIS': 2,
        'NAXIS1': 1024,
        'NAXIS2': 1024,
        'CRPIX1': 512.0,
        'CRPIX2': 512.0,
        'CDELT1': 0.01,
        'CDELT2': 0.01,
        'CRVAL1': 120.0,
        'CRVAL2': 29.0,
        'CTYPE1': 'RA---CAR-SIP',
        'CTYPE2': 'DEC--CAR-SIP',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Create WCS object - this should preserve PV keywords
    w = WCS(header)
    
    # Check that PV keywords are still present in the WCS object
    pv = w.wcs.get_pv()
    
    # After the fix, PV keywords should be preserved (not removed)
    assert len(pv) > 0, "PV keywords should be preserved when SIP is present"
    
    # Check that the PV values are what we expect
    pv_dict = {(p[0], p[1]): p[2] for p in pv}
    assert (1, 0) in pv_dict
    assert (1, 1) in pv_dict
    assert (1, 2) in pv_dict
    
    # Verify that SIP is also still available
    assert w.sip is not None, "SIP coefficients should be preserved"
    
    # Verify that the specific PV values match what we set
    assert pv_dict[(1, 0)] == 1.0
    assert pv_dict[(1, 1)] == 120.0
    assert pv_dict[(1, 2)] == 29.0


def test_pv_keywords_with_tan_ctype():
    """
    Test that PV keywords are handled properly with -TAN CTYPE (pre-2012 SCAMP format).
    """
    # Create a header with -TAN CTYPE and PV keywords
    header_dict = {
        'SIMPLE': True,
        'BITPIX': -32,
        'NAXIS': 2,
        'NAXIS1': 1024,
        'NAXIS2': 1024,
        'CRPIX1': 512.0,
        'CRPIX2': 512.0,
        'CDELT1': 0.01,
        'CDELT2': 0.01,
        'CRVAL1': 120.0,
        'CRVAL2': 29.0,
        'CTYPE1': 'RA---TAN',  # -TAN instead of -SIP
        'CTYPE2': 'DEC--TAN',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'PV1_3': 0.001,  # This is a radial term that might trigger the old logic
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Create WCS object - this should handle the -TAN case properly
    w = WCS(header)
    
    # Check that PV keywords are preserved when they should be
    pv = w.wcs.get_pv()
    
    # PV keywords should be preserved in this case
    assert len(pv) > 0, "PV keywords should be preserved with -TAN CTYPE"
    
    # Verify that SIP is also still available
    assert w.sip is not None, "SIP coefficients should be preserved"


def test_sip_preserved_when_pv_present():
    """
    Test that SIP coefficients are not removed when PV keywords are present
    and the CTYPE indicates a projection that should use PV.
    """
    # Create a header with SIP and PV keywords where PV should be used
    header_dict = {
        'SIMPLE': True,
        'BITPIX': -32,
        'NAXIS': 2,
        'NAXIS1': 1024,
        'NAXIS2': 1024,
        'CRPIX1': 512.0,
        'CRPIX2': 512.0,
        'CDELT1': 0.01,
        'CDELT2': 0.01,
        'CRVAL1': 120.0,
        'CRVAL2': 29.0,
        'CTYPE1': 'RA---CAR-SIP',
        'CTYPE2': 'DEC--CAR-SIP',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Create WCS object - SIP should not be removed when PV is present
    w = WCS(header)
    
    # Check that SIP is still available
    assert w.sip is not None, "SIP coefficients should be preserved when PV is present"
    
    # Check that PV keywords are also available
    pv = w.wcs.get_pv()
    assert len(pv) > 0, "PV keywords should be preserved"
    
    # Verify that we can actually do coordinate transformations
    # This tests that both SIP and PV are properly integrated
    try:
        # Test a simple coordinate transformation
        x, y = w.all_world2pix([120.0], [29.0], 0)
        assert len(x) == 1
        assert len(y) == 1
    except Exception:
        pytest.fail("Coordinate transformation failed with both SIP and PV present")


def test_no_unwanted_pv_removal():
    """
    Test that PV keywords are NOT removed when they should be preserved.
    This specifically tests the case that was broken in the original code.
    """
    # This is the exact case from the bug report
    header_dict = {
        'SIMPLE': True,
        'BITPIX': -32,
        'NAXIS': 2,
        'NAXIS1': 1024,
        'NAXIS2': 1024,
        'CRPIX1': 512.0,
        'CRPIX2': 512.0,
        'CDELT1': 0.01,
        'CDELT2': 0.01,
        'CRVAL1': 120.0,
        'CRVAL2': 29.0,
        'CTYPE1': 'RA---CAR-SIP',
        'CTYPE2': 'DEC--CAR-SIP',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Create WCS object - this should NOT emit a warning about removing PV keywords
    # because they should be used for the CAR projection
    w = WCS(header)
    
    # PV should be preserved
    pv = w.wcs.get_pv()
    assert len(pv) > 0, "PV keywords should be preserved in CAR projection case"