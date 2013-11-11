echo -e .COM comp "\n" test_xy_single, \"coords_i.fits\" |idl &> rxys.log
echo -e import comp "\n"comp.test_xy_single\(\"coords_p.fits\"\) |python >> rxys.log 2>&1
echo -e .COM comp "\n" compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl >> rxys.log 2>&1
