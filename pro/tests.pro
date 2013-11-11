;+
; NAME:
;   tests
;
; PURPOSE:
;   unit tests for wssa_utils IDL routines
;
; CALLING SEQUENCE:
;   tests
;
; INPUTS:
;   
; OPTIONAL INPUTS:
;   
; KEYWORDS:
;   
; OUTPUTS:
;   
; OPTIONAL OUTPUTS:
;   
; EXAMPLES:
;   
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Nov-6 - Aaron Meisner
;----------------------------------------------------------------------
pro test_single_pair

; test a single (lon, lat) pair

  nsam = 1
  coords = random_lonlat(nsam, /deg)
  ra  = coords[0, *]
  dec = coords[1, *]
  val = w3_getval(ra, dec)
  assert, (n_elements(val) EQ nsam)
  assert, (size(val, /type) EQ 4)
  
end

pro test_many_coords

; lon and lat both 1d arrays, all within single tile

  par = tile_par_struc(/large)
  str = mrdfits(par.indexfile, 1)
  racen  = str[114].ra
  deccen = str[114].dec

  nsam = 100
  ra = randomu(seed, nsam) - 0.5 + racen
  dec = randomu(seed, nsam) - 0.5 + deccen

  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ nsam)
  assert, (size(vals, /type) EQ 4)
  assert, (n_elements(size(val, /DIM)) EQ 1)
  assert, ((size(vals, /DIM))[0] EQ nsam)

end

pro test_many_tiles

  ; lon and lat both 1d arrays, spread over multiple tiles

  nsam = 10
  coords = random_lonlat(nsam, /deg)
  ra = coords[0, *]
  dec = coords[1, *]
  vals = w3_getval(ra, dec)

  assert, (n_elements(vals) EQ nsam)
  assert, (size(vals, /type) EQ 4)
  assert, array_equal(size(vals, /DIM), size(ra, /DIM))

end

pro test_full_sky

; lon, lat for every nside=16 HEALPix pixel center

  nside = 16
  healgen_lb, nside, ra, dec
  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 4)
  assert, array_equal(size(vals, /DIM), size(ra, /DIM))

end

pro test_2d_coords

; lon and lat both 2d arrays, all within single tile

  par = tile_par_struc(/large)
  str = mrdfits(par.indexfile, 1)
  racen  = str[114].ra
  deccen = str[114].dec

  nsam = 100
  ra = randomu(seed, nsam) - 0.5 + racen
  dec = randomu(seed, nsam) - 0.5 + deccen

  sz = [10, 10]
  ra = reform(ra, sz[0], sz[1])
  dec = reform(dec, sz[0], sz[1])

  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 4)
  assert, array_equal(size(vals, /DIM), sz)

end

pro test_2d_many

; lon and lat both 2d arrays, spread over multiple tiles

  par = tile_par_struc(/large)
  str = mrdfits(par.indexfile, 1)
  racen  = str[114].ra
  deccen = str[114].dec

  nsam = 100
  dist = 10.
  ra = dist*(randomu(seed, nsam) - 0.5) + racen
  dec = dist*(randomu(seed, nsam) - 0.5) + deccen

  sz = [20, 5] ; non-square
  ra = reform(ra, sz[0], sz[1])
  dec = reform(dec, sz[0], sz[1])

  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 4)
  assert, array_equal(size(vals, /DIM), sz)

end

pro test_bad_lon

; see if anything breaks when longitude outside of [0, 360)

  tol = 1e-5
  ra  = [-10.d, 370.d]
  dec = [ 45.d,  45.d]

  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 4)

  tru = w3_getval((ra + 360.d) MOD 360, dec)
  assert, (total(abs(tru-vals) GT tol) EQ 0)

end

pro test_bad_lat

; see if anything breaks when latitude outside of [-90, 90]

  ra  = [  45.d,  45.d] ; arb
  dec = [-100.d, 100.d]

  vals = w3_getval(ra, dec)

end

pro test_ext_type

; test that extension samples are of correct type, e.g. mask is integer

  nsam = 1
  coords = random_lonlat(nsam, /deg)
  ra = coords[0, *]
  dec = coords[1, *]

  par = tile_par_struc(/large, release='1.0')
  msk = par.ismsk
  for ext=0, n_elements(msk)-1 do begin
      if ~msk[ext] then continue
      val = w3_getval(ra, dec, exten=ext)
      assert, (n_elements(val) EQ nsam)
      assert, (size(val, /type) EQ 3) ; long     
  endfor

end

pro test_poles

; see if anything breaks at poles

  ra  = [  0.d,  0.d]
  dec = [-90.d, 90.d]

  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 4)
  assert, (total(~finite(vals)) EQ 0)

end

pro test_unit_conversion

; test that conversion to MJy/sr from DN happening when appropriate

  nsam = 1
  coords = random_lonlat(nsam, /deg)

  ra  = coords[0, *]
  dec = coords[1, *]
  val = w3_getval(ra, dec)
  val_mjysr = w3_getval(ra, dec, /mjysr)
  
  assert, (n_elements(val_mjysr) EQ nsam)
  assert, (size(val_mjysr, /type) EQ 4)

  assert, (val[0] NE 0)

  rat = val_mjysr[0]/val[0]
  tol = 1e-5

  par = tile_par_struc(/large)
  tru = par.calfac
  assert, (abs(rat-tru) LT tol)

end

pro tests

; run unit tests

  test_single_pair
  test_many_coords
  test_many_tiles
  test_full_sky
  test_2d_coords
  test_2d_many
  test_bad_lon
  test_poles
  test_unit_conversion
  test_ext_type

end
