#!/usr/bin/env python
"""
Unit tests, will eventually repurpose for use with nose.

"""
# if these imports fail, you're already in trouble
import pyfits
import numpy as np
import healpy
import wssa_utils
from random_lonlat import random_lonlat

def test_single_pair():
    """test a single (lon, lat) pair"""
    print test_single_pair.__doc__

    nsam = 1
    ra, dec = random_lonlat(nsam, deg=True)
    val = wssa_utils.w3_getval(ra, dec)
    assert isinstance(val, np.ndarray)
    assert val.dtype.name == 'float32'
    assert val.shape == (nsam,)

def test_many_coords():
    """lon and lat both 1d arrays, all within single tile"""

def test_many_tiles():
    """lon and lat both 1d arrays, spread over multiple tiles"""
    print test_many_tiles.__doc__
    
    nsam = 10
    ra, dec = random_lonlat(nsam, deg=True)
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.dtype.name == 'float32'
    assert vals.shape == (nsam,)

def test_full_sky():
    """lon and lat at every nside=16 HEALPix pixel center"""
    print test_full_sky.__doc__
    
    nside = 16
    npix = healpy.pixelfunc.nside2npix(nside)
    pix = np.arange(npix)
    theta, phi = healpy.pixelfunc.pix2ang(nside, pix)
    ra = (180./np.pi)*phi
    dec = 90. - (180./np.pi)*theta
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.shape == (npix,)

def test_2d_coords():
    """lon and lat both 2d arrays, all within single tile"""

def test_2d_many():
    """lon and lat both 2d arrays, spread over multiple tiles"""

def test_bad_lon():
    """see if anything breaks when longitude outside of [0, 360)"""
    print test_bad_lon.__doc__

    dec = np.array([45.]) # arb
    for r in [-10., 370.]:
        ra = np.array([r])
        val = wssa_utils.w3_getval(ra, dec)
        assert isinstance(val, np.ndarray)
        assert val.dtype.name == 'float32'
        assert val.shape == (1,)

def test_bad_lat():
    """see if anything breaks when latitude outside of [-90, 90]"""

def test_ext_type():
    """test that extension samples are of correct type, e.g. mask is integer"""

def test_poles():
    """see if anything breaks at poles"""
    print test_poles.__doc__
    
    ra = np.array([0.])
    for d in [-90., 90.]:
        dec = np.array([d])
        val = wssa_utils.w3_getval(ra, dec)
        assert isinstance(val, np.ndarray)
        assert val.dtype.name == 'float32'
        assert val[0] != 0

def test_unit_conversion():
    """test that conversion to to MJy/sr from DN happening when appropriate"""
    print test_unit_conversion.__doc__

    nsam = 1
    ra, dec = random_lonlat(nsam, deg=True)
    val = wssa_utils.w3_getval(ra, dec)
    val_mjysr = wssa_utils.w3_getval(ra, dec, mjysr=True)
    assert isinstance(val_mjysr, np.ndarray)
    assert val_mjysr.dtype.name == 'float32'
    assert val.shape == (nsam,)
    assert val[0] != 0

    rat = val_mjysr[0]/val[0]
    tol = 1.0e-5
    tru = wssa_utils.tile_par_struc()['calfac']
    assert np.abs(rat-tru) < tol

if __name__ == '__main__':
# eventually need to allow tilepath as keyword argument somehow
    """run the above tests"""
    test_single_pair()
    test_many_tiles()
    test_unit_conversion()
    test_poles()
    test_bad_lon()
    print 'successfully completed testing'
