"""
Regression test for ITRS to Observed frame transforms.

This tests behavior that will change when the ITRS fixes are applied.
"""

from astropy import units as u
from astropy.coordinates import ITRS
from astropy.time import Time


def test_itrs_structure_before_fix():
    """Test the characteristic structure of ITRS in pre-fix version."""
    
    # In the pre-fix state, ITRS frames should have:
    # 1. obstime attribute 
    # 2. No location attribute (that gets added by fix)
    
    obstime = Time('2020-01-01T00:00:00')
    
    # This should work - pre-fix ITRS is basic
    itrs_frame = ITRS(obstime=obstime)
    
    # Should have obstime  
    assert hasattr(itrs_frame, 'obstime')
    assert itrs_frame.obstime == obstime
    
    # Should NOT have the location attribute that gets added by fix
    assert not hasattr(itrs_frame, 'location')
    
    # Basic coordinate construction should work without location 
    coords = ITRS(0*u.m, 0*u.m, 0*u.m, obstime=obstime)
    assert coords.obstime == obstime
    assert not hasattr(coords, 'location')