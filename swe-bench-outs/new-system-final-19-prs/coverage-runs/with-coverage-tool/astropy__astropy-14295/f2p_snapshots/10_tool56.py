# Copied unchanged by the harness from astropy/wcs/tests/test_utils.py::test_skycoord_to_pixel, a test in this repository before this change.
import pytest
from numpy.testing import assert_allclose
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.utils.data import get_pkg_data_contents
from astropy.wcs.utils import pixel_to_skycoord, skycoord_to_pixel
from astropy.wcs.wcs import WCS
import warnings


@pytest.mark.parametrize("mode", ["all", "wcs"])
def test_seeded_skycoord_to_pixel(mode):
    # Import astropy.coordinates here to avoid circular imports
    from astropy.coordinates import SkyCoord

    header = get_pkg_data_contents("data/maps/1904-66_TAN.hdr", encoding="binary")
    wcs = WCS(header)

    ref = SkyCoord(0.1 * u.deg, -89.0 * u.deg, frame="icrs")

    xp, yp = skycoord_to_pixel(ref, wcs, mode=mode)

    # WCS is in FK5 so we need to transform back to ICRS
    new = pixel_to_skycoord(xp, yp, wcs, mode=mode).transform_to("icrs")

    assert_allclose(new.ra.degree, ref.ra.degree)
    assert_allclose(new.dec.degree, ref.dec.degree)

    # Make sure you can specify a different class using ``cls`` keyword
    class SkyCoord2(SkyCoord):
        pass

    new2 = pixel_to_skycoord(xp, yp, wcs, mode=mode, cls=SkyCoord2).transform_to("icrs")

    assert new2.__class__ is SkyCoord2
    assert_allclose(new2.ra.degree, ref.ra.degree)
    assert_allclose(new2.dec.degree, ref.dec.degree)


def test_pv_keywords_preserved_with_sip():
    """
    Test that PV keywords are preserved when SIP distortion parameters are present
    but the PV keywords represent actual PV distortions, not SCAMP distortion parameters.
    
    This is a regression test for the issue where PV keywords were incorrectly
    removed when SIP parameters were present.
    
    The old behavior: PV keywords were removed when SIP was present, even when they
    represented actual PV distortions.
    The new behavior: PV keywords should be preserved when they represent actual PV distortions.
    """
    from astropy.io import fits
    
    # Create a header similar to the one in the issue report
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
    
    # Capture warnings to check if PV keywords are removed
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        wcs = WCS(header)
        
        # Check that PV keywords are preserved (not removed by _fix_scamp)
        # The old behavior would remove PV keywords due to SIP presence
        # The new behavior should preserve them
        
        # Check PV parameters - they should NOT be empty
        pv_params = wcs.wcs.get_pv()
        
        # Check if any warnings about removing SCAMP distortion parameters were issued
        pv_removed_warnings = [warning for warning in w 
                              if "SCAMP distortion parameters" in str(warning.message)]
        
        # The key assertion: PV keywords should be preserved when they represent
        # actual PV distortions, not SCAMP distortion parameters
        # This test should fail with the old code (PV empty, warning issued) 
        # and pass with the new code (PV preserved, no warning)
        assert len(pv_params) > 0, "PV keywords should be preserved when SIP is present"
        assert len(pv_removed_warnings) == 0, "No warning should be issued about removing SCAMP distortion parameters"
        
        # Verify the PV parameters are what we expect
        expected_pv = [(1, 0, 1.0), (1, 1, 120.0), (1, 2, 29.0)]
        # Note: PV parameters are stored as (i, j, value) tuples
        # The actual order may vary, so let's check that we have the expected values
        pv_values = [(p[0], p[1], p[2]) for p in pv_params]
        assert len(pv_values) == 3, f"Expected 3 PV parameters, got {len(pv_values)}"
        
        # Check that we have the expected PV values (order may vary)
        pv_dict = {(p[0], p[1]): p[2] for p in pv_values}
        assert (1, 0) in pv_dict and abs(pv_dict[(1, 0)] - 1.0) < 1e-10
        assert (1, 1) in pv_dict and abs(pv_dict[(1, 1)] - 120.0) < 1e-10
        assert (1, 2) in pv_dict and abs(pv_dict[(1, 2)] - 29.0) < 1e-10


def test_remove_sip_kw_function():
    """
    Test that the _remove_sip_kw function works correctly by testing SIP keyword removal.
    
    This test specifically targets the _remove_sip_kw function which removes SIP
    information from a header. This function was added in the PR and should be 
    tested to ensure SIP keywords are properly removed when needed.
    """
    from astropy.io import fits
    
    # Create a header with SIP keywords that should be removed
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
        'CTYPE1': 'RA---CAR',
        'CTYPE2': 'DEC--CAR',
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4,
        'AP_ORDER': 1,
        'AP_1_0': 0.1,
        'BP_ORDER': 1,
        'BP_1_0': 0.2
    }
    
    header = fits.Header(header_dict)
    
    # Verify SIP keywords are present initially
    assert 'A_ORDER' in header
    assert 'B_ORDER' in header
    assert 'AP_ORDER' in header
    assert 'BP_ORDER' in header
    
    # Create a WCS object which should trigger _remove_sip_kw
    # (this is a bit indirect, but we can test the function directly)
    wcs = WCS(header)
    
    # The _remove_sip_kw function is called internally during WCS initialization
    # We can test that SIP keywords are properly handled by checking the header
    # after WCS creation
    
    # Check that SIP keywords are still present (the function is called with del_order=False by default)
    # But we can test the function directly by calling it on a copy of the header
    from astropy.wcs.wcs import WCS as WCSClass
    WCSClass._remove_sip_kw(header, del_order=False)
    
    # SIP keywords should still be present since del_order=False
    assert 'A_ORDER' in header
    assert 'B_ORDER' in header
    
    # Test with del_order=True to make sure the function works with that parameter
    header_copy = fits.Header(header_dict)
    WCSClass._remove_sip_kw(header_copy, del_order=True)
    
    # SIP keywords should be removed when del_order=True
    assert 'A_ORDER' not in header_copy
    assert 'B_ORDER' not in header_copy
    assert 'AP_ORDER' not in header_copy
    assert 'BP_ORDER' not in header_copy