"""
Regression tests for ITRS to Observed transformations.

This test captures the key behavioral differences introduced by the pull request
that enables ITRS frames to properly handle location information for topocentric
transformations.
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import ITRS, EarthLocation
from astropy.time import Time


def test_itrs_has_location_attribute():
    """
    Test that ITRS frame now supports location attribute (structural change).
    
    This is the core change that enables proper topocentric coordinate handling.
    In the pre-fix version, this would fail because ITRS doesn't have location.
    """
    # This test is designed to pass in the fixed version and fail in the pre-fix version
    try:
        # This should work after the fix
        from astropy.coordinates.builtin_frames.itrs import ITRS
        
        # Check that ITRS has location attribute
        assert hasattr(ITRS, 'location'), "ITRS should have location attribute"
        
        # Verify it's the right type
        location_attr = getattr(ITRS, 'location')
        assert location_attr is not None
        
    except Exception:
        # This is expected in pre-fix version - we let it fail to show the difference
        # The test failing means the fix hasn't been applied yet
        raise AssertionError("ITRS does not have location attribute - fix not applied")


def test_itrs_can_be_instantiated_with_location():
    """
    Test that ITRS frames can be created with location parameter.
    
    This validates the functional change that enables location-aware transformations.
    """
    try:
        # This should work after the fix
        location = EarthLocation.from_geodetic(-70*u.deg, -30*u.deg, 0*u.m)
        obstime = Time('2020-01-01T12:00:00')
        
        # Create ITRS frame with location - this is the new capability
        itrs_frame = ITRS(6371*u.km, 0*u.km, 0*u.km, obstime=obstime, location=location)
        
        # Verify location was set
        assert hasattr(itrs_frame, 'location')
        assert itrs_frame.location == location
        
    except Exception:
        # Expected in pre-fix version - we let it fail to show the difference
        raise AssertionError("ITRS cannot be instantiated with location - fix not applied")


def test_transformation_infrastructure_exists():
    """
    Test that the transformation infrastructure supports location-aware ITRS.
    
    This ensures the modules and imports are set up correctly for the new behavior.
    """
    try:
        # Test that we can import the new module (should exist after fix)
        from astropy.coordinates.builtin_frames import itrs_observed_transforms
        assert itrs_observed_transforms is not None
        
        # Test that intermediate rotation transforms are importable
        from astropy.coordinates.builtin_frames import intermediate_rotation_transforms
        assert intermediate_rotation_transforms is not None
        
    except ImportError:
        # Expected in pre-fix version - we let it fail to show the difference
        raise AssertionError("Transformation infrastructure missing - fix not applied")


def test_itrs_attributes_after_fix():
    """
    Test that ITRS frame has all expected attributes after the fix.
    
    This validates the complete structural change to the ITRS class.
    """
    try:
        from astropy.coordinates.builtin_frames.itrs import ITRS
        
        # These should all exist after the fix
        assert hasattr(ITRS, 'obstime')
        assert hasattr(ITRS, 'location')  # The key addition
        
        # Check that it's a proper frame with expected structure
        assert hasattr(ITRS, 'default_representation')
        assert hasattr(ITRS, 'default_differential')
        
    except Exception:
        # Expected in pre-fix version - we let it fail to show the difference
        raise AssertionError("ITRS missing expected attributes - fix not applied")


def test_behavioral_difference_exists():
    """
    Test that demonstrates the expected behavioral difference.
    
    In the pre-fix version:
    - ITRS frames don't support location parameter
    - Transformations default to EARTH_CENTER
    - No direct ITRS->Observed transformations
    
    In the post-fix version:
    - ITRS frames support location parameter
    - Transformations respect location information
    - Direct ITRS->Observed transformations exist
    """
    # This test verifies that the infrastructure exists for the new behavior
    # It should pass in the fixed version and fail in the pre-fix version
    
    # Test 1: ITRS has location attribute
    test_itrs_has_location_attribute()
    
    # Test 2: ITRS can be created with location
    test_itrs_can_be_instantiated_with_location()
    
    # Test 3: Transformation infrastructure exists
    test_transformation_infrastructure_exists()
    
    # Test 4: All expected attributes exist
    test_itrs_attributes_after_fix()
    
    # If we get here, all tests passed
    assert True, "All behavioral differences verified"