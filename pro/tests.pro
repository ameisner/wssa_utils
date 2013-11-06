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

end

pro test_many_tiles

end

pro test_full_sky

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

end
