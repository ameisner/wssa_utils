;+
; NAME:
;   assert
;
; PURPOSE:
;   evaluate predicate at run-time, stop program execution if false
;
; CALLING SEQUENCE:
;   assert, p
;
; INPUTS:
;   p - true = 1, false = 0
;
; OPTIONAL INPUTS:
;   
; KEYWORDS:
;   
; OUTPUTS:
;   stops program execution with 'assertion failed' message if p = 0
;   or p is of unexpected nature
;
; OPTIONAL OUTPUTS:
;   
; EXAMPLES:
;   
; COMMENTS:
;   
; REVISION HISTORY:
;   2013-Nov-5 - Aaron Meisner
;----------------------------------------------------------------------
pro assert, p

  if n_elements(p) NE 1  then message, 'improper assertion'

; ----- type byte
  if size(p, /type) NE 1 then message, 'improper assertion'

  if (p NE 1) then message, 'assertion failed'

end
