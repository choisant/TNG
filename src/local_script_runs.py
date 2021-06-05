import os
import pandas as pd
import cut_data_size as cut
import safe_tester
import physics
import process_snapshot as pros
import matplotlib.pyplot as plt

#import check_rotation as rot

#cut.make_pickles("tng-100-1", 99)
safe_tester.cleanup("tng-100-1", "veldisp_mw")
#cut.make_central_id_file("tng-100-1", 99)
#cat1 = pros.veldisp_test("tng-100-3", 99, 0.0323567549719664, 9839)
#cat2 = pros.velocities("tng-100-3", 99, 0.0323567549719664, 3403)
#print(cat1["SubhaloVelDisp3D_Stellar_Re_Total_MW"])

#cat = pd.read_pickle("./data/tng-100-1/catalogues/veldisp_mw.pkl")
#cat.to_csv("./data/tng-100-1/catalogues/veldisp_mw.csv")
#cat["p"] = 100*cat["SubhaloVelDisp3D_Stellar_Total_MW"]/cat["SubhaloVelDisp3D_Stellar_Total"]
#cat.plot.scatter("SubhaloMassStellarTotal", "SubhaloVelDisp3D_Stellar_Total_MW")
#plt.show()
