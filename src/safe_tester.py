"""
Testing script
Different functions perfomrm different tests.
"""

import os
import tng100_test as test
import cut_data_size

def set_params(tng_run):
    """
    Sets the parameters needed to rund the tests.
    """
    if tng_run == "tng-100-1":
        dm_part_mass = 0.000505574296436975
    elif tng_run == "tng-100-3":
        dm_part_mass = 0.0323567549719664
    else:
        print("Not an available run.")
    return dm_part_mass

def find_centrals(tng_run, snapshot=99):
    """
    Finds the central galaxies in the snapshot and saves their indices in a file.
    """
    cut_data_size.make_central_id_file(tng_run, snapshot)

def simple_test_all(tng_run, test_name, i, snapshot=99):
    """
    Creates and saves group catalogues for all central galaxies.
    If process is aborted, data is still saved up until that point.
    """
    dm_part_mass = set_params(tng_run)

    temp_cat = test.basic_properties_stars(tng_run, snapshot, i, stars_out = False)
    folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    file_path = str(i) + ".pkl"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    temp_cat = test.masses(tng_run, snapshot, dm_part_mass, i, temp_cat)
    temp_cat.to_pickle(folder_path + file_path)
