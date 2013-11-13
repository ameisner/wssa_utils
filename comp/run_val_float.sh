echo -e import comp "\n"comp.test_val_float\(\"val_p.fits\"\) |python &> rvf.log
echo -e .COM comp "\n" test_val_float, \"val_i.fits\" \& compare_outputs, \"val_p.fits\", \"val_i.fits\" |idl >> rvf.log 2>&1
