echo -e import comp "\n"comp.test_xy_heal\(\"coords_p.fits\", nside=256\) |python &> rxyh.log
echo -e .COM comp "\n" test_xy_heal, \"coords_i.fits\", nside=256 \& compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl >> rxyh.log 2>&1
