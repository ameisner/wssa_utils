echo -e import comp "\n"comp.test_xy_rect\(\"coords_p.fits\"\) |python &> rxyr.log
echo -e .COM comp "\n" test_xy_rect, \"coords_i.fits\" \& compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl >> rxyr.log 2>&1
tot=`wc -l < rxyr.log`
sta=`sed -n '/checking/=' rxyr.log |head -1`
nta=$(( ${tot}-${sta}+1 ))
tail -$nta rxyr.log