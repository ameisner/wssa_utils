#!/usr/bin/env python
"""
Unit tests, will eventually repurpose for use with nose.

"""
# if these imports fail, you're already in trouble
import pyfits
import numpy as np
import healpy
import wssa_utils

def test_single_pair():
    """test a single (lon, lat) pair"""

def test_many_coords():
    """lon and lat both 1d arrays, all within single tile"""

def test_many_tiles():
    """lon and lat both 1d arrays, spread over multiple tiles"""

def test_full_sky():
    """lon and lat at every nside=16 HEALPix pixel center"""

def test_2d_coords():
    """lon and lat both 2d arrays, all within single tile"""

def test_2d_many():
    """lon and lat both 2d arrays, spread over multiple tiles"""

def test_bad_lon():
    """see if anything breaks when longitude outside of [0, 360)"""

def test_bad_lat():
    """see if anything breaks when latitude outside of [-90, 90]"""

def test_ext_type():
    """test that extension samples are of correct type, e.g. mask is integer"""

def test_unit_conversion():
    """test that conversion to to MJy/sr from DN happening when appropriate"""

if __name__ == '__main__':
# eventually need to allow tilepath as keyword argument somehow
    """run the above tests"""
    print 'successfully completed testing'
