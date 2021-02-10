import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import illustris_python as il
import physics

def load(tng_run, snapshot, i):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    print("Loading stellar particles")

    print("Subhalo ", i, " ", timer())
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))
    print(timer())
    return group_cat

def angular_momentum(tng_run, snapshot, i, stars_out=False):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    print("Loading stellar particles")

    print("Subhalo ", i)
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))

    group_cat = physics.properties.group_properties(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, group_cat)
    stars = physics.properties.relative_pos_radius(stars, group_cat)
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    group_cat = physics.properties.total_stellar_mass(stars, group_cat)
    stars, group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    group_cat = physics.properties.half_mass_radius(stars, group_cat)
    group_cat = physics.properties.max_ang_momentum(stars, group_cat)

    if stars_out:
        return stars
    
    return group_cat

def mass_vel_photo(tng_run, snapshot, dm_mass, i):
     #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities", "GFM_StellarPhotometrics"],
        "gas": ["Coordinates", "Masses"],
        "dm": ["Coordinates", "Potential"]
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    print("Loading particles")
    print("Subhalo ", i)
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))
    gas = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'gas', fields["gas"]))
    dm = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'dm', fields["dm"]))
    dm["Masses"] = dm_mass
    #Get total mass, position, radius and change coordinates
    group_cat = physics.properties.group_properties(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, group_cat)
    stars = physics.properties.relative_pos_radius(stars, group_cat)
    gas = physics.properties.relative_pos_radius(gas, group_cat)
    dm = physics.properties.relative_pos_radius(dm, group_cat)
    #Reduce data size
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    gas = gas[gas["r"] < max_rad]
    dm = dm[dm["r"] < max_rad]
    #Calculate 
    group_cat = physics.properties.total_stellar_mass(stars, group_cat)
    group_cat = physics.properties.rotational_vel(gas, dm, stars, group_cat)
    group_cat = physics.properties.velocity_disp(stars, group_cat)

    return group_cat


def masses(tng_run, snapshot, dm_mass, i, catalogue):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
        "gas": ["Coordinates", "Masses"],
        "dm": ["Coordinates", "Potential"]
        }

    #Load all particles

    df = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'gas', fields["gas"]))
    df = physics.properties.relative_pos_radius(df, catalogue)
    max_rad = catalogue["SubhaloGalaxyRad"][0]
    df = df[df["r"] < max_rad]
    catalogue["SubhaloMassGas"] = df["Masses"].sum()

    df = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'dm', fields["dm"]))
    df["Masses"] = dm_mass
    df = physics.properties.relative_pos_radius(df, catalogue)
    max_rad = catalogue["SubhaloGalaxyRad"][0]
    df = df[df["r"] < max_rad]
    catalogue["SubhaloMassDM"] = df["Masses"].sum()
    catalogue["SubhaloMassTotal"] = catalogue["SubhaloMassDM"] + catalogue["SubhaloMassGas"] + catalogue["SubhaloMassStellar"]
        
    return catalogue

#def kinematics(tng_run, snapshot, i, catalogue):


def save_particle_fields(particle, indices):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    g = 0
    particle[g].to_pickle("./data/tng-100-1/subhalos/subhalo" + str(indices[g]) +"_stars.pkl")
    