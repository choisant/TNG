import os
import pandas as pd
import tng100_test as test
import cut_data_size as cut
import safe_tester
#import check_rotation as rot

#safe_tester.test_all("tng-100-3", "kinematics_1802", 1893, 99)
#cut.make_pickles("tng-100-3", 99)
safe_tester.cleanup("tng-100-1", "idun_1802")
