import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import illustris_python as il
import physics
import process_snapshot as process

##Parser
"""
parser_rot = argparse.ArgumentParser()
parser_rot.add_argument('-tng', type=str, required=True, help="What TNG-run do you want to process?")
parser_rot.add_argument('-id', type=str, default = "none", help="Test run id. The output will have this id-tag.")
parser_rot.add_argument('-n', '--name', type=str, default = "test", help="Test name. The output will have this name.")
parser_rot.add_argument('-sub', '--subhalo', type=str, default = "0", help="Id of a specific subhalo to rotate.")

args = parser_rot.parse_args()
"""

def create_cat(path):
    df = pd.DataFrame()
    for filename in os.listdir(path):
        temp = pd.read_pickle(path + filename)
        df_temp = pd.concat([df, temp])
        df_temp = df_temp.sort_values(by="id") 
        df = df_temp.reset_index(drop=True)
    return df

def find_most_late(tng_run, test_name):
    new_cat_path = "./data/" + tng_run + "/catalogues/" + test_name + "/"
    group_cat = create_cat(new_cat_path)
    group_cat["SubhaloGasFrac"] = group_cat["SubhaloMassGas"]/group_cat["SubhaloMassStellar"]
    latest_index = group_cat["SubhaloGasFrac"].values.argmax()
    latest_id = group_cat["id"][latest_index]
    rot_vector = np.transpose(np.array([group_cat["AngularMomentumX"][latest_index],
        group_cat["AngularMomentumY"][latest_index],
        group_cat["AngularMomentumZ"][latest_index]]))
    return latest_id, rot_vector

def save_particle_fields(subhalo, index):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    subhalo.to_pickle("./data/tng-100-1/subhalos/subhalo" + str(index) +"_stars.pkl")

def create_projections(subhalo, group_cat, index, test_name):

    fig1, axs1 = plt.subplots(nrows = 1, ncols = 3, figsize=(31,9))
    
    r_half = group_cat[group_cat["id"] == index]["SubhaloHalfmassRadStellar"].values[0]
    theta = np.linspace(0, 2*np.pi, 100)
    x_half = np.cos(theta)*r_half
    y_half = np.sin(theta)*r_half
    x_half_3 = np.cos(theta)*r_half*3
    y_half_3 = np.sin(theta)*r_half*3

    subhalo.plot.scatter("x_rot", "y_rot", color="orange", s=3, alpha=0.5, ax=axs1[0])
    axs1[0].plot(x_half, y_half, '--', label=r'$r_{half}$')
    axs1[0].plot(x_half_3, y_half_3, '-', label=r'$3 r_{half}$')
    
    
    subhalo.plot.scatter("x_rot", "z_rot", color="orange", s=3, alpha = 0.5, ax=axs1[1])
    axs1[1].plot(x_half, y_half, '--', label=r'$r_{half}$')
    axs1[1].plot(x_half_3, y_half_3, '-', label=r'$3 r_{half}$')
    

    subhalo.plot.scatter("y_rot", "z_rot", color="orange", s=3, alpha=0.5, ax=axs1[2])
    axs1[2].plot(x_half, y_half, '--', label=r'$r_{half}$')
    axs1[2].plot(x_half_3, y_half_3, '-', label=r'$3 r_{half}$')

    il.formatplot.rot_galaxy_map(axs1[0], r_half, "x", "y")
    il.formatplot.rot_galaxy_map(axs1[1], r_half, "x", "z")
    il.formatplot.rot_galaxy_map(axs1[2], r_half, "y", "z")

    folder_path = "./fig/projections/" + test_name + "/"
    file_path = "rot_subhalo_" + str(index) + ".png"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    plt.savefig(folder_path + file_path)

def check(tng_run, test_name, snapshot):
    latest_id, rot_vec = find_most_late(tng_run, test_name)
    new_cat_path = "./data/" + tng_run + "/catalogues/test_runs/" + test_name + "/"
    group_cat = create_cat(new_cat_path)
    most_late = process.stars_out(tng_run, snapshot, latest_id)
    most_late = physics.geometry.rotate_coordinates(most_late, rot_vec)
    create_projections(most_late, group_cat, latest_id, test_name)

def subhalo_rotation(tng_run, test_name, snapshot, subhalo_id):
    new_cat_path = "./data/" + tng_run + "/catalogues/" + test_name + ".pkl"
    group_cat = pd.read_pickle(new_cat_path)
    subhalo_index = group_cat[group_cat["id"] == subhalo_id].index.values.astype(int)[0]
    rot_vector = np.transpose(np.array([group_cat["AngularMomentumX"][subhalo_index],
        group_cat["AngularMomentumY"][subhalo_index],
        group_cat["AngularMomentumZ"][subhalo_index]]))
    subhalo = process.stars_out(tng_run, snapshot, subhalo_id)
    subhalo = physics.geometry.rotate_coordinates(subhalo, rot_vector)
    create_projections(subhalo, group_cat, subhalo_id, test_name)
"""
tng_run = args.tng
##Variables
if args.id != "none":
    test_name = args.name + "_" + args.id
else:
    test_name = args.name
"""
tng_run = "tng-100-3"
snapshot = 99
test_name = "kapparot_2602"
subhalo_id = 13332

subhalo_rotation(tng_run, test_name, 99, subhalo_id)
