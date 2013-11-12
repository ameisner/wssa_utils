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

pro test_val_float, outname

; get tile value for one lon, lat pair

  ra  = [ 308.49839d]
  dec = [-30.757660d]

  ra  = float(ra)
  dec = float(dec)

  val = w3_getval(ra, dec)
  writefits, outname, val

end

pro test_vals_float, outname

; get tile values more than one lon, lat pair

  ra  = [228.06533d, 336.88487d,  132.85047d, 296.63675d, 174.24343d, $ 
          304.68113d]
  dec = [9.6944888d, 25.149593d, -29.273778d, 11.994469d, 43.651411d, $ 
         -10.985369d]

  ra  = float(ra)
  dec = float(dec)

  vals = w3_getval(ra, dec)
  writefits, outname, vals

end

pro compare_outputs, fp, fi

; check Python vs. IDL fits outputs for consistency

  print, 'Python output in : ', fp
  print, 'IDL output in :', fi

  fits_info, fp, /silent, n_ext=n_ext

  for exten=0, n_ext do begin
      p = readfits(fp, ex=exten, /silent)
      i = readfits(fi, ex=exten, /silent)
      print, 'checking extension:', exten, ' , ', n_elements(p), ' values'
      assert, (total(i NE p) EQ 0)
  endfor

  print, 'comparison finished successfully'
end
