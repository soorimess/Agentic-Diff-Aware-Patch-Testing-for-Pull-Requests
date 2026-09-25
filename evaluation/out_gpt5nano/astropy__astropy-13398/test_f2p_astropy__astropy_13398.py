# Regression test for astropy/astropy#13398: ITRS should accept a topocentric location argument

from astropy import units as u
from astropy.coordinates import ITRS, EarthLocation
from astropy.time import Time


def test_itrs_accepts_location_argument_after_fix():
    t = Time('2020-01-01T00:00:00', scale='utc')
    loc = EarthLocation.from_geodetic(lon=10 * u.deg, lat=20 * u.deg, height=2 * u.km)

    itrs = ITRS(obstime=t, location=loc)

    assert isinstance(itrs, ITRS)
    assert itrs.obstime == t
    assert isinstance(itrs.location, EarthLocation)
