echo -e .COM comp "\n" test_xy_rect, \"coords_i.fits\" |idl &> rxyr.log
echo -e import comp "\n"comp.test_xy_rect\(\"coords_p.fits\"\) |python >> rxyr.log 2>&1
echo -e .COM comp "\n" compare_outputs, \"coords_p.fits\", \"coords_i.fits\" |idl >> rxyr.log 2>&1
