"""
Regression tests for ITRS to observed frame transformations.

This test ensures that the behavior change in ITRS frame handling is properly
tested, particularly the addition of location attribute to ITRS frames and
the direct ITRS to observed transformations.
"""
import pytest
from astropy import units as u
from astropy.coordinates import (
    ITRS, AltAz, HADec, EarthLocation, CartesianRepresentation
)
from astropy.time import Time


def test_itrs_location_attribute_exists():
    """Test that ITRS frames now support location attribute."""
    # Test that ITRS can be created with a location - this should work after the change
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    itrs_frame = ITRS(obstime=Time('2020-01-01T00:00:00', scale='utc'), location=loc)
    assert itrs_frame.location == loc


def test_itrs_observed_transformations_work():
    """Test that direct ITRS to observed transformations exist and work."""
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
    
    # Test that transformation to HADec works
    hadec_frame = HADec(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                        location=loc)
    
    # This should work after the change
    result_hadec = itrs_coord.transform_to(hadec_frame)
    assert isinstance(result_hadec, HADec)


def test_itrs_observed_roundtrip_transformations():
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


def test_itrs_with_refraction_support():
    """Test that ITRS to observed transformations work with refraction parameters."""
    # Create test locations
    loc = EarthLocation.from_geodetic(-70*u.deg, 40*u.deg, 0*u.m)
    
    # Create ITRS coordinate
    itrs_coord = ITRS(CartesianRepresentation([6378000, 0, 0]*u.m), 
                      obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                      location=loc)
    
    # Test that transformation to AltAz with refraction works
    altaz_frame = AltAz(obstime=Time('2020-01-01T00:00:00', scale='utc'), 
                        location=loc,
                        pressure=1013.25*u.hPa,
                        temperature=10*u.deg_C,
                        relative_humidity=50*u.percent,
                        obswl=550*u.nm)
    
    # This should work after the change
    result_altaz = itrs_coord.transform_to(altaz_frame)
    assert isinstance(result_altaz, AltAz)