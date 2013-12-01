"""Utilities for reading WSSA tiles."""

import os
import numpy as np
import pyfits
from ang2pix_ring import ang2pix_ring
from scipy.ndimage import map_coordinates

# global variables
com_pix_tile = {'NSIDE': 64}
com_tiles    = {}
radeg = 180./np.pi

def tile_par_struc(large=True, release='1.0'):
    """
    Create dictionary storing important WSSA tile related parameters.

    Keyword Inputs:
        large   - set for 8k x 8k tiles, default is 3k x 3k
        release - default '1.0', currently only release = '1.0' supported
    """

    # tile sidelength, degrees
    sidelen   = 12.5
    # tile sidelength, pixels
    pix       = (8000. if large else 3000.)
    # pixel scale, asec/pixel
    pscl      = (5.625 if large else 15.)
    # central coordinate, lower left = (0,0)
    crpix     = (3999.5 if large else 1499.5)
    # name of index file with tile centers, etc.
    indexfile = os.path.join(os.environ['WISE_DATA'],
                             'wisetile-index-allsky.fits')
    # file containing HEALPix -> tile lookup table
    lookup = os.path.join(os.environ['WISE_DATA'], 'pixel_lookup.fits')

    # tile extension names
    extens = {'clean' : 0,
              'dirt'  : 1,
              'cov'   : 2,
              'min'   : 3,
              'max'   : 4,
              'amsk'  : 5,
              'omsk'  : 6,
              'art'   : 7 }

    # boolean indicating whether each extension should be treated as a bit-mask
    ismsk  = [0,0,0,0,0,1,1,0]
    # number of tiles, don't want random 430's all over my code
    ntile  = 430
    # default tile path
    tpath  = os.environ['WISE_TILE']
    # conversion from factor from W3 DN to MJy/sr
    calfac = 0.0135172
    # data type for intensity and bit-mask outputs, respectively
    dtype  = ['float32', 'int32']

    par = {'sidelen'   : sidelen,
           'pix'       : pix,
           'crpix'     : crpix,
           'pscl'      : pscl,
           'indexfile' : indexfile,
           'extens'    : extens,
           'ismsk'     : ismsk,
           'ntile'     : ntile,
           'tpath'     : tpath,
           'calfac'    : calfac,
           'lookup'    : lookup, 
           'dtype'     : dtype    }

    return par

def issa_proj_gnom(ra, dec, ra0, dec0, scale):
    """
    Project points from longitude and latitude to a gnomic projection.

    Inputs:
        ra    - array of RA coordinates, assumed radians J2000
        dec   - array of DEC coordinates, assumed radians J2000
        ra0   - array of central RA of projection, radians
        dec0  - array of central DEC of projection, radians
        scale - scale factor of projection in pixels/radian

    Outputs:
        x     - array of x coordinates within each tile, relative to center
        y     - array of y coordinates within each tile, relative to center

    Comments:
       This is my port of an IDL routine, issa_proj_gnom.pro,
       originally written by Doug Finkbeiner.
    """

    A = np.cos(dec)*np.cos(ra-ra0)
    F = scale/(np.sin(dec0)*np.sin(dec) + A*np.cos(dec0))

    x = -F*np.cos(dec)*np.sin(ra-ra0)
    y = F*(np.cos(dec0)*np.sin(dec) - A*np.sin(dec0))

    return x, y

def coord_to_tile(ra, dec, large=True):
    """
    Translate (ra,dec) coordinates to WSSA tiles using HEALPix lookup table.

    Inputs:
        ra  - array of RA coordinates, assumed degrees J2000
        dec - array of DEC coordinates, assumed degrees J2000

    Keyword inputs:
        large    - set for 8k x 8k tiles, default is 3k x 3k

    Outputs:
        tlist - array of tiles corresponding to each (ra, dec) pair
        x     - array of x coordinates within each tile
        y     - array of y coordinates within each tile
    """

    pix = ang2pix_ring(com_pix_tile['NSIDE'], (90.-dec)/radeg, ra/radeg)
    tlist = (com_pix_tile['TILE'])[pix]
    del pix
    par = tile_par_struc(large=large)
    scale = (par['pix']/par['sidelen'])*radeg
    x, y = issa_proj_gnom(ra/radeg, dec/radeg,
                          (com_tiles['RA'])[tlist-1]/radeg,
                          (com_tiles['DEC'])[tlist-1]/radeg, scale)
    x += par['crpix']
    y += par['crpix']

    return tlist, x, y

def uniq(arr):
    """
    Return sorted unique values and indices of their first appearance.

    Inputs:
        arr - a sorted array
    """
    
    r = np.roll(arr, 1)
    bdy = (np.where([r != arr]))[1]

    if len(bdy) == 0:
        return arr[0], np.array([0])

    u = arr[bdy]
    return u, bdy

def tile_val_interp(tnum, x, y, large=True, exten=0, release='1.0',
                    tpath=tile_par_struc()['tpath'], gz=False):
    """
    Use (x,y) pairs and tile numbers to sample values from WSSA tiles.

    Inputs:
        tnum - array of tile numbers, [1, 430]
        x    - array of x coordinates within relevant tiles
        y    - array of y coordinates within relevant tiles

    Keyword inputs:
        large    - set for 8k x 8k tiles, default is 3k x 3k
        exten    - fits extension, default to 0, currently implemented
                   only for scalar exten values
        release  - default '1.0', currently only release = '1.0' supported
        large    - set for 8k x 8k tiles, default is 3k x 3k

    Outputs:
        vals - values at (x,y) sampled from tiles tnum
    """

    par = tile_par_struc(large=large, release=release)
    exten = (exten if isinstance(exten, int) else par['extens'][exten])
    nval = len(tnum.flat)
    sind = np.argsort(tnum)
    tu, bdy = uniq(tnum[sind])
    nu = len(tu.flat)

    fname = (com_tiles['FNAME'])[tnum[sind[bdy]]-1]
    vals = np.zeros(nval, dtype=(par['dtype'])[(par['ismsk'])[exten]])
    for i in range(0, nu):
        indl = bdy[i]
        indu = (nval if (i == (nu-1)) else bdy[i+1])
        xx = x[sind[indl:indu]]
        yy = y[sind[indl:indu]]
        f = os.path.join(tpath, fname[i]) + ('.gz' if gz else '')

        print('[' + str(i+1) + '/' + str(nu) + '] Reading: ' + f + ', ' +
              str(len(xx)) + ' sample'+ 's'*int(len(xx) > 1))

        xoffs = int(max(np.floor(np.min(xx)), 0))
        yoffs = int(max(np.floor(np.min(yy)), 0))

        xmax = int(min(np.ceil(np.max(xx)), par['pix']-1)) + 1
        ymax = int(min(np.ceil(np.max(yy)), par['pix']-1)) + 1

        hdus = pyfits.open(f)
        subim = hdus[exten].section[yoffs:ymax, xoffs:xmax]
        if (par['ismsk'])[exten] == 1:
            vals[sind[indl:indu]] = \
            subim[(np.round(yy)).astype('int')-yoffs,
                  (np.round(xx)).astype('int')-xoffs]
        else:
            vals[sind[indl:indu]] = map_coordinates(subim,
                                                [(yy-yoffs).astype('float32'),
                                                 (xx-xoffs).astype('float32')],
                                                  order=1, mode='nearest')
    return vals

def check_coords(ra, dec):
    """Attempt to ensure ra, dec are numpy arrays, sanity check coordinates"""
    try:
        ra, dec = np.atleast_1d(ra, dec)
    except:
        return False, ra, dec
    good = (ra.shape == dec.shape) & (np.max(np.abs(dec)) <= 90)
    return good, ra, dec

def wssa_getval(ra, dec, exten=0, tilepath=tile_par_struc()['tpath'],
                release='1.0', large=True, mjysr=False, gz=False):
    """
    Sample values from WSSA tiles at specified celestial coordinates.

    Inputs:
        ra  - array of RA coordinates, assumed degrees J2000
        dec - array of DEC coordinates, assumed degrees J2000

    Keyword inputs:
        exten - extension, either as an integer or string, acceptable
                values for release='1.0':
                    0: 'clean'
                    1: 'dirt'
                    2: 'cov'
                    3: 'min'
                    4: 'max'
                    5: 'amsk'
                    6: 'omsk'
                    7: 'art'
        tilepath - directory containing WSSA tiles
        release  - default '1.0', currently only release = '1.0' supported
        large    - set for 8k x 8k tiles, default is 3k x 3k
        mjysr    - set for result in MJy/sr, default is W3 DN

    Outputs:
        vals - values at (ra, dec) sampled from  WSSA tiles
    """

    sane, ra, dec = check_coords(ra, dec)
    if not sane: return -1

    ra = ra.astype('float64')
    dec = dec.astype('float64')

    sh = ra.shape
    ra = ra.ravel()
    dec = dec.ravel()

    tnum, x, y = coord_to_tile(ra, dec, large=large)
    vals = tile_val_interp(tnum, x, y, exten=exten, tpath=tilepath,
                           release=release, large=large, gz=gz)

    par = tile_par_struc(release=release, large=large)
    mask = (par['ismsk'])[exten if isinstance(exten, int) else
                          par['extens'][exten]]

    if mjysr and not mask:
        vals *= par['calfac']

    vals = vals.reshape(sh)

    return vals

def fits2dict(fname):
    """Ingest FITS table and return dictionary containing the data."""
    hdus = pyfits.open(fname)
    cols = hdus[1].columns
    tab  = hdus[1].data

    return dict([(col.name, tab[col.name]) for col in cols])

def init_global():
    """Initialize global variables."""
    global com_pix_tile, com_tiles
    par = tile_par_struc()

    com_pix_tile.update(fits2dict(par['lookup']))
    com_tiles.update(fits2dict(par['indexfile']))

init_global()
