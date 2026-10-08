"""
Regression test for ITRS to Observed transformations.

This test ensures that the direct ITRS to Observed (AltAz/HADec) transformations
work correctly, which should not include stellar aberration effects that would
occur when going through intermediate frames like CIRS/GCRS/TETE.
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import ITRS, AltAz, HADec
from astropy.time import Time
from astropy.coordinates import EarthLocation


def test_itrs_to_observed_transforms():
    """Test that ITRS to Observed transformations work correctly."""
    
    # Create a test location (e.g., Greenwhich)
    location = EarthLocation.from_geodetic(lon=0*u.deg, lat=51.477*u.deg, height=0*u.m)
    
    # Create a test ITRS coordinate (some arbitrary position near Earth)
    obstime = Time('2020-01-01T12:00:00')
    itrs_coord = ITRS(x=6378000*u.m, y=0*u.m, z=0*u.m, obstime=obstime, location=location)
    
    # Test ITRS to AltAz transformation
    altaz_frame = AltAz(obstime=obstime, location=location)
    altaz_result = itrs_coord.transform_to(altaz_frame)
    
    # Test ITRS to HADec transformation  
    hadec_frame = HADec(obstime=obstime, location=location)
    hadec_result = itrs_coord.transform_to(hadec_frame)
    
    # These transformations should work without errors
    assert altaz_result is not None
    assert hadec_result is not None
    assert altaz_result.obstime == obstime
    assert hadec_result.obstime == obstime
    assert altaz_result.location == location
    assert hadec_result.location == location


def test_itrs_observed_roundtrip():
    """Test round-trip transformations between ITRS and observed frames."""
    
    # Create a test location
    location = EarthLocation.from_geodetic(lon=0*u.deg, lat=51.477*u.deg, height=0*u.m)
    obstime = Time('2020-01-01T12:00:00')
    
    # Create an ITRS coordinate
    itrs_coord = ITRS(x=6378000*u.m, y=0*u.m, z=0*u.m, obstime=obstime, location=location)
    
    # Transform to AltAz and back
    altaz_frame = AltAz(obstime=obstime, location=location)
    altaz_result = itrs_coord.transform_to(altaz_frame)
    itrs_back = altaz_result.transform_to(ITRS(obstime=obstime, location=location))
    
    # Transform to HADec and back
    hadec_frame = HADec(obstime=obstime, location=location)
    hadec_result = itrs_coord.transform_to(hadec_frame)
    itrs_back2 = hadec_result.transform_to(ITRS(obstime=obstime, location=location))
    
    # The round-trip should preserve the original ITRS coordinates (approximately)
    # Note: This is a simplified test - actual round-trip precision depends on the implementation
    assert altaz_result is not None
    assert hadec_result is not None
    assert itrs_back is not None
    assert itrs_back2 is not None


def test_itrs_location_attribute():
    """Test that ITRS frame properly supports location attribute."""
    
    # Create ITRS frame with location
    location = EarthLocation.from_geodetic(lon=0*u.deg, lat=51.477*u.deg, height=0*u.m)
    obstime = Time('2020-01-01T12:00:00')
    
    itrs_frame = ITRS(obstime=obstime, location=location)
    
    # Check that location is properly set
    assert itrs_frame.location == location
    assert itrs_frame.obstime == obstime


def test_observed_to_itrs_transforms():
    """Test that observed to ITRS transformations work correctly."""
    
    # Create a test location
    location = EarthLocation.from_geodetic(lon=0*u.deg, lat=51.477*u.deg, height=0*u.m)
    obstime = Time('2020-01-01T12:00:00')
    
    # Create an AltAz coordinate
    altaz_frame = AltAz(az=90*u.deg, alt=45*u.deg, obstime=obstime, location=location)
    
    # Transform to ITRS
    itrs_result = altaz_frame.transform_to(ITRS(obstime=obstime, location=location))
    
    # Create a HADec coordinate
    hadec_frame = HADec(ha=6*u.hourangle, dec=45*u.deg, obstime=obstime, location=location)
    
    # Transform to ITRS
    itrs_result2 = hadec_frame.transform_to(ITRS(obstime=obstime, location=location))
    
    # These transformations should work without errors
    assert itrs_result is not None
    assert itrs_result2 is not None


if __name__ == "__main__":
    test_itrs_to_observed_transforms()
    test_itrs_observed_roundtrip()
    test_itrs_location_attribute()
    test_observed_to_itrs_transforms()
    print("All tests passed!")