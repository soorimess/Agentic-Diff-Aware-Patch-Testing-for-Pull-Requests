"""
Regression tests for ITRS to observed frame transformations.

This test ensures that the behavior change in ITRS frame handling is properly
tested, particularly the addition of location attribute to ITRS frames and
the direct ITRS to observed transformations.
"""
import numpy as np
import pytest
from astropy import units as u
from astropy.coordinates import (
    ITRS, AltAz, HADec, EarthLocation, CartesianRepresentation
)
from astropy.time import Time


def test_itrs_location_attribute():
    """Test that ITRS frames now support location attribute."""
    # Test that ITRS can be created with a location
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    itrs_frame = ITRS(obstime=Time('2020-01-01T00:00:00', scale='utc'), location=loc)
    
    # Test that the location is properly stored
    assert itrs_frame.location == loc
    
    # Test that default location is EARTH_CENTER when not specified
    itrs_default = ITRS(obstime=Time('2020-01-01T00:00:00', scale='utc'))
    from astropy.coordinates.builtin_frames.utils import EARTH_CENTER
    assert itrs_default.location == EARTH_CENTER


def test_itrs_observed_transformations_exist():
    """Test that direct ITRS to observed transformations exist."""
    # Create test locations
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    
    # Create ITRS coordinate
    itrs_coord = ITRS(CartesianRepresentation([6378000, 0, 0]*u.m), 
                      obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                      location=loc)
    
    # Test that transformation to AltAz works
    altaz_frame = AltAz(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                        location=loc)
    
    # This should work without raising an error
    result_altaz = itrs_coord.transform_to(altaz_frame)
    
    # Test that transformation to HADec works
    hadec_frame = HADec(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                        location=loc)
    
    # This should work without raising an error
    result_hadec = itrs_coord.transform_to(hadec_frame)


if __name__ == "__main__":
    # Run the tests
    test_itrs_location_attribute()
    test_itrs_observed_transformations_exist()
    print("All tests passed!")