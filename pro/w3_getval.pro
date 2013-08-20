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
;   ra - input list of RA values
;   dec - input list of DEC values
;
; OPTIONAL INPUTS:
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
function w3_getval, ra, dec

  coord_to_tile, ra, dec, tnum, x=x, y=y
  vals = tile_val_interp(tnum, x, y)

  return, vals

end
