;+
; NAME:
;   string_to_ext
;
; PURPOSE:
;   convert string extension name to integer extension number
;
; CALLING SEQUENCE:
;   exten = string_to_ext(ext, release=)
;
; INPUTS:
;   ext - string or integer for desired extension
;
; OPTIONAL INPUTS:
;   release - data release, because order and number of extensions may depend
;             on tile release version
;
; OUTPUTS:
;   exten - integer extension number (zero-indexed), suitable for use with
;           exten keyword in e.g. fxread
;
; EXAMPLES:
;   see tile_val_interp.pro
;
; COMMENTS:
;   also does some really minimal error checking, will be more
;   thorough with error checking later
;
;   will generalize to handle lists of extensions later
;
; REVISION HISTORY:
;   2013-Aug-20 - Aaron Meisner
;----------------------------------------------------------------------
function string_to_ext, ext, release=release

  par = tile_par_struc(release=release)
; ----- for now assume ext to be a single string or integer, generalize
;       later to allow an array of strings or integers
; ----- don't modify input variable ext
  if size(ext, /TYPE) EQ 7 then exten = where(par.extens EQ ext) $ 
      else exten = ext

; ----- very crude error checking, clean this up later
  if (exten LT 0) OR (exten GE n_elements(par.extens)) then begin
      print, 'Acceptable tile extensions are:'
      for i=0, n_elements(par.extens)-1 do begin
          print, strtrim(string(i), 2)+': '+par.extens[i]
      endfor
      stop
  endif

  return, exten
end
