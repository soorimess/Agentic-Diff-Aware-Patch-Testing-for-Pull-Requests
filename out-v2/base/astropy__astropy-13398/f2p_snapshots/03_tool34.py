"""
Regression tests for ITRS to observed frame transformations.
"""
import pytest
from astropy import units as u
from astropy.coordinates import (
    ITRS, AltAz, HADec, EarthLocation, CartesianRepresentation
)
from astropy.time import Time


def test_itrs_location_attribute():
    """Test that ITRS frames now support location attribute."""
    # Test that ITRS can be created with a location - this should work after the change
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    itrs_frame = ITRS(obstime=Time('2020-01-01T00:00:00', scale='utc'), location=loc)
    assert itrs_frame.location == loc


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
    
    # This should work after the change
    result_altaz = itrs_coord.transform_to(altaz_frame)
    assert isinstance(result_altaz, AltAz)


def test_itrs_observed_transform_roundtrip():
    """Test that ITRS to observed and back works correctly."""
    # Create test locations
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    
    # Create ITRS coordinate
    itrs_coord = ITRS(CartesianRepresentation([6378000, 0, 0]*u.m), 
                      obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                      location=loc)
    
    # Transform to AltAz
    altaz_frame = AltAz(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                        location=loc)
    
    altaz_result = itrs_coord.transform_to(altaz_frame)
    
    # Transform back to ITRS - this should work
    itrs_back = altaz_result.transform_to(ITRS(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                                               location=loc))
    
    # The back transformation should work
    assert isinstance(itrs_back, ITRS)
    assert itrs_back.location == loc