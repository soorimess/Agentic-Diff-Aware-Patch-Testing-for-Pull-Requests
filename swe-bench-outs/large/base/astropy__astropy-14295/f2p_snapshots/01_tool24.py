# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS


def test_pv_keywords_preserved_with_sip_coefficients():
    """
    Test that PV keywords are preserved when SIP coefficients are present
    and PV keywords are legitimate SCAMP distortion parameters.
    
    This is a regression test for astropy/astropy#14295.
    
    Before the fix: PV keywords were removed whenever SIP parameters were present
    After the fix: PV keywords are only removed when they are truly redundant SCAMP distortion parameters
    """
    
    # Create a header with SIP coefficients and PV keywords as described in the issue
    # This is the exact case from the bug report that should NOT remove PV keywords
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
    
    # Create WCS object - PV keywords should be preserved (the fix)
    # The PV keywords should NOT be removed because they represent legitimate SCAMP distortions
    # that are not redundant with the SIP coefficients
    w = WCS(header)
    
    # Check that PV keywords are still present in the WCS object
    # This assertion should pass after the fix is applied
    pv = w.wcs.get_pv()
    
    # PV keywords should be preserved (not removed)
    assert len(pv) > 0, "PV keywords should be preserved when SIP coefficients are present"
    
    # Check that SIP coefficients are also present
    assert w.sip is not None, "SIP coefficients should be present"