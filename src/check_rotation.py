import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import physics
import tng100_test

##Parser

parser_rot = argparse.ArgumentParser()
parser_rot.add_argument('-tng', type=str, required=True, help="What TNG-run do you want to process?")
parser_rot.add_argument('-id', type=str, default = "none", help="Test run id. The output will have this id-tag.")
parser_rot.add_argument('-n', '--name', type=str, default = "test", help="Test name. The output will have this name.")
parser_rot.add_argument('-sub', '--subhalo', type=str, default = "0", help="Id of a specific subhalo to rotate.")

args = parser_rot.parse_args()


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
    latest_index = group_cat["SubhaloGasFrac"].values.argmax()
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
    most_late = tng100_test.basic_properties_stars(tng_run, snapshot, latest_id, stars_out=True)
    most_late = physics.geometry.rotate_coordinates(most_late, rot_vec)
    create_projections(most_late, latest_id, test_name)

def subhalo(tng_run, test_name, snapshot, subhalo_id):
    new_cat_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    group_cat = create_cat(new_cat_path)
    subhalo_index = group_cat[group_cat["id"] == subhalo_id].index.values.astype(int)[0]
    rot_vector = np.transpose(np.array([group_cat["RotationAxisX"][subhalo_index],
        group_cat["RotationAxisY"][subhalo_index],
        group_cat["RotationAxisZ"][subhalo_index]]))
    subhalo = tng100_test.basic_properties_stars(tng_run, snapshot, subhalo_id, stars_out=True)
    subhalo = physics.geometry.rotate_coordinates(subhalo, rot_vector)
    create_projections(subhalo, subhalo_id, test_name)

tng_run = args.tng
##Variables
if args.id != "none":
    test_name = args.name + "_" + args.id
else:
    test_name = args.name

if args.subhalo == "0":
    check(tng_run, test_name, 99)
else:
    subhalo(tng_run, test_name, 99, int(args.subhalo))