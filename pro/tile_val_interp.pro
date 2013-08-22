;+
; NAME:
;   tile_val_interp
;
; PURPOSE:
;   use (x,y) pairs and tile numbers to sample values from WSSA tiles
;
; CALLING SEQUENCE:
;   vals = tile_val_interp(tnum, x, y, large=, exten=, tpath=)
;
; INPUTS:
;   tnum - tile number
;   x    - x coordinate
;   y    - y coordinate
;
; OPTIONAL INPUTS:
;   tpath - path to location of WSSA tiles
;   exten - fits extension, default to exten=0, now implemented for
;           single-element exten input
;   release - for now 'dev' or '1.0', 'dev' is default
;
; KEYWORDS:
;   large - not yet implemented
;
; OUTPUTS:
;   vals - values interpolated off of tiles
;
; OPTIONAL OUTPUTS:
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
function tile_val_interp, tnum, x, y, large=large, exten=exten, tpath=tpath, $ 
                          release=release

  if ~keyword_set(exten) then exten = 0
; ----- make sure exten is an integer, do some checks on exten
  exten = string_to_ext(exten, release=release)

  par = tile_par_struc(large=large)
  if ~keyword_set(tpath) then tpath = par.tpath

  nval = n_elements(tnum)
  sind = sort(tnum)
  bdy = uniq(tnum[sind])
; ----- number of unique tiles
  nu = n_elements(bdy)
  fname = concat_dir(tpath, $ 
      'wise_' + string(tnum[sind[bdy]], format='(I03)') + '.fits')

  vals = dblarr(nval) ; can debate float vs. double here later
  for i=0, nu-1 do begin
      indl = (i EQ 0) ? 0 : bdy[i-1] + 1
      indu = bdy[i]
      print, '['+strtrim(string(i+1), 2) + '/' + strtrim(string(nu), 2)+']', $
          ' Reading: ', fname[i],', '+strtrim(string(indu-indl+1),2)+' samples'
      xx = x[sind[indl:indu]]
      yy = y[sind[indl:indu]]
      xoffs = (floor(min(x)) > 0)
      yoffs = (floor(min(y)) > 0)

      xmax = (ceil(max(x)) < (par.pix-1))
      ymax = (ceil(max(y)) < (par.pix-1))

      fxread, fname[i], subim, _, xoffs, xmax, yoffs, ymax, exten=exten

; ----- for bit-masks, round coordinates and quote value, interpolate otherwise
;       clean up conversion to appropriate integer data type later
      if par.ismsk[exten] then $ 
          vals[sind[indl:indu]] = subim[round(xx)-xoffs, round(yy)-yoffs] $
      else $
          vals[sind[indl:indu]] = interpolate(subim, xx-xoffs, yy-yoffs)
  endfor

  return, vals
end
