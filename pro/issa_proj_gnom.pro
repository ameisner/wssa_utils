;-----------------------------------------------------------------------
;+
; NAME:
;   issa_proj_gnom
; PURPOSE:
;   Project points from longitude and latitude to a gnomic projection.
;
;   Forward gnomic projection used for the IRAS Sky Survey Atlas.
;   Projection formulae taken from the IRAS Explanatory Supplement,
;   Volume 1, page X-31, with a different scale factor.
;
;   Pass (ra,dec) and the plate center (ra0,dec0) in radians,
;   and the scale factor in pixels/radian.
;
;   For the ISSA 500x500 fields, the scale factor is
;     scale = 40 pixels/degree = 2291.8312 pixels/radian
;   and the returned positions (x,y) are in the range [-249,250].
;
; CALLING SEQUENCE:
;   issa_proj_gnom, ra, dec, ra0, dec0, scale, x, y
;
; INPUTS:
;   ra:         RA in radians
;   dec:        DEC in radians
;   ra0:        Central RA of projection [radians]
;   dec0:       Central DEC of projection [radians]
;   scale:      Scale factor in pixels/radian
;
; OUTPUTS:
;   x:          X position(s) on map in pixel position from center
;   y:          Y position(s) on map in pixel position from center
;
; PROCEDURES CALLED:
;
; REVISION HISTORY:
;   First written by D. Schlegel, Feb 1993, Berkeley in Fortran 77.
;   Modified for IDL by D. Finkbeiner.
;-
;-----------------------------------------------------------------------
pro issa_proj_gnom, ra, dec, ra0, dec0, scale, x, y

   ; Need 7 parameters
   if N_params() LT 7 then begin
      print, 'Syntax - issa_proj_gnom, ra, dec, ra0, dec0, scale, x, y'
      return
   endif

   A = cos(dec) * cos(ra-ra0)
   F = scale / (sin(dec0)*sin(dec) + A*cos(dec0))

   x = -F * cos(dec) * sin(ra-ra0)
   ; Flip the sign on y... (why?)
   y = F*(cos(dec0)*sin(dec) - A*sin(dec0))

   return
end
;-----------------------------------------------------------------------
