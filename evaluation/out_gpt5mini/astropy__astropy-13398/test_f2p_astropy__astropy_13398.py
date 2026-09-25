# Regression test for astropy#13398
# Ensure the ITRS frame accepts a 'location' attribute (EarthLocation).
# Before the fix, ITRS did not have a 'location' frame attribute and would
# raise on construction with that keyword.

from astropy.coordinates import ITRS, EarthLocation
from astropy.time import Time
import astropy.units as u


def test_itrs_has_location_attribute_and_accepts_value():
    loc = EarthLocation.from_geodetic(-1 * u.deg, 52 * u.deg, 0 * u.m)
    itrs = ITRS(obstime=Time('J2000'), location=loc)

    # Frame should have a 'location' attribute and it should equal the input
    assert hasattr(itrs, 'location')
    # EarthLocation implements equality by comparing geocentric coordinates
    assert itrs.location == loc
