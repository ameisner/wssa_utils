import numpy as np
import pyfits
import wssa_utils
from pix2ang_ring import pix2ang_ring
import os

def arrs2fits(outname, *arrs):
    """write multi-extension fits file with input arrays as image extensions"""
    hdus = []
    for i, arr in enumerate(arrs):
        hdus.append(pyfits.ImageHDU(arr) if i is not 0 else
                    pyfits.PrimaryHDU(arr))

    hdulist = pyfits.HDUList(hdus)
    hdulist.writeto(outname)

def test_xy_single(outname):
    """convert one lon, lat pair to x, y with coord_to_tile"""
    ra = np.array([308.49839])
    dec = np.array([-30.757660])
    _, x, y = wssa_utils.coord_to_tile(ra, dec)
    arrs2fits(outname, x, y)

def test_xy_many(outname):
    """convert more than one lon, lat pair to x,y with coord_to_tile"""
    ra  = np.array([228.06533, 336.88487,  132.85047, 296.63675, 174.24343,
                     304.68113])
    dec = np.array([9.6944888, 25.149593, -29.273778, 11.994469, 43.651411,
                    -10.985369])
    _, x, y = wssa_utils.coord_to_tile(ra, dec)
    arrs2fits(outname, x, y)

def test_xy_heal(outname, nside=16):
    """convert all HEALPix pixel centers to tile x, y"""
    npix = 12*nside*nside
    pix = np.arange(npix)
    theta, phi = pix2ang_ring(nside, pix)
    ra = (180./np.pi)*phi
    dec = 90. - (180./np.pi)*theta
    tnum, x, y = wssa_utils.coord_to_tile(ra, dec)
    arrs2fits(outname, x, y, tnum)

def test_xy_rect(outname, fname='rect.fits'):
    """convert all ra, dec in rectangular grid to tile x, y"""
    fname = os.path.join(os.environ['WISE_DATA'], fname)
    hdus = pyfits.open(fname)
    ra  = hdus[0].data
    dec = hdus[1].data

    tnum, x, y = wssa_utils.coord_to_tile(ra, dec)
    arrs2fits(outname, x, y, tnum)

def test_val_float(outname):
    """get tile value for one lon, lat pair"""
    ra = np.array([308.49839])
    dec = np.array([-30.757660])

    ra  = ra.astype('float32')
    dec = dec.astype('float32')

    val = wssa_utils.wssa_getval(ra, dec)
    arrs2fits(outname, val)

def test_vals_float(outname):
    """get tile values more than one lon, lat pair"""
    ra  = np.array([228.06533, 336.88487,  132.85047, 296.63675, 174.24343,
                     304.68113])
    dec = np.array([9.6944888, 25.149593, -29.273778, 11.994469, 43.651411,
                    -10.985369])  
    ra  = ra.astype('float32')
    dec = dec.astype('float32')

    vals = wssa_utils.wssa_getval(ra, dec)
    arrs2fits(outname, vals)
    
def test_edge_interp(outname):
    """
    engineer extreme test cases for interpolation near or off of tile edges
    such cases may never actually arise when running wssa_getval
    """
    x = np.array([-0.23647, -1.0, -10.5, 0.,    1619.25, 7999.5, 8000.,
                  2893.81])
    y = np.array([ 4190.14, -1.0, -5.5 , 0., -0.0952951, 7999.5, 8000.,
                   8000.5])
    nsam = len(x)
    tnum = np.zeros(nsam,dtype='int')+115
    par = wssa_utils.tile_par_struc()
    tpath = par['tpath']
    vals = wssa_utils.tile_val_interp(tnum, x, y, large=True, release='1.0',
                                      tpath=tpath)
    arrs2fits(outname, vals)

def test_vals_rect(outname, fname='rect.fits', exten=0):
    """sample values for all ra, dec in rectangular grid"""
    fname = os.path.join(os.environ['WISE_DATA'], fname)
    hdus = pyfits.open(fname)
    ra  = hdus[0].data
    dec = hdus[1].data

    vals = wssa_utils.wssa_getval(ra, dec, exten=exten)
    arrs2fits(outname, vals)

def test_vals_mjysr(outname):
    """test that conversion to MJy/sr doesn't create any problems"""
    ra  = np.array([228.06533, 336.88487,  132.85047, 296.63675, 174.24343,
                     304.68113])
    dec = np.array([9.6944888, 25.149593, -29.273778, 11.994469, 43.651411,
                    -10.985369])

    vals = wssa_utils.wssa_getval(ra, dec, mjysr=True)
    arrs2fits(outname, vals)
