import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il
import pandas as pd

def radius(df):
    x = np.array(df["x"])
    y = np.array(df["y"])
    z = np.array(df["z"])
    r = (x**2 + y**2 + z**2)**(1/2)
    return r

#calculate radius
def particle_radii(particles, N, catalogue):
    #THIS CODE TAKES A LONG TIME. IMPROVEMENTS?
    center_of_mass = np.zeros([N,3])
    for i in range(N):
        #find center of halo
        min_pot = 0
        for particle in particles:
            #Find particle with lowest potential
            min_pot_value = particle[i]["Potential"].min()
            if min_pot_value < min_pot:
                min_pot = min_pot_value
                #Get particle position and assign as center of galaxy
                min_pot_pos = particle[i][particle[i]["Potential"] == min_pot_value]["Coordinates"].values[0]
        center_of_mass[i] = min_pot_pos
        #Calculate new coordinates
        for particle in particles:
            particle[i]["x"] = particle[i]["X"] - min_pot_pos[0]
            particle[i]["y"] = particle[i]["Y"] - min_pot_pos[1]
            particle[i]["z"] = particle[i]["Z"] - min_pot_pos[2]
            particle[i]["r"] = radius(particle[i])
    #Save to group catalogue
    catalogue["CenterOfMassX"] = center_of_mass[:,0]
    catalogue["CenterOfMassY"] = center_of_mass[:,1]
    catalogue["CenterOfMassZ"] = center_of_mass[:,2]
    return particles, catalogue

#Calculate total mass for each particle type
def total_mass(particles, N, catalogue):
    particle_mass = np.zeros([len(particles), N])
    p = 0
    for particle in particles:
        for i in range(N):
            particle_mass[p][i] = particle[i]["Masses"].sum() #or load from snapshot to save time
        p = p + 1
    total_mass = particle_mass.sum()

    #save value to catalogue
    catalogue["SubhaloMassGas"] = particle_mass[0]
    catalogue["SubhaloMassDM"] = particle_mass[1]
    catalogue["SubhaloMassStellar"] = particle_mass[2]
    catalogue["SubhaloMass"] = total_mass
    return particles, catalogue
    

def half_mass_radius(particles, N, catalogue):
    #Calculate half mass radius
    halfmass_rad = np.zeros(N)
    for i in range(N):
        temp = particles[2][i].copy(deep=True)
        temp = temp.sort_values(by="r")
        temp_mass = 0
        n = temp["count"][0]
        r_max = 40
        r = 0
        for j in range(n):
            if temp_mass < (catalogue["SubhaloMassStellar"][i]/2):
                temp_mass = temp_mass + temp["Masses"][j]
            else:
                m1 = temp["Masses"][j-1]
                m2 = temp["Masses"][j]
                M = m1+m2
                halfmass_rad[i] = (m1*temp["r"][j-1] + m2*temp["r"][j])/M #some uncertainty here, now center of mass
                break  
    catalogue["SubhaloHalfmassRadStellar"] = halfmass_rad
    return particles, catalogue
