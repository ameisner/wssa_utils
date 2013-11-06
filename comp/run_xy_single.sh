echo -e .COM comp "\n" test_xy_single, \"coords_i.fits\" |idl &> rxysi.log
echo -e import comp "\n"comp.test_xy_single\(\"coords_p.fits\"\) |python &> rxysp.log
echo -e .COM comp "\n" compare_xy_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl &> rxys.log
