;+
; NAME:
;   coord_to_tile
;
; PURPOSE:
;   use HEALPix lookup table to match (ra,dec) coordinates with WSSA tiles
;
; CALLING SEQUENCE:
;   coord_to_tile, ra, dec, tnum, x=x, y=y, large=large
;
; INPUTS:
;   ra - list of RA coordinates, assumed deg J2000
;   dec - list of DEC coordinates, assumed deg J2000
;
; KEYWORDS:
;   large - set for 8k x 8k tile astrometry, default 3k x 3k, only
;           matters if (x, y) coords desired
;
; OUTPUTS:
;   tnum - tile number corresponding to each (ra, dec) pair
;
; OPTIONAL OUTPUTS:
;   x - x coordinate within tile tnum for each (ra, dec) pair
;   y - y coordinate within tile tnum for each (ra, dec) pair
;
; EXAMPLES:
;    coord_to_tile, ra, dec, tnum, x=x, y=y
;    tile_val_interp, tnum, x, y
;
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Aug-18 - Aaron Meisner
;----------------------------------------------------------------------
pro coord_to_tile, ra, dec, tnum, x=x, y=y, large=large

; ----- load pixel -> tile lookup table
  init_pixel_lookup, /read
  COMMON PIXTILE, plist, tlist, nside

; ----- convert to HEALPix
  radeg = 180.d/!dpi
  ang2pix_ring, nside, (90.d - dec)/radeg, ra/radeg, pix
  tnum = tlist[pix]
  delvarx, pix ; don't waste RAM

; ----- if requested, convert to (x,y) within tile
  if arg_present(x) then begin
      init_tile_index
      COMMON TILES, _, ra0, dec0, __, ___, ____
      par = tile_par_struc(large=large)
      scale = (par.pix/par.sidelen)*radeg
      issa_proj_gnom, ra/radeg, dec/radeg, $ 
          ra0[tnum-1]/radeg, dec0[tnum-1]/radeg, scale, dx, dy
      x = dx + par.crpix
      y = dy + par.crpix
  endif

end
