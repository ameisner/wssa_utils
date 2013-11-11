pro test_xy_single, outname

; convert one lon, lat pair to x, y with coord_to_tile

  ra  = [ 308.49839d]
  dec = [-30.757660d]
  coord_to_tile, ra, dec, tnum, x=x, y=y, /large

  writefits, outname, x
  writefits, outname, y, /append

end

pro test_xy_many, outname

; convert more than one lon, lat pair to x,y with coord_to_tile

  ra  = [228.06533d, 336.88487d,  132.85047d, 296.63675d, 174.24343d, $ 
          304.68113d]
  dec = [9.6944888d, 25.149593d, -29.273778d, 11.994469d, 43.651411d, $ 
         -10.985369d]
  coord_to_tile, ra, dec, tnum, x=x, y=y, /large

  writefits, outname, x
  writefits, outname, y, /append

end

pro test_xy_heal, outname

; convert all HEALPix nside = 16 pixel centers to tile x, y

  nside = 16

  pix2ang_ring, 16, lindgen(12L*16*16), theta, phi
  radeg = (180.d/!dpi)
  ra = phi*radeg
  dec = 90.d - radeg*theta
  coord_to_tile, ra, dec, tnum, x=x, y=y, /large

  writefits, outname, x
  writefits, outname, y, /append
  writefits, outname, tnum, /append

end

pro test_xy_rect, outname, fname=fname

; convert all ra, dec in rectangular grid to tile x, y

  if ~keyword_set(fname) then fname = 'rect.fits'
  fname = concat_dir('$WISE_DATA', fname)

  ra  = readfits(fname)
  dec = readfits(fname, ex=1)
  coord_to_tile, ra, dec, tnum, x=x, y=y, /large

  writefits, outname, x
  writefits, outname, y, /append
  writefits, outname, tnum, /append

end

pro test_vals_rect, outname, fname=fname

; sample values for all ra, dec in rectangular grid

  if ~keyword_set(fname) then fname = 'rect.fits'
  fname = concat_dir('$WISE_DATA', fname)

  ra  = readfits(fname)
  dec = readfits(fname, ex=1)

  vals = w3_getval(ra, dec)
  writefits,  outname, vals

end

pro compare_xy_outputs, fpython, fidl

; check Python vs. IDL fits outputs for consistency

  print, 'python output in : ', fpython
  print, 'IDL output in :', fidl

  xp = readfits(fpython)
  xi = readfits(fidl)

  yp = readfits(fpython, ex=1)
  yi = readfits(fidl, ex=1)

  assert, (total(xi NE xp) EQ 0)
  assert, (total(yi NE yp) EQ 0)

  print, 'comparison finished successfully'
end
