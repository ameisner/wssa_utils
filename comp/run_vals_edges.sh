echo -e import comp "\n"comp.test_edge_interp\(\"vals_p.fits\"\) |python &> rve.log
echo -e .COM comp "\n" test_edge_interp, \"vals_i.fits\" \& compare_outputs, \"vals_p.fits\", \"vals_i.fits\" |idl >> rve.log 2>&1
