;+
; NAME:
;   init_pixel_lookup
;
; PURPOSE:
;   store common block containing lookup between HEALPix pixel and tile
;
; CALLING SEQUENCE:
;   init_pixel_lookup, read=
;
; KEYWORDS:
;   read - set to read in look-up table instead of generating it on the fly
;
; EXAMPLES:
;   see coord_to_tile.pro
;
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Aug-18 - Aaron Meisner
;----------------------------------------------------------------------
pro init_pixel_lookup, read=read

  COMMON PIXTILE, pix, tile, nside
  if n_elements(tile) EQ 0 then begin
; ----- eventually read from a file instead of computing on the fly
      nside = 64
      if keyword_set(read) then begin
          str = mrdfits('$WISE_DATA/pixel_lookup.fits', 1)
          tile = str.tile
      endif else begin
          pixel_to_tile, tile, nside=64
      endelse
      pix = lindgen(12L*nside*nside)
  endif

end
