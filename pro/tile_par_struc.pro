;+
; NAME:
;   tile_par_struc
;
; PURPOSE:
;   repository for WSSA tile related parameters
;
; CALLING SEQUENCE:
;   par = tile_par_struc(large=, w4=)
;
; KEYWORDS:
;   large - set for large version of tiles (8k x 8k), normal size is
;           3k x 3k
;   w4 - set for W4 (default W3), not yet implemented
;
; OUTPUTS:
;   par - structure containing tile parameters
;
; OPTIONAL OUTPUTS:
;   
; EXAMPLES:
;   
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Aug-15 - Aaron Meisner
;----------------------------------------------------------------------
function tile_par_struc, large=large, w4=w4

; ----- tile sidelength, degrees
  sidelen = 12.5d
; ----- tile sidelength, pixels
  pix = keyword_set(large) ? 8000.d : 3000.d
; ----- pixel scale, asec/pixel
  pscl = keyword_set(large) ? 5.625 : 15.
; ----- central coordinate, lower left = (0,0)
  crpix = keyword_set(large) ? 3999.5d : 1499.5d
; ----- name of index file with tile centers, etc.
  indexfile = '$WISE_DATA/wisetile-index-allsky.fits'

  par = { sidelen   : sidelen,   $ 
          pix       : pix,       $
          crpix     : crpix,     $
          pscl      : pscl,      $
          indexfile : indexfile   }

  return, par

end
