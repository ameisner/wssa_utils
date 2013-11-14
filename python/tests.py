#!/usr/bin/env python
"""
Unit tests, will eventually repurpose for use with nose.

"""
# if these imports fail, you're already in trouble
import pyfits
import numpy as np
from pix2ang_ring import pix2ang_ring
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
    print test_many_coords.__doc__

    racen = wssa_utils.com_tiles['RA'][114]
    deccen = wssa_utils.com_tiles['DEC'][114]
    nsam = 100
    ra = np.random.rand(nsam) - 0.5 + racen
    dec = np.random.rand(nsam) - 0.5 + deccen
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.dtype.name == 'float32'
    assert vals.shape == (nsam,)
    
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
    """lon, lat for every nside=16 HEALPix pixel center"""
    print test_full_sky.__doc__
    
    nside = 16
    npix = 12*(nside**2)
    pix = np.arange(npix)
    theta, phi = pix2ang_ring(nside, pix)
    ra = (180./np.pi)*phi
    dec = 90. - (180./np.pi)*theta
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.shape == (npix,)

def test_2d_coords():
    """lon and lat both 2d arrays, all within single tile"""
    print test_2d_coords.__doc__

    racen = wssa_utils.com_tiles['RA'][114]
    deccen = wssa_utils.com_tiles['DEC'][114]
    nsam = 100
    ra = np.random.rand(nsam) - 0.5 + racen
    dec = np.random.rand(nsam) - 0.5 + deccen
    sh = (10, 10)
    ra = ra.reshape(sh)
    dec = dec.reshape(sh)
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.shape == sh

def test_2d_many():
    """lon and lat both 2d arrays, spread over multiple tiles"""
    print test_2d_many.__doc__

    racen = wssa_utils.com_tiles['RA'][114]
    deccen = wssa_utils.com_tiles['DEC'][114]
    nsam = 100
    dist = 10.
    ra = dist*(np.random.rand(nsam) - 0.5) + racen
    dec = dist*(np.random.rand(nsam) - 0.5) + deccen
    sh = (20, 5) # try non-square
    ra = ra.reshape(sh)
    dec = dec.reshape(sh)
    vals = wssa_utils.w3_getval(ra, dec)
    assert isinstance(vals, np.ndarray)
    assert vals.shape == sh

def test_bad_lon():
    """see if anything breaks when longitude outside of [0, 360)"""
    print test_bad_lon.__doc__

    tol = 1e-5
    dec = np.array([45.]) # arb
    for r in [-10., 370.]:
        ra = np.array([r])
        val = wssa_utils.w3_getval(ra, dec)
        assert isinstance(val, np.ndarray)
        assert val.dtype.name == 'float32'
        assert val.shape == (1,)        
        tru = wssa_utils.w3_getval(np.array([(r+360.) % 360.]), dec)
        assert np.abs(val-tru) < tol

def test_bad_lat():
    """see if anything breaks when latitude outside of [-90, 90]"""
    print test_bad_lat.__doc__

    ra = np.array([45.]) #arb
    # just see if this runs without crashing ...
    for d in [-100., 100.]:
        dec = np.array([d])
        val = wssa_utils.w3_getval(ra, dec)

def test_ext_type():
    """test that extension samples are of correct type, e.g. mask is integer"""
    print test_ext_type.__doc__

    nsam = 1
    ra, dec = random_lonlat(nsam, deg=True)
    msk = wssa_utils.tile_par_struc()['ismsk']
    for ext, ismsk in enumerate(msk):
        if not ismsk: continue
        val = wssa_utils.w3_getval(ra, dec, exten=ext)
        assert isinstance(val, np.ndarray)
        assert val.dtype.name == 'int32'

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
    test_ext_type()
    test_many_coords()
    test_2d_coords()
    test_2d_many()
    print 'successfully completed testing'
