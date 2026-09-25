# Licensed under a 3-clause BSD style license - see LICENSE.rst

import warnings

import numpy as np

from astropy import units as u
from astropy.coordinates import EarthLocation, AltAz, CartesianRepresentation, HADec, ITRS
from astropy.tests.helper import assert_quantity_allclose as assert_allclose
from astropy.time import Time
from astropy.utils import iers


def test_topocentric_itrs_observed_transform_uses_local_vector():
    t = Time("J2010")
    location = EarthLocation(lon=-1*u.deg, lat=52*u.deg, height=0*u.m)
    overhead = EarthLocation(lon=-1*u.deg, lat=52*u.deg, height=10*u.km)
    topocentric_up = overhead.get_itrs(t).cartesian - location.get_itrs(t).cartesian

    lon = location.lon.to_value(u.radian)
    lat = location.lat.to_value(u.radian)
    north = CartesianRepresentation(
        -np.sin(lat)*np.cos(lon)*10*u.km,
        -np.sin(lat)*np.sin(lon)*10*u.km,
        np.cos(lat)*10*u.km)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", iers.IERSWarning)
        warnings.simplefilter("ignore", iers.IERSStaleWarning)

        topocentric_itrs = ITRS(topocentric_up, obstime=t, location=location)
        altaz = topocentric_itrs.transform_to(AltAz(obstime=t, location=location))
        hadec = topocentric_itrs.transform_to(HADec(obstime=t, location=location))

        assert_allclose(altaz.alt, 90*u.deg, atol=1*u.uas, rtol=0)
        assert_allclose(altaz.distance, 10*u.km, atol=1*u.mm, rtol=0)
        assert_allclose(hadec.ha, 0*u.hourangle, atol=1*u.uas, rtol=0)
        assert_allclose(hadec.dec, location.lat, atol=1*u.uas, rtol=0)
        assert_allclose(hadec.distance, 10*u.km, atol=1*u.mm, rtol=0)

        north_itrs = ITRS(north, obstime=t, location=location)
        north_altaz = north_itrs.transform_to(AltAz(obstime=t, location=location))
        north_hadec = north_itrs.transform_to(HADec(obstime=t, location=location))

        assert_allclose(north_altaz.az, 0*u.deg, atol=1*u.uas, rtol=0)
        assert_allclose(north_altaz.alt, 0*u.deg, atol=1*u.uas, rtol=0)
        assert_allclose(north_altaz.distance, 10*u.km, atol=1*u.mm, rtol=0)
        assert_allclose(north_hadec.ha, -12*u.hourangle, atol=1*u.uas, rtol=0)
        assert_allclose(north_hadec.dec, (90*u.deg - location.lat),
                        atol=1*u.uas, rtol=0)
        assert_allclose(north_hadec.distance, 10*u.km, atol=1*u.mm, rtol=0)

        itrs_frame = ITRS(obstime=t, location=location)
        altaz_itrs = AltAz(alt=90*u.deg, az=0*u.deg, distance=10*u.km,
                           obstime=t, location=location).transform_to(itrs_frame)
        hadec_itrs = HADec(ha=0*u.hourangle, dec=location.lat,
                           distance=10*u.km, obstime=t,
                           location=location).transform_to(itrs_frame)

        assert_allclose(altaz_itrs.cartesian.xyz, topocentric_up.xyz,
                        atol=1*u.mm, rtol=0)
        assert_allclose(hadec_itrs.cartesian.xyz, topocentric_up.xyz,
                        atol=1*u.mm, rtol=0)
