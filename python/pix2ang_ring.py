import numpy

def pix2ang_ring(nside, ipix):
    """
    Convert from ring order HEALPix pixel index to polar coordinates.

    Inputs:
        nside - HEALPix nside parameter
        ipix  - HEALPix pixel indices, ring order

    Outputs:
        theta - polar angle relative to North pole, RADIANS
        phi   - azimuthal angle, RADIANS

    Comments:
        input ipix must be a numpy array
    
        This is my line-for-line port of pix2ang_ring.pro from the IDL HEALPix
        utilities. I've written this routine because I have found that IDL
        pix2ang_ring outputs do not always agree identically with those of 
        healpy.pix2ang. The coordinates output by this routine always agree 
        with IDL pix2ang_ring, according to my best efforts in testing.

    History:
        2013-Nov-14 - Aaron Meisner, Harvard
    """

    npix = 12*nside*nside
    nl1 = nside
    nl2 = 2*nl1
    if (nl1 > 8192):
        nl4 = long(4)*nl1
        ncap = nl2*(nl1-long(1))
        nsup = nl2*(long(5)*nl1+long(1))
        one = long(1)
        four = long(4)
        l64 = 1
    else:
        nl4 = 4*nl1
        ncap = nl2*(nl1-1)
        nsup = nl2*(5*nl1+1)
        one = 1
        four = 4
        l64 = 0
    fact1 = 1.5*nl1
    fact2 = (3.0*nl1)*nl1
    np = len(ipix)
    theta = numpy.zeros(np, dtype='float64')
    phi = numpy.zeros(np, dtype='float64')


    pix_np = numpy.where(ipix < ncap)[0]
    n_np = len(pix_np)
    if (n_np > 0):
        ip = numpy.round(ipix[pix_np]) + one
        iring = (numpy.sqrt(ip/2.-numpy.sqrt(ip/2))).astype('int') + 1
        iphi = ip - 2*iring*(iring-one)

        theta[pix_np] = numpy.arccos(1. - numpy.power(iring.astype('float64'), 2)/fact2)
        phi[pix_np] = (iphi - 0.5)*numpy.pi/(2.*iring)

    pix_eq = numpy.where((ipix >= ncap) & (ipix < nsup))[0]
    n_eq = len(pix_eq)
    if (n_eq > 0):
        ip = numpy.round(ipix[pix_eq]) - ncap
        iring = (ip/nl4).astype('int') + nl1
        iphi = (ip % nl4) + one

        fodd = 0.5*(1+((iring+nl1) % 2))

        theta[pix_eq] = numpy.arccos((nl2-iring)/fact1)
        phi[pix_eq] = (iphi-fodd)*numpy.pi/(2.*nl1)

    pix_sp = numpy.where(ipix >= nsup)[0]
    n_sp = len(pix_sp)
    if (n_sp > 0):
        ip = npix - numpy.round(ipix[pix_sp])
        iring = (numpy.sqrt(ip/2.-numpy.sqrt(ip/2))).astype('int') + 1
        iphi = one + four*iring - (ip - 2*iring*(iring-one))

        theta[pix_sp] = numpy.arccos(-1. + numpy.power(iring.astype('float64'), 2)/fact2)
        phi[pix_sp] = (iphi-0.5)*numpy.pi/(2.*iring)

    return theta, phi
