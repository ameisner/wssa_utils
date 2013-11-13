echo -e import comp "\n"comp.test_vals_float\(\"vals_p.fits\"\) |python &> rvfs.log
echo -e .COM comp "\n" test_vals_float, \"vals_i.fits\" \& compare_outputs, \"vals_p.fits\", \"vals_i.fits\" |idl >> rvfs.log 2>&1
