import os
import numpy
import pyfits
import healpy
from scipy.ndimage import map_coordinates

# global variables
com_pix_tile = {'NSIDE': 64}
com_tiles    = {}
radeg = 180./numpy.pi

def tile_par_struc(large=0, w4=0, release='1.0'):
    # tile sidelength, degrees
    sidelen = 12.5 # python float = 32 bits, right?
    # tile sidelength, pixels
    pix = (8000. if large else 3000.)
    # pixel scale, asec/pixel
    pscl = (5.625 if large else 15.)
    # central coordinate, lower left = (0,0)
    crpix = (3999.5 if large else 1499.5)
    # name of index file with tile centers, etc.
    indexfile = os.path.join(os.environ['WISE_DATA'],
                             'wisetile-index-allsky.fits')
    # extension names, clean this up later, for now useful to see list
    if release == 'dev':
        extens = {'clean' : 0,
                  'dirt'  : 1,
                  'cov'   : 2,
                  'sfd'   : 3,
                  'min'   : 4,
                  'max'   : 5,
                  'amsk'  : 6,
                  'omsk'  : 7,
                  'art'   : 8 }
    else:
        extens = {'clean' : 0,
                  'dirt'  : 1,
                  'cov'   : 2,
                  'min'   : 3,
                  'max'   : 4,
                  'amsk'  : 5,
                  'omsk'  : 6,
                  'art'   : 7 }
    # boolean indicating whether each extension should be treated as a bit-mask
    ismsk = ([0,0,0,0,0,0,1,1,0] if (release == 'dev') else [0,0,0,0,0,1,1,])
    # number of tiles, don't want random 430's all over my code
    ntile = 430
    # default tile path
    tpath = '/fink1/ameisner/tile-combine-8k' if large else \
            '/fink1/ameisner/tile-planck-zp'
    # conversion from factor from W3 DN to MJy/sr
    calfac = 0.0163402

    par = {'sidelen'   : sidelen,
           'pix'       : pix,
           'crpix'     : crpix,
           'pscl'      : pscl,
           'indexfile' : indexfile,
           'extens'    : extens,
           'ismsk'     : ismsk,
           'ntile'     : ntile,
           'tpath'     : tpath,
           'calfac'    : calfac   }

    return par

def issa_proj_gnom(ra, dec, ra0, dec0, scale):
    # all inputs need to be in radians
    A = numpy.cos(dec)*numpy.cos(ra-ra0)
    F = scale/(numpy.sin(dec0)*numpy.sin(dec) + A*numpy.cos(dec0))

    x = -F*numpy.cos(dec)*numpy.sin(ra-ra0)
    y = F*(numpy.cos(dec0)*numpy.sin(dec) - A*numpy.sin(dec0))

    return x, y

def coord_to_tile(ra, dec, large=0):
    # assume ra,dec in degrees
    pix = healpy.ang2pix(com_pix_tile['NSIDE'], (90.-dec)/radeg, ra/radeg)
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

def tile_interp_val(tnum, x, y, large=0, exten=0, release='1.0', tpath=''):
    
    par = tile_par_struc(large=large, release=release)
    if isinstance(exten, str):
        exten = (par['extens'])[exten]
    if tpath == '':
        tpath = par['tpath']
    nval = len(tnum.flat)
    sind = numpy.argsort(tnum)
    tu, bdy = numpy.unique(tnum[sind], return_index=True)
    nu = len(tu.flat)

    fname = os.path.join(tpath, (com_tiles['FNAME'])[tnum[sind[bdy]]-1])
    vals = numpy.zeros(nval, dtype='float')
    for i in range(0, nu):
        indl = bdy[i]
        indu = (nval if (i == (nu-1)) else bdy[i+1])
        print 'reading: ' + fname[i]
        xx = x[sind[indl:indu]]
        yy = y[sind[indl:indu]]

        xoffs = int(max(numpy.floor(numpy.min(xx)), 0))
        yoffs = int(max(numpy.floor(numpy.min(yy)), 0))

        xmax = int(min(numpy.ceil(numpy.max(xx)), par['pix']-1)) + 1 # <---
        ymax = int(min(numpy.ceil(numpy.max(yy)), par['pix']-1)) + 1 # <---

        hdus = pyfits.open(fname[i])
        subim = hdus[exten].section[xoffs:xmax, yoffs:ymax]
        if (par['ismsk'])[exten] == 1:
            vals[sind[indl:indu]] = \
            subim[(numpy.round(xx)).astype('int')-xoffs,
                  (numpy.round(yy)).astype('int')-yoffs]
        else:
            vals[sind[indl:indu]] = map_coordinates(subim,
                                                    [xx-xoffs, yy-yoffs],
                                                    order=1,
                                                    cval=numpy.nan)
        # the above line has all kinds of possible issues, need to investigate
    return vals

def w3_getval(ra, dec, exten=0, tilepath='', release='1.0', large=0,
              mjysr=0):
    tnum, x, y = coord_to_tile(ra, dec, large=large)
    vals = tile_interp_val(tnum, x, y, exten=exten, tpath=tilepath,
                           release=release, large=large)
    if mjysr:
        par = tile_par_struc(release=release, large=large)
        vals *= par['calfac']
    
    return vals

def init_dict(keys, name):
    fname = os.path.join(os.environ['WISE_DATA'], name)
    hdus = pyfits.open(fname)
    tab = hdus[1].data
    d = {}
    for key in keys:
        d[key] = tab[key]
    return d

def init_global():
    global com_pix_tile, com_tiles
    print 'loading auxiliary data...'
    com_pix_tile.update(init_dict(['PIX', 'TILE'], 'pixel_lookup.fits'))
    com_tiles   = init_dict(['FNAME', 'RA', 'DEC', 'LGAL', 'BGAL'],
                            'wisetile-index-allsky.fits')
    print '...done'

init_global()
