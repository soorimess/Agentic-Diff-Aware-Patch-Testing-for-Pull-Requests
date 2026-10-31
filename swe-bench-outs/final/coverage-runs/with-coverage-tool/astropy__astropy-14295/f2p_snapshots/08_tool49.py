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


def test_fix_scamp_function_behavior():
    """
    Test that the _fix_scamp function behaves correctly by creating conditions
    that would trigger its specific logic paths.
    
    This test creates a scenario where:
    1. PV parameters are present
    2. SIP parameters are present  
    3. No radial terms are present (so it should NOT return early)
    4. PV parameters should be preserved (not removed)
    
    This tests the specific lines in _fix_scamp that were removed in the PR:
    - Lines 730-732: Check if SIP is None (early return)
    - Line 737: Loop over distinct values of `i` index
    - Lines 758-759: Check for radial terms (j in (3, 11, 23, 39))  
    - Lines 764-765: Return if radial terms found
    - Line 770: Remove PV parameters and warn (this should NOT happen in our case)
    """
    from astropy.io import fits
    
    # Create a header that would trigger _fix_scamp logic but should NOT remove PV
    # This creates conditions where:
    # - PV parameters exist (will trigger the function)
    # - SIP parameters exist (will trigger the function) 
    # - No radial terms (so it should NOT return early)
    # - PV parameters should be preserved (not removed)
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
        'CTYPE1': 'RA---TAN-SIP',  # TAN with SIP - should trigger _fix_scamp
        'CTYPE2': 'DEC--TAN-SIP',
        'PV1_1': 120.0,
        'PV1_2': 29.0,
        'PV1_0': 1.0,
        'A_ORDER': 2,
        'A_2_0': 5.0e-4,
        'B_ORDER': 2,
        'B_2_0': 5.0e-4
    }
    
    header = fits.Header(header_dict)
    
    # Capture warnings to check behavior
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        wcs = WCS(header)
        
        # Check that PV parameters are preserved (should not be removed by _fix_scamp)
        pv_params = wcs.wcs.get_pv()
        
        # Check for warnings about removing SCAMP distortion parameters
        scamp_warnings = [warning for warning in w 
                         if "SCAMP distortion parameters" in str(warning.message)]
        
        # In the old behavior, this would remove PV parameters and issue a warning
        # In the new behavior, PV parameters should be preserved
        assert len(pv_params) > 0, "PV parameters should be preserved (not removed by _fix_scamp)"
        assert len(scamp_warnings) == 0, "No SCAMP distortion warning should be issued"
        
        # Verify that the PV parameters are what we expect
        pv_values = [(p[0], p[1], p[2]) for p in pv_params]
        assert len(pv_values) == 3, f"Expected 3 PV parameters, got {len(pv_values)}"
        
        # Check that we have the expected PV values (order may vary)
        pv_dict = {(p[0], p[1]): p[2] for p in pv_values}
        assert (1, 0) in pv_dict and abs(pv_dict[(1, 0)] - 1.0) < 1e-10
        assert (1, 1) in pv_dict and abs(pv_dict[(1, 1)] - 120.0) < 1e-10
        assert (1, 2) in pv_dict and abs(pv_dict[(1, 2)] - 29.0) < 1e-10