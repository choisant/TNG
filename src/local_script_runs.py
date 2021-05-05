import os
import pandas as pd
import cut_data_size as cut
import safe_tester
import physics
import process_snapshot as pros

#import check_rotation as rot

#cut.make_pickles("tng-100-1", 99)
#safe_tester.cleanup("tng-100-1", "velocities_0405")
#cut.make_central_id_file("tng-100-1", 99)
cat1 = pros.velocities("tng-100-3", 99, 0.0323567549719664, 9839)
#cat2 = pros.velocities("tng-100-3", 99, 0.0323567549719664, 3403)
print(cat1.keys())
#print(cat1["SubhaloHalfmassRadStellarTotal"])
#print(cat1["SubhaloHalfmassRad_xyTotal"])
print(cat1["SubhaloVelDisp3D_DM_Total"][0])
print(cat1["SubhaloVelDisp3D_Gas_Re_Total"][0])
print(cat1["SubhaloVelDisp3D_Gas_Re_30kpc"][0])
print(cat1["SubhaloVelDisp3D_Gas_Re_15Rvir"][0])
print(cat1["SubhaloHalfmassRad_xy30kpc"][0])
#print(cat1["SubhaloHalfmassRadStellar10kpc"][0])



