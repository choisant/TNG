"""
This script provides functions for working with Pandas using the TNG data
"""

import pandas as pd
import numpy as np

def dict_to_pandas(data):
    """
    Converts a dictionary to a pandas dataframe. Unloads lists within lists.
    """
    key_list = list(data.keys())
    for key in key_list:
        if key != "count":
            dummy = data[key]
            data[key] = list(dummy)
        if key == "SubhaloMassType":
            particle_types = {"SubhaloMassGas": 0,
                              "SubhaloMassDM": 1,
                              "None": 2,
                              "SubhaloMassTracers": 3,
                              "SubhaloMassStellar": 4,
                              "SubhaloMassBH": 5}
            masses = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = masses[:,particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)

        if key == "GroupMassType":
            particle_types = {"GroupMassGas": 0,
                              "GroupMassDM": 1,
                              "None": 2,
                              "GroupMassTracers": 3,
                              "GroupMassStellar": 4,
                              "GroupMassBH": 5}
            masses = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = masses[:,particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)

        if key == "SubhaloMassInHalfRadType":
            particle_types = {"SubhaloMassInHalfRadGas": 0,
                              "SubhaloMassInHalfRadDM": 1,
                              "SubhaloMassInHalfRadNone": 2,
                              "SubhaloMassInHalfRadTracers": 3,
                              "SubhaloMassInHalfRadStellar": 4,
                              "SubhaloMassInHalfRadBH": 5}
            masses = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = masses[:, particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)
        if key == "SubhaloHalfmassRadType":
            particle_types = {"SubhaloHalfmassRadGas": 0,
                              "SubhaloHalfmassRadDM": 1,
                              "SubhaloHalfmassRadNone": 2,
                              "SubhaloHalfmassRadTracers": 3,
                              "SubhaloHalfmassRadStellar": 4,
                              "SubhaloHalfmassRadBH": 5}
            masses = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = masses[:, particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)
        if key == "Coordinates":
            directions = {"X": 0,
                          "Y": 1,
                          "Z": 2}
            positions = np.array(data[key])
            for xyz in directions:
                temp = positions[:, directions[xyz]]
                data[xyz] = list(temp)
        
    df = pd.DataFrame(data, dtype=object)
    return df

def stellar_masses(df):
    """
    Changes the stellar masses of the dataframe from 10**10 M_o/h to M_o 
    """
    particle_types = ["SubhaloMassGas",
                      "SubhaloMassDM",
                      "SubhaloMassStellar",
                      "SubhaloMassBH",
                      "SubhaloMassInHalfRadGas",
                      "SubhaloMassInHalfRadDM",
                      "SubhaloMassInHalfRadStellar",
                      "SubhaloMass",
                      "SubhaloMassInHalfRad",
                      "SubhaloBHMass"]
    for particle in particle_types:
        print(particle + "...")
        df[particle] *= (10**10)/0.67 #changes the units to stellar mass
    return df

def ssfr(df):
    """
    Adds star formation rates
    """
    keys = df.keys()
    if "SubhaloSFR" in keys:
        df["SubhalosSFR"] = df["SubhaloSFR"]/df["SubhaloMassStellar"]
        df["SubhalosSFR"] *= 10**(9) #sSFR in unit Gyr^(-1)
    return df
