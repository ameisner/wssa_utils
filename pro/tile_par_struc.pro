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
; OPTIONAL INPUTS:
;   release - release string, should be either 'dev' or '1.0'
;
; KEYWORDS:
;   large - set for large version of tiles (8k x 8k), default size is
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
function tile_par_struc, large=large, w4=w4, release=release

  if ~keyword_set(release) then release = 'dev'
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
; ----- extension names, clean this up later, for now useful to see list
  if (release EQ 'dev') then $ 
      extens = ['clean', $ 
                'dirt',  $ 
                'cov',   $ 
                'sfd',   $
                'min',   $ 
                'max',   $
                'amsk',  $ 
                'omsk',  $ 
                'art'     ] $
  else $
      extens = ['clean', $ 
                'dirt',  $ 
                'cov',   $ 
                'min',   $ 
                'max',   $
                'amsk',  $ 
                'omsk',  $ 
                'art'     ]
; ----- boolean indicating whether each extension should be treated as a
;       bit-mask, 0=not mask, 1=mask (what about coverage??)
  ismsk = strpos(extens, 'msk') GT 0
; ----- number of tiles, don't want random 430's all over my code
  ntile = 430
; ----- default tile path
  tpath = getenv('WISE_TILE')
; ----- conversion from factor from W3 DN to MJy/sr
  calfac = 0.0163402d

  par = { sidelen   : sidelen,   $ 
          pix       : pix,       $
          crpix     : crpix,     $
          pscl      : pscl,      $
          indexfile : indexfile, $
          extens    : extens,    $
          ismsk     : ismsk,     $
          ntile     : ntile,     $
          tpath     : tpath,     $ 
          calfac    : calfac      }

  return, par

end
