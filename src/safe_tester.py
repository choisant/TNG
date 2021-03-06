"""
Testing script
Different functions perfomrm different tests.
"""

import os
import pandas as pd
import process_snapshot as process
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

def fifteen_virial(tng_run, test_name, i, snapshot=99):
    """
    Creates and saves group catalogue for subhalo with id i.
    """
    dm_part_mass = set_params(tng_run)

    temp_cat = process.fifteen_virial(tng_run, snapshot, dm_part_mass, i)
    folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    file_path = str(i) + ".pkl"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    temp_cat.to_pickle(folder_path + file_path)

def velocities(tng_run, test_name, i, snapshot=99):
    """
    Creates and saves group catalogue for subhalo with id i.
    """
    dm_part_mass = set_params(tng_run)
    temp_cat = process.velocities(tng_run, snapshot, dm_part_mass, i)
    folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    file_path = str(i) + ".pkl"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    temp_cat.to_pickle(folder_path + file_path)

def veldisp_test(tng_run, test_name, i, snapshot=99):
    """
    Creates and saves group catalogue for subhalo with id i.
    """
    dm_part_mass = set_params(tng_run)
    temp_cat = process.veldisp_test(tng_run, snapshot, dm_part_mass, i)
    folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    file_path = str(i) + ".pkl"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    temp_cat.to_pickle(folder_path + file_path)

def set_aperture_size(tng_run, test_name, i, snapshot=99):
    """
    Creates and saves group catalogue for subhalo with id i.
    """
    dm_part_mass = set_params(tng_run)
    temp_cat = process.set_aperture(tng_run, snapshot, dm_part_mass, i)
    folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    file_path = str(i) + ".pkl"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    temp_cat.to_pickle(folder_path + file_path)

def cleanup (tng_run, test_name):
    def create_cat(path):
        df = pd.DataFrame()
        for filename in os.listdir(path):
            temp = pd.read_pickle(path + filename)
            df_temp = pd.concat([df, temp])
            df_temp = df_temp.sort_values(by="id") 
            df = df_temp.reset_index(drop=True)
        return df
    new_cat_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    new_cat = create_cat(new_cat_path)
    new_cat.to_pickle("./data/" + tng_run + "/catalogues/" + test_name + ".pkl", protocol=4)
