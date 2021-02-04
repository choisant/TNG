import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il
import physics
import tng100_test

import os

def create_cat(path):
    df = pd.DataFrame()
    for filename in os.listdir(path):
        temp = pd.read_pickle(path + filename)
        df_temp = pd.concat([df, temp])
        df_temp = df_temp.sort_values(by="id") 
        df = df_temp.reset_index(drop=True)
    return df

def find_most_late(tng_run, test_name):
    new_cat_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    group_cat = create_cat(new_cat_path)
    group_cat["SubhaloGasFrac"] = group_cat["SubhaloMassGas"]/group_cat["SubhaloMassTotal"]
    latest_index = group_cat["SubhaloGasFrac"].argmin()
    latest_id = group_cat["id"][latest_index]
    rot_vector = np.transpose(np.array([group_cat["RotationAxisX"][latest_index],
        group_cat["RotationAxisY"][latest_index],
        group_cat["RotationAxisZ"][latest_index]]))
    return latest_id, rot_vector

def save_particle_fields(subhalo, index):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    subhalo.to_pickle("./data/tng-100-1/subhalos/subhalo" + str(index) +"_stars.pkl")

def create_projections(subhalo, index, test_name):

    fig1, axs1 = plt.subplots(nrows = 1, ncols = 3, figsize=(28,8))

    subhalo.plot.scatter("x_rot", "y_rot", color="orange", s=3, alpha=0.5, ax=axs1[0])
    axs1[0].set_xlabel('x_rot [ckpc/h]')
    axs1[0].set_ylabel('y_rot [ckpc/h]')
    
    subhalo.plot.scatter("x_rot", "z_rot", color="orange", s=3, alpha = 0.5, ax=axs1[1])
    axs1[1].set_xlabel('x_rot [ckpc/h]')
    axs1[1].set_ylabel('z_rot [ckpc/h]')

    subhalo.plot.scatter("y_rot", "z_rot", color="orange", s=3, alpha=0.5, ax=axs1[2])
    axs1[2].set_xlabel('y_rot [ckpc/h]')
    axs1[2].set_ylabel('z_rot [ckpc/h]')

    plt.savefig("./fig/projections/" + test_name + "_rot_subhalo_" + str(index) + "_xy.png")
   
    fig2, axs2 = plt.subplots(nrows = 1, ncols = 3, figsize=(28,8))

    subhalo.plot.scatter("x", "y", color = "orange", s=3, alpha=0.5, ax=axs2[0])
    axs2[0].set_xlabel('x [ckpc/h]')
    axs2[0].set_ylabel('y [ckpc/h]')
    
    subhalo.plot.scatter("x", "z", color = "orange", s=3, alpha=0.5, ax=axs2[1])
    axs2[1].set_xlabel('x [ckpc/h]')
    axs2[1].set_ylabel('z [ckpc/h]')

    subhalo.plot.scatter("y", "z", color = "orange", s=3, alpha = 0.5, ax = axs2[2])
    axs2[2].set_xlabel('y [ckpc/h]')
    axs2[2].set_ylabel('z [ckpc/h]')

    plt.savefig("./fig/projections/" + test_name + "_subhalo_" + str(index) + "_xy.png")


def check(tng_run, test_name, snapshot):
    latest_id, rot_vec = find_most_late(tng_run, test_name)
    print(rot_vec)
    most_late = tng100_test.basic_properties_stars(tng_run, snapshot, [latest_id], stars_out=True)
    most_late = physics.geometry.rotate_coordinates(most_late, 1, [rot_vec])
    create_projections(most_late[0], latest_id, test_name)
