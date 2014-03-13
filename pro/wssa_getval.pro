;+
; NAME:
;   wssa_getval
;
; PURPOSE:
;   return WSSA tile values sampled at list of input sky locations
;
; CALLING SEQUENCE:
;   vals = wssa_getval(ra, dec)
;
; INPUTS:
;   ra - input list of RA values, assumed J2000
;   dec - input list of DEC values, assumed J2000
;
; OPTIONAL INPUTS:
;   exten - extension, either as an integer or string, acceptable values
;           for release='1.0':
;                0: 'clean'
;                1: 'dirt'
;                2: 'cov'
;                3: 'min'
;                4: 'max'
;                5: 'amsk'
;                6: 'omsk'
;                7: 'art'
;   akari - set to either 'WideS' or 'WideL' to read Akari tiles
;
; KEYWORDS:
;   tilepath - directory containing WSSA tile fits files
;   release  - default '1.0', currently only release = '1.0' is supported
;   large - large = 1 for 8k x 8k tiles, large = 1 is now default,
;           specify large = 0 for 3k x 3k
;   mjysr - set for result in MJy/sr, default is W3 DN
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
function wssa_getval, ra, dec, exten=exten, tilepath=tilepath, $
                      release=release, large=large, mjysr=mjysr, gz=gz, $ 
                      akari=akari

  sane = check_coords(ra, dec)
  if ~sane then return, -1

  if keyword_set(akari) && (akari NE 'WideS') && (akari NE 'WideL') then $ 
      return, -1

  if ~keyword_set(exten) OR keyword_set(akari) then exten = 0
; ----- make large = 1 (8k x 8k tiles) default for WISE, 
;            large = 0 (3k x 3k tiles) default for Akari
  if n_elements(large) EQ 0 then large = (keyword_set(akari) ? 0 : 1)
; ----- dummy value for Akari release
  if ~keyword_set(release) then release = (keyword_set(akari) ? '' : '1.0')

  exten = string_to_ext(exten, release=release)

  ra = double(ra)
  dec = double(dec)

  coord_to_tile, ra, dec, tnum, x=x, y=y, large=large
  vals = tile_val_interp(tnum, x, y, exten=exten, tpath=tilepath, $ 
      release=release, large=large, gz=gz, akari=akari)

  if n_elements(vals) GT 1 then vals = reform(vals, size(ra, /dim))

  par = tile_par_struc(release=release, large=large)
  mask = (keyword_set(akari) ? 0 : (par.ismsk)[exten])

  if mask then vals = long(vals)
  if keyword_set(mjysr) AND (~mask) AND ~keyword_set(akari) then $ 
      vals *= float(par.calfac)

  return, vals

end
