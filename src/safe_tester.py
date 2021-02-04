"""
Testing script
Different functions perfomrm different tests.
"""

import os
from os import path
import numpy as np
import pandas as pd
import tng100_test as test
import cut_data_size
from timeit import default_timer as timer
import datetime
import check_rotation as rot

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

def simple_test_last_ten(tng_run, test_name, snapshot=99):
    """
    Creates and saves group catalogue for the last ten galaxies in the central galaxies sample.
    """
    #Start timer
    start = timer()
    dm_part_mass = set_params(tng_run)
    print("Getting indices")
    if path.exists("./data/" + tng_run + "/cutdata/central_id.txt"):
        indices = np.genfromtxt("./data/" + tng_run + "/cutdata/central_id.txt", int)
    else:
        print("No list of central galaxy indices exists. Trying to create file ...")
        find_centrals(tng_run, snapshot)
        indices = np.genfromtxt("./data/" + tng_run + "/cutdata/central_id.txt", int)

    index_list = indices[-10:] #Get last ten subhalos
    print("Starting test")
    temp_cat = test.basic_properties_stars(tng_run, snapshot, indices = index_list, stars_out = False)
    print(temp_cat[0])
    print("Saving results")
    temp_cat.to_pickle("./data/" + tng_run + "/catalogues/last_ten_" + test_name + ".pkl")
    #End timer
    end = timer()
    print("Time to process ")
    print(datetime.timedelta(seconds =int(end - start)), "h:m:s")



def simple_test_all(tng_run, test_name, snapshot=99):
    """
    Creates and saves group catalogues for all central galaxies.
    If process is aborted, data is still saved up until that point.
    """
    #Start timer
    start = timer()
    percent = 0
    dm_part_mass = set_params(tng_run)
    if path.exists("./data/" + tng_run + "/cutdata/central_id.txt"):
        indices = np.genfromtxt("./data/" + tng_run + "/cutdata/central_id.txt", int)
    else:
        print("No list of central galaxy indices exists. Trying to create file ...")
        find_centrals(tng_run, snapshot)
        indices = np.genfromtxt("./data/" + tng_run + "/cutdata/central_id.txt", int)

    index_lists = np.array_split(indices, len(indices)/4) #split into chunks of length 4
    for id_chunks in index_lists:
        print(int(percent), " percent of data processed")
        temp_cat = test.basic_properties_stars(tng_run, snapshot, indices = id_chunks, stars_out = False)
        folder_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
        file_path = str(id_chunks[0]) + "-" + str(id_chunks[-1]) + ".pkl"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        temp_cat = test.masses(tng_run, snapshot, dm_part_mass, id_chunks, temp_cat)
        temp_cat.to_pickle(folder_path + file_path)
        percent = percent + 4*100/(len(indices))
    #End timer
    end = timer()
    print("Time to process:")
    print(datetime.timedelta(seconds=int(end - start)), "h:m:s")

def rotation_test(tng_run, test_name, snapshot=99):
    rot.check(tng_run, test_name, snapshot)