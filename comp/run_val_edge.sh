echo -e import comp "\n"comp.test_edge_interp\(\"val_p.fits\"\) |python &> rve.log
echo -e .COM comp "\n" test_edge_interp, \"val_i.fits\" \& compare_outputs, \"val_p.fits\", \"val_i.fits\" |idl >> rve.log 2>&1
