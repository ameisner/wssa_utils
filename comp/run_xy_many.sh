echo -e .COM comp "\n" test_xy_many, \"coords_i.fits\" |idl &> rxym.log
echo -e import comp "\n"comp.test_xy_many\(\"coords_p.fits\"\) |python >> rxym.log 2>&1
echo -e .COM comp "\n" compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl >> rxym.log 2>&1
