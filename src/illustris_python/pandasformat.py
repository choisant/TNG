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
        if key == "SubhaloMassInRadType":
            particle_types = {"SubhaloMassInRadGas": 0,
                            "SubhaloMassInRadDM": 1,
                            "SubhaloMassInRadNone": 2,
                            "SubhaloMassInRadTracers": 3,
                            "SubhaloMassInRadStellar": 4,
                            "SubhaloMassInRadBH": 5}
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
            radii = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = radii[:, particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)

        if key == "SubhaloStellarPhotometrics":
            particle_types = {"SubhaloStellarPhotometrics_g": 4,
                            "SubhaloStellarPhotometrics_i": 6}
            photometrics = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = photometrics[:, particle_types[particle]]
                data[particle] = list(temp)

        if key == "GFM_StellarPhotometrics":
            particle_types = {"StellarPhotometrics_g": 4,
                            "StellarPhotometrics_i": 6}
            photometrics = np.array(data[key]) #create Series object
            for particle in particle_types:
                temp = photometrics[:, particle_types[particle]]
                data[particle] = list(temp)
            data.pop(key)
    if len(key_list) > 0:
        df = pd.DataFrame(data, dtype=object)
    else:
        df = empty_df()
    return df

def empty_df():
    data = {
        "Coordinates": [[0, 0, 0]],
        "Masses": [0],
        "StarFormationRate":[0]
    }
    df = pd.DataFrame(data, dtype=object)
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
