import numpy

def ang2pix_ring(nside, theta, phi):
    """
    Convert from polar coordinates to ring order HEALPix pixel indices.

    Inputs:
        nside - HEALPix nside parameter
        theta - polar angle relative to North pole, RADIANS
        phi   - azimuthal angle, RADIANS

    Outputs:
        ipring - HEALPix ring order pixel indices corresponding to input coords

    Comments:
        Inputs theta and phi must have same shape, currently no checks
        performed.
    
        This is my line-for-line port of ang2pix_ring.pro from the IDL HEALPix
        utilities. I've written this routine because I have found that IDL
        ang2pix_ring outputs do not always agree with those of healpy.ang2pix.
        The pixel indices output by this routine always agree with IDL
        ang2pix_ring, according to my best efforts in testing.

    History:
        2013-Nov-12 - Aaron Meisner, Harvard
    """
    
    sh = theta.shape
    theta = theta.ravel()
    phi = phi.ravel()

    np = len(theta)
    ipring = numpy.zeros(np, dtype='int64')
    pion2 = numpy.pi/2.
    twopi = numpy.pi*2.
    nl2 = 2*nside
    nl4 = 4*nside
    npix = 12*nside*nside
    ncap = nl2*(nside-1)
    
    cth0 = 2./3.

    cth_in = numpy.cos(theta)
    phi_in = phi % twopi
    phi_in[phi <= 0.] =  phi_in[phi <= 0.] + twopi

    pix_eqt = numpy.where((cth_in <= cth0) & (cth_in > -cth0))[0]
    pix_np = numpy.where(cth_in > cth0)[0]
    pix_sp = numpy.where(cth_in <= -cth0)[0]

    n_eqt = len(pix_eqt)
    n_np = len(pix_np)
    n_sp = len(pix_sp)

    if (n_eqt > 0):
        tt = phi_in[pix_eqt]/pion2
        
        jp = (nside*(0.5 + tt - cth_in[pix_eqt]*0.75)).astype('int64')
        jm = (nside*(0.5 + tt + cth_in[pix_eqt]*0.75)).astype('int64')
        
        ir = (nside + 1) + jp - jm
        k = ((ir % 2) == 0).astype('int')
        
        ip = ((jp+jm+k+(1-nside))/2) + 1
        ip = ip - nl4*((ip > nl4).astype('int'))

        ipring[pix_eqt] = ncap + nl4*(ir-1) + ip - 1

    if (n_np > 0):
        tt = phi_in[pix_np]/pion2
        
        tp = (tt % 1.)
        tmp = numpy.sqrt(3.*(1.-numpy.abs(cth_in[pix_np])))

        jp = (nside*tp*tmp).astype('int64')
        jm = (nside*(1.-tp)*tmp).astype('int64')

        ir = jp + jm + 1
        ip = (tt*ir).astype('int64') + 1
        ir4 = 4*ir
        ip = ip - ir4*((ip > ir4).astype('int'))
        
        ipring[pix_np] = 2*ir*(ir-1) + ip - 1

    if (n_sp > 0):
        tt = phi_in[pix_sp]/pion2
        
        tp = (tt % 1.)
        tmp = numpy.sqrt(3.*(1.-numpy.abs(cth_in[pix_sp])))

        jp = (nside*tp*tmp).astype('int64')
        jm = (nside*(1.-tp)*tmp).astype('int64')

        ir = jp + jm + 1
        ip = (tt*ir).astype('int64') + 1
        ir4 = 4*ir
        ip = ip - ir4*((ip > ir4).astype('int'))

        ipring[pix_sp] = npix - 2*ir*(ir+1) + ip - 1

    ipring = ipring.reshape(sh)
    return ipring
