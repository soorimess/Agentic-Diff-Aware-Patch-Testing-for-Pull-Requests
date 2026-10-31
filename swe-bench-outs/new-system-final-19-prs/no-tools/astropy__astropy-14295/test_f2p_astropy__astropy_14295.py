"""
Regression test for astropy/astropy#14295

This test ensures that PV keywords are not automatically removed when SIP 
distortion parameters are present, which was causing PV keywords to be ignored.
"""

import warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.wcs import FITSFixedWarning


def test_pv_keywords_preserved_when_sip_present():
    """
    Test that PV keywords are preserved when SIP distortion parameters are present.
    
    This is a regression test for astropy/astropy#14295 where PV keywords 
    were being removed automatically when SIP coefficients were present,
    even though they should be used for distortion corrections.
    """
    # Create a header similar to the one described in the issue
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
    
    # Check that PV keywords are present in the header
    assert 'PV1_0' in header
    assert 'PV1_1' in header
    assert 'PV1_2' in header
    
    # Parse the WCS - this should NOT remove PV keywords
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        wcs = WCS(header)
        
        # Check that no warning about removing redundant SCAMP distortion parameters was issued
        scamp_warnings = [warn for warn in w if "SCAMP distortion parameters" in str(warn.message)]
        # Before the fix, this would have caught the warning about removing SCAMP distortion parameters
        # After the fix, there should be no such warning
        assert len(scamp_warnings) == 0, f"Unexpected SCAMP distortion warning: {scamp_warnings}"
        
        # Check that PV parameters are still present in the WCS object
        pv = wcs.wcs.get_pv()
        assert len(pv) > 0, "PV parameters should be preserved when SIP is present"
        
        # Verify that the PV values are correctly set
        pv_dict = {(p[0], p[1]): p[2] for p in pv}
        assert (1, 0) in pv_dict
        assert (1, 1) in pv_dict
        assert (1, 2) in pv_dict


def test_pv_keywords_with_tan_projection_preserved():
    """
    Test that PV keywords with -TAN projection are preserved when SIP is present.
    
    This tests the specific case where CTYPE ends with -TAN but PV parameters
    should still be preserved.
    """
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
        'CTYPE1': 'RA---TAN',
        'CTYPE2': 'DEC--TAN',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'PV2_1': 120.0,
        'PV2_2': 29.0,
        'PV2_0': 1.0,
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Check that PV keywords are present in the header
    assert 'PV1_0' in header
    assert 'PV1_1' in header
    assert 'PV1_2' in header
    
    # Parse the WCS - this should NOT remove PV keywords
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        wcs = WCS(header)
        
        # Check that no warning about removing redundant SCAMP distortion parameters was issued
        scamp_warnings = [warn for warn in w if "SCAMP distortion parameters" in str(warn.message)]
        assert len(scamp_warnings) == 0, f"Unexpected SCAMP distortion warning: {scamp_warnings}"
        
        # Check that PV parameters are still present in the WCS object
        pv = wcs.wcs.get_pv()
        assert len(pv) > 0, "PV parameters should be preserved when SIP is present"
        
        # Verify that the PV values are correctly set
        pv_dict = {(p[0], p[1]): p[2] for p in pv}
        assert (1, 0) in pv_dict
        assert (1, 1) in pv_dict
        assert (1, 2) in pv_dict
        assert (2, 0) in pv_dict
        assert (2, 1) in pv_dict
        assert (2, 2) in pv_dict


def test_sip_only_header():
    """
    Test that SIP-only headers work normally (no PV parameters).
    """
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
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Parse the WCS
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        wcs = WCS(header)
        
        # Check that no warning about removing redundant SCAMP distortion parameters was issued
        scamp_warnings = [warn for warn in w if "SCAMP distortion parameters" in str(warn.message)]
        assert len(scamp_warnings) == 0, f"Unexpected SCAMP distortion warning: {scamp_warnings}"
        
        # Check that no PV parameters exist
        pv = wcs.wcs.get_pv()
        assert len(pv) == 0, "No PV parameters should exist when none are specified"


if __name__ == "__main__":
    test_pv_keywords_preserved_when_sip_present()
    test_pv_keywords_with_tan_projection_preserved()
    test_sip_only_header()
    print("All tests passed!")