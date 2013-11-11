echo -e .COM comp "\n" test_xy_many, \"coords_i.fits\" |idl &> rxymi.log
echo -e import comp "\n"comp.test_xy_many\(\"coords_p.fits\"\) |python &> rxymp.log
echo -e .COM comp "\n" compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl &> rxym.log
