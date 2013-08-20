;+
; NAME:
;   init_tile_index

; PURPOSE:
;   create common block storing information about ISSA tile centers
;
; CALLING SEQUENCE:
;   init_tile_index
;
; EXAMPLES:
;
; COMMENTS:
;
; REVISION HISTORY:
;   2013-Aug-15 - Aaron Meisner
;----------------------------------------------------------------------
pro init_tile_index

  COMMON TILES, tilenum, ra, dec, lgal, bgal, name
  if n_elements(tilenum) EQ 0 then begin
      par = tile_par_struc()
      fname = par.indexfile
      tstr = mrdfits(fname, 1)
      ra = tstr.ra
      dec = tstr.dec
      lgal = tstr.lgal
      bgal = tstr.bgal
      name = tstr.fname
      tilenum = fix(strmid(name, 5, 3))
  endif

end
