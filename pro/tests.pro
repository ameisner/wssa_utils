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
  assert, (size(val, /type) EQ 5)
  
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
  assert, (size(vals, /type) EQ 5)
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
  assert, (size(vals, /type) EQ 5)
  assert, array_equal(size(vals, /DIM), size(ra, /DIM))

end

pro test_full_sky

; lon and lat at every nside=16 HEALPix pixel center

  nside = 16
  healgen_lb, nside, ra, dec
  vals = w3_getval(ra, dec)
  assert, (n_elements(vals) EQ n_elements(ra))
  assert, (size(vals, /type) EQ 5)
  assert, array_equal(size(vals, /DIM), size(ra, /DIM))

end

pro test_2d_coords

end

pro test_2d_many

end

pro test_bad_lon

end

pro test_bad_lat

end

pro test_ext_type

end

pro test_poles

end

pro test_unit_conversion

end

pro tests

; run unit tests

  test_single_pair
  test_many_coords
  test_many_tiles
  test_full_sky

end
