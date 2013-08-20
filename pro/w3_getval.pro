;+
; NAME:
;   w3_getval
;
; PURPOSE:
;   return WSSA tile values sampled at list of input sky locations
;
; CALLING SEQUENCE:
;   vals = w3_getval(ra, dec)
;
; INPUTS:
;   ra - input list of RA values, assumed J2000
;   dec - input list of DEC values, assumed J2000
;
; OPTIONAL INPUTS:
;   exten - extension, either as an integer or string, acceptable
;           values depend on release, but for release='dev':
;                0: clean
;                1: dirt
;                2: cov
;                3: sfd
;                4: min
;                5: max
;                6: amsk
;                7: omsk
;                8: art
;
; KEYWORDS:
;   
; OUTPUTS:
;   vals - values at (ra, dec) interpolated off of WSSA tiles
;
; OPTIONAL OUTPUTS:
;   
; EXAMPLES:
;   
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Aug-19 - Aaron Meisner
;----------------------------------------------------------------------
function w3_getval, ra, dec, exten=exten

  coord_to_tile, ra, dec, tnum, x=x, y=y
  vals = tile_val_interp(tnum, x, y, exten=exten)

; ---- need to properly deal with un-flattening of multi-dimensional input

  return, vals

end
