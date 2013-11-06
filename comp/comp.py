import numpy as np
import pyfits
import wssa_utils

def coords2fits(x, y, outname):
    """write multi-extension fits file given arrays of x, y coordinates"""
    hdu_x = pyfits.PrimaryHDU(x)
    hdu_y = pyfits.ImageHDU(y)
    hdulist = pyfits.HDUList([hdu_x, hdu_y])
    hdulist.writeto(outname)   

def test_xy_single(outname):
    """convert one lon, lat pair to x, y with coord_to_tile"""
    ra = np.array([308.49839])
    dec = np.array([-30.757660])
    _, x, y = wssa_utils.coord_to_tile(ra, dec)
    coords2fits(x, y, outname)

def test_xy_many(outname):
    """convert more than one lon, lat pair to x,y with coord_to_tile"""
    ra  = np.array([228.06533, 336.88487,  132.85047, 296.63675, 174.24343,
                     304.68113])
    dec = np.array([9.6944888, 25.149593, -29.273778, 11.994469, 43.651411,
                    -10.985369])
    _, x, y = wssa_utils.coord_to_tile(ra, dec)
    coords2fits(x, y, outname)

def test_xy_heal():
    """convert all HEALPix nside = 16 pixel centers to tile x, y"""

def test_xy_rect():
    """convert all ra, dec in rectangular grid to tile x, y"""
