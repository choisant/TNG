import os
import pandas as pd
import cut_data_size as cut
import safe_tester
import physics
import process_snapshot as pros

#import check_rotation as rot

cut.make_pickles("tng-100-1", 99)
#safe_tester.cleanup("tng-100-1", "mass_vel_photo_2303")
#cut.make_central_id_file("tng-100-1", 99)
#cat1 = pros.velocities("tng-100-3", 99, 0.0323567549719664, 29507)
#cat2 = pros.velocities("tng-100-3", 99, 0.0323567549719664, 3403)

#print(cat2)
