echo -e .COM comp "\n" test_vals_rect, \"vals_i.fits\" |idl &> rvr.log
echo -e import comp "\n"comp.test_vals_rect\(\"vals_p.fits\"\) |python >> rvr.log 2>&1
echo -e .COM comp "\n" compare_outputs, \"vals_p.fits\", \"vals_i.fits\" |idl >> rvr.log 2>&1
