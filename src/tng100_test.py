import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import illustris_python as il
import physics


def basic_properties(tng_run, snapshot, indices, dm_particle_mass):
    #intitial setup
    basePath = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            "gas": ["Coordinates", "Potential", "Masses", "Velocities"],
            "dm": ["Coordinates", "Potential", "Velocities"]
            }

    N = len(indices)
    stars = [0]*N
    gas = [0]*N
    dm = [0]*N
    particle_lists = [gas, dm, stars]
    group_cat = pd.DataFrame({"id": indices})
    #Start timer
    start = timer()

    #Load all particles
    print("Loading all particles")
    for i in range(N):
        print("Subhalo ", indices[i])
        stars[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, snapshot, indices[i], 'stars', fields["stars"]))
        #gas[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, snapshot, indices[i], 'gas', fields["gas"]))
        #dm[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, snapshot, indices[i], 'dm', fields["dm"]))
        #dm[i]["Masses"] = [dm_particle_mass]*len(dm[i]["Potential"]) #Add dm masses

    print("Finding galaxy radius")
    group_cat = physics.properties.galaxy_radius(group_cat, basePath)
    print("Finding center of galaxy")
    group_cat = physics.properties.center_halo(stars, N, group_cat)
    print("Calculating new coordinates and radius")
    #for particle in particle_lists:
        #particle = physics.properties.relative_pos_radius(particle, N, group_cat)
    stars = physics.properties.relative_pos_radius(stars, N, group_cat)
    print("Deleting particles outside galaxy radius")
    for i in range(N):
        max_rad = group_cat["SubhaloGalaxyRad"][i]
        stars[i] = stars[i][stars[i]["r"] < max_rad]
        #for particle in particle_lists:
            #particle[i] = particle[i][particle[i]["r"] < max_rad]

    print("Calculating particle masses")
    group_cat["SubhaloMassStellar"] = np.zeros(N)
    for i in range(N):
        group_cat["SubhaloMassStellar"] = stars[i]["Masses"].sum()
    #particle_lists, group_cat = physics.properties.total_mass(particle_lists, N, group_cat)
    print("Calculating subhalo velocity")
    stars, group_cat = physics.properties.subhalo_velocity(stars, N, group_cat)
    print("Calculating relative velocities")
    stars = physics.properties.relative_velocities(stars, N, group_cat)
    print("Calculating half mass radius")
    group_cat = physics.properties.half_mass_radius(stars, N, group_cat, "Stellar")
    #print("Calculating maximum angular momentum")
    #group_cat = physics.properties.max_ang_momentum(stars, N, group_cat)
    #End timer
    end = timer()
    print("Time to process " + str(N) + " Subhalos: ")
    print(int(end - start), "Seconds")

    return group_cat

def rotate(particle_lists, N, group_cat, rot_vector):
    print("Rotating subhalos")
    particle_lists = physics.geometry.rotate_coordinates(particle_lists, N, group_cat, rot_vector)

def save_particle_fields(particle, indices):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    g = 0
    particle[g].to_pickle("./data/tng-100-1/subhalos/subhalo" + str(indices[g]) +"_stars.pkl")
    