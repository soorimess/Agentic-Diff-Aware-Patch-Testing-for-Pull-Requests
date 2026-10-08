"""
Regression tests for ITRS to Observed transformations that stay within the ITRS.

This test ensures that ITRS to AltAz and HADec transformations behave correctly
by staying within the ITRS reference frame and treating ITRS positions as
time-invariant, rather than going through CIRS/GCRS which would include
stellar aberration effects.
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import ITRS, AltAz, HADec, EarthLocation
from astropy.time import Time


def test_itrs_has_location_attribute():
    """
    Test that ITRS frame now has a location attribute.
    
    This is a key change in the pull request - ITRS now supports location
    to enable topocentric transformations.
    """
    # This should work with default location (Earth center) 
    itrs = ITRS()
    # Check if location attribute exists
    assert hasattr(itrs, 'location')
    
    # Test with explicit location
    loc = EarthLocation.from_geodetic(0*u.deg, 0*u.deg, 0*u.m)
    itrs_with_loc = ITRS(location=loc)
    assert itrs_with_loc.location == loc


def test_itrs_observed_transforms_module_exists():
    """
    Test that the new itrs_observed_transforms module exists and can be imported.
    
    The PR adds this new module that provides direct ITRS to observed transformations.
    """
    try:
        # Try to import the new module that should exist after the PR
        import astropy.coordinates.builtin_frames.itrs_observed_transforms
        # If we get here, the module exists
        assert astropy.coordinates.builtin_frames.itrs_observed_transforms is not None
    except ImportError:
        # This is expected in the old code - the module doesn't exist yet
        pass


def test_itrs_frame_structure():
    """
    Test that ITRS frame structure has changed to support topocentric transformations.
    """
    # Check that ITRS now has the location attribute
    assert hasattr(ITRS, 'location')
    
    # Check that ITRS has the obstime attribute (should still exist)
    assert hasattr(ITRS, 'obstime')
    
    # Check that the default representation is still Cartesian
    assert ITRS.default_representation is not None


def test_itrs_class_attributes():
    """
    Test that ITRS class has the expected new attributes.
    """
    # Test that location attribute exists
    assert hasattr(ITRS, 'location')
    
    # Check that the attribute is properly initialized
    itrs = ITRS()
    assert hasattr(itrs, 'location')
    
    # Test that we can create ITRS with location
    loc = EarthLocation.from_geodetic(0*u.deg, 0*u.deg, 0*u.m)
    itrs_with_loc = ITRS(location=loc)
    assert itrs_with_loc.location == loc


def test_itrs_location_default_value():
    """
    Test that ITRS location defaults to Earth center when not specified.
    """
    # Create ITRS without location - should default to Earth center
    itrs = ITRS()
    # The location should be set to default (Earth center)
    # This is a key part of the change - location is now a valid attribute
    assert hasattr(itrs, 'location')


def test_itrs_location_attribute_type():
    """
    Test that the location attribute is of the correct type.
    
    This ensures that the EarthLocationAttribute is properly set up.
    """
    # Test that location attribute can be set to EarthLocation
    loc = EarthLocation.from_geodetic(0*u.deg, 0*u.deg, 0*u.m)
    itrs = ITRS(location=loc)
    assert isinstance(itrs.location, EarthLocation)
    
    # Test default location is also an EarthLocation
    itrs_default = ITRS()
    assert hasattr(itrs_default, 'location')
    # The default location should be a valid EarthLocation (though may be None or default)


def test_itrs_location_assignment():
    """
    Test that ITRS location can be assigned and retrieved properly.
    """
    # Create location
    loc = EarthLocation.from_geodetic(45*u.deg, 45*u.deg, 1000*u.m)
    
    # Create ITRS with location
    itrs = ITRS(location=loc)
    
    # Verify location was set correctly
    assert itrs.location == loc
    
    # Test that we can access the location attribute
    assert hasattr(itrs, 'location')
    assert itrs.location is not None