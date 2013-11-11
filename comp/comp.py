import numpy as np
import pyfits
import wssa_utils
import healpy
import os

def coords2fits(x, y, outname, tnum=None):
    """write multi-extension fits file given arrays of x, y coordinates"""
    hdus = []
    hdus.append(pyfits.PrimaryHDU(x))
    hdus.append(pyfits.ImageHDU(y))
    if tnum is not None:
        hdus.append(pyfits.ImageHDU(tnum))

    hdulist = pyfits.HDUList(hdus)
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

def test_xy_heal(outname):
    """convert all HEALPix nside = 16 pixel centers to tile x, y"""
    nside = 16
    npix = healpy.pixelfunc.nside2npix(nside)
    pix = np.arange(npix)
    theta, phi = healpy.pixelfunc.pix2ang(nside, pix)
    ra = (180./np.pi)*phi
    dec = 90. - (180./np.pi)*theta
    tnum, x, y = wssa_utils.coord_to_tile(ra, dec)
    coords2fits(x, y, outname, tnum=tnum)

def test_xy_rect(outname, fname='rect.fits'):
    """convert all ra, dec in rectangular grid to tile x, y"""
    fname = os.path.join(os.environ['WISE_DATA'], fname)
    hdus = pyfits.open(fname)
    ra  = hdus[0].data
    dec = hdus[1].data

    tnum, x, y = wssa_utils.coord_to_tile(ra, dec)
    coords2fits(x, y, outname, tnum=tnum)

def test_vals_rect(outname, fname='rect.fits'):
    """sample values for all ra, dec in rectangular grid"""
    fname = os.path.join(os.environ['WISE_DATA'], fname)
    hdus = pyfits.open(fname)
    ra  = hdus[0].data
    dec = hdus[1].data

    vals = wssa_utils.w3_getval(ra, dec)
