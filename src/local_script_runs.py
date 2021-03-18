import os
import pandas as pd
import cut_data_size as cut
import safe_tester
import physics

#import check_rotation as rot

#cut.make_pickles("tng-100-3", 99)
#safe_tester.cleanup("tng-100-1", "veldisp_1803")
cut.make_central_id_file("tng-100-1", 99)