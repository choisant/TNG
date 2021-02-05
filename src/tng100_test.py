import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import illustris_python as il
import physics


def basic_properties_stars_old(tng_run, snapshot, indices, stars_out=False):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            }
    N = len(indices)
    stars = [0]*N
    group_cat = pd.DataFrame({"id": indices})
    #Start timer
    start = timer()

    #Load all particles
    print("Loading stellar particles")
    for i in range(N):
        print("Subhalo ", indices[i])
        stars[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'stars', fields["stars"]))
        if indices[i] < 152031:
            stars[i].info(verbose=False)
    group_cat = physics.properties.galaxy_radius(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, N, group_cat)
    stars = physics.properties.relative_pos_radius(stars, N, group_cat)
    for i in range(N):
        max_rad = group_cat["SubhaloGalaxyRad"][i]
        stars[i] = stars[i][stars[i]["r"] < max_rad]
    group_cat = physics.properties.total_mass(stars, N, group_cat)
    #stars, group_cat = physics.properties.subhalo_velocity(stars, N, group_cat)
    stars = physics.properties.relative_velocities(stars, N, group_cat)
    group_cat = physics.properties.half_mass_radius(stars, N, group_cat, "Stellar")
    group_cat = physics.properties.max_ang_momentum(stars, N, group_cat)
    
    #End timer
    end = timer()
    print("Time to process " + str(N) + " Subhalos: ")
    print(int(end - start), "Seconds")

    if stars_out:
        return stars
    
    return group_cat

def masses_old(tng_run, snapshot, dm_mass, indices, catalogue):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
        "gas": ["Coordinates", "Masses"],
        "dm": ["Coordinates", "Potential"]
        }
    N = len(indices)
    #Load all particles
    gas_masses = np.zeros(N)
    dm_masses = np.zeros(N)
    for i in range(N):
        df = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'gas', fields["gas"]))
        df = physics.properties.relative_pos_radius([df], 1, catalogue)[0]
        max_rad = catalogue["SubhaloGalaxyRad"][i]
        df = df[df["r"] < max_rad]
        gas_masses[i] = df["Masses"].sum()

        df = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'dm', fields["dm"]))
        df["Masses"] = dm_mass
        df = physics.properties.relative_pos_radius([df], 1, catalogue)[0]
        print("Deleting particles outside galaxy radius")
        max_rad = catalogue["SubhaloGalaxyRad"][i]
        df = df[df["r"] < max_rad]
        dm_masses[i] = df["Masses"].sum()
    
    catalogue["SubhaloMassGas"] = gas_masses.sum()
    catalogue["SubhaloMassDm"] = dm_masses.sum()
    catalogue["SubhaloMassTotal"] = catalogue["SubhaloMassDm"] + catalogue["SubhaloMassGas"] + catalogue["SubhaloMassStellar"]
        
    return catalogue

def basic_properties_stars(tng_run, snapshot, i, stars_out=False):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            }
    group_cat = pd.DataFrame({"id": [i]})
    N = 1
    #Load particles
    print("Loading stellar particles")

    print("Subhalo ", i)
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))

    group_cat = physics.properties.galaxy_radius(group_cat, base_path)
    group_cat = physics.properties.center_halo([stars], N, group_cat)
    stars = physics.properties.relative_pos_radius([stars], N, group_cat)[0]
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    group_cat = physics.properties.total_mass([stars], N, group_cat)
    stars, group_cat = physics.properties.subhalo_velocity_one(stars, group_cat)
    #from here stars is a list of one element
    stars = physics.properties.relative_velocities([stars], N, group_cat)
    group_cat = physics.properties.half_mass_radius(stars, N, group_cat, "Stellar")
    group_cat = physics.properties.max_ang_momentum(stars, N, group_cat)

    if stars_out:
        return stars[0]
    
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
    df = physics.properties.relative_pos_radius([df], 1, catalogue)[0]
    max_rad = catalogue["SubhaloGalaxyRad"][0]
    df = df[df["r"] < max_rad]
    catalogue["SubhaloMassGas"] = df["Masses"].sum()

    df = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'dm', fields["dm"]))
    df["Masses"] = dm_mass
    df = physics.properties.relative_pos_radius([df], 1, catalogue)[0]
    max_rad = catalogue["SubhaloGalaxyRad"][0]
    df = df[df["r"] < max_rad]
    catalogue["SubhaloMassDm"] = df["Masses"].sum()
    catalogue["SubhaloMassTotal"] = catalogue["SubhaloMassDm"] + catalogue["SubhaloMassGas"] + catalogue["SubhaloMassStellar"]
        
    return catalogue

def save_particle_fields(particle, indices):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    g = 0
    particle[g].to_pickle("./data/tng-100-1/subhalos/subhalo" + str(indices[g]) +"_stars.pkl")
    