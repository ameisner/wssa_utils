;+
; NAME:
;   check_coords
;
; PURPOSE:
;   sanity check input coordinates
;
; CALLING SEQUENCE:
;   good = check_coords(ra, dec)
;
; INPUTS:
;   ra  - ra values, degrees
;   dec - dec values, degrees
;   
; OPTIONAL INPUTS:
;   
; KEYWORDS:
;   
; OUTPUTS:
;   good - 1 if ra, dec coordinates pass sanity checks, 0 if not
;
; OPTIONAL OUTPUTS:
;   
; EXAMPLES:
;   
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Nov-16 - Aaron Meisner
;----------------------------------------------------------------------
function check_coords, ra, dec

  good = (max(abs(minmax(dec))) LE 90) AND $ 
          array_equal(size(ra, /DIM), size(dec, /DIM))

  return, good
end
