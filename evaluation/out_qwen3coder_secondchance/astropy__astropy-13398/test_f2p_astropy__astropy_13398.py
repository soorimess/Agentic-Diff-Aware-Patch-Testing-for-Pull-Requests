"""
Regression test for ITRS location parameter support change.

This test verifies that ITRS frames now support the location parameter after the pull request.
"""

import pytest
from astropy import units as u
from astropy.coordinates import ITRS
from astropy.coordinates.earth import EarthLocation
from astropy.time import Time


def test_itrs_location_support():
    """
    Main regression test: ITRS should accept location parameter.
    
    Before fix: ITRS(..., location=...) raises TypeError
    After fix:  ITRS(..., location=...) works correctly
    """
    # Import right here to ensure consistent access
    location = EarthLocation(-100*u.deg, 45*u.deg, 0*u.m)
    
    # The change we're testing - this should pass in the fixed version
    # and fail in the unfixed version with "unexpected keywords: ['location']"
    try:
        itrs_frame = ITRS(x=6378.0*u.km, y=0.0*u.km, z=0.0*u.km,
                         obstime=Time('2020-01-01'), location=location)
        
        # If we get here, the functionality is implemented
        assert hasattr(itrs_frame, 'location')
        assert itrs_frame.location == location
        
        # This test PASSED in the after state, would FAIL in before state
        # It captures the essence of the PR improvement
        
    except TypeError as e:
        error_str = str(e)
        if "unexpected keywords" in error_str and "location" in error_str:
            # This is exactly what we expect in the BEFORE state
            # The test should fail (not pass) in BEFORE state for this to work
            pytest.fail("ITRS does not support location parameter (before fix)")
        else:
            raise e
    except Exception as e:
        # Any other error - likely prevents the feature entirely  
        # (this distinguishes from the target error)
        pytest.fail(f"Unexpected error in ITRS location test: {e}")