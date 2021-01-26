"""
This script takes in the Group catalog data from the .hdf5 files,
and uses the pandasformat.py file to convert the data to the pandas DataFrame format.
The data is then run through the desired filter, and saved as a .pkl file in the
cutdata folder of the relevant simulation.
"""
import pandas as pd
import illustris_python as il
pd.options.mode.chained_assignment = None  # default='warn'

#filters
def subhalo_flag_drop(df):
    df_copy = df.copy(deep=True)
    index_names = df_copy[df_copy["SubhaloFlag"] == 0].index
    df_copy = df_copy.drop(index_names)
    return df_copy

def dark_matter_zeros(df):
    df_copy = df.copy(deep=True)
    index_names = df_copy[df_copy["SubhaloMassDM"] == 0].index
    df_copy = df_copy.drop(index_names)
    return df_copy

def min_particles(df, minPart):
    df_copy = df.copy(deep=True)
    print("Removing galaxies below the minimum amount of particles.")
    index_names = df_copy[df_copy["SubhaloLen"] < minPart].index
    df_copy = df_copy.drop(index_names)
    return df_copy

def min_ymass(df, minMass, Y, haloType):
    print("Removing galaxies below the minimum mass.")
    df_copy = df.copy(deep=True)
    particle_type = (haloType+"Mass"+Y)
    if haloType == "Subhalo":
        df_copy = subhalo_flag_drop(df)
        df_copy = dark_matter_zeros(df)
    #Get indices that fail to meet this condition.
    index_names = df_copy[df_copy[particle_type] < minMass].index
    df_copy = df_copy.drop(index_names)
    return df_copy

def central_galaxies(df_halos, df_subhalos):
    #dfHalos must have the key-value pair GroupFirstSub
    print("Starting the central galaxies sorting")
    central_indices = df_halos["GroupFirstSub"]
    central_indices = central_indices[central_indices > 0]
    central_halos = df_subhalos.iloc[central_indices]
    return central_halos

def late_type_SFR(df):
    df_copy = df.copy(deep=True)
    index_names_1 = df_copy[df_copy["SubhalosSFR"] > 0.36].index
    df_copy = df_copy.drop(index_names_1, inplace=True)
    index_names_2 = df_copy[df_copy["SubhalosSFR"] < 0.036].index
    df_copy = df_copy.drop(index_names_2)
    return df_copy

def early_type_SFR(df):
    df_copy = df.copy(deep=True)
    index_names = df_copy[df_copy["SubhalosSFR"] > 0.01148].index
    df_copy = df_copy.drop(index_names)
    return df_copy

def late_type_gas(df):
    df_copy = df.copy(deep=True)
    df_copy["SubhaloGasFraction"] = df_copy["SubhaloMassInHalfRadGas"]/df_copy["SubhaloMassInHalfRadStellar"]
    index_names = df_copy[df_copy["SubhaloGasFraction"] < 0.1].index #Ferrero2020
    df_copy = df_copy.drop(index_names)
    return df_copy

def early_type_gas(df):
    df_copy = df.copy(deep=True)
    df_copy["SubhaloGasFraction"] = df_copy["SubhaloMassInHalfRadGas"]/df_copy["SubhaloMassInHalfRadStellar"]
    index_names = df_copy[df_copy["SubhaloGasFraction"] > 0.1].index #Ferrero2020
    df_copy = df_copy.drop(index_names)
    return df_copy

#Saving the data in the correct format
def save_data_CSV(df, haloType, filename, tngFolder):
    path = "./data/"+tngFolder+"/cutdata/"+haloType+"_"+filename+".csv"
    f = open(path, "a+") #Create file if it does not already exist.
    df.to_csv(path)

def save_data_pickle(df, haloType, filename, tngFolder):
    path = "./data/"+tngFolder+"/cutdata/"+haloType+"_"+filename+".pkl"
    f = open(path, "a+") #Create file if it does not already exist.
    df.to_pickle(path)

def create_data_subset(subhalo_fields, halo_fields, min_mass):
    subhalos = il.groupcat.loadSubhalos(BASE_PATH, SNAPSHOT, subhalo_fields)
    df_subhalos = il.pandasformat.dict_to_pandas(subhalos)
    df_subhalos["id"] = df_subhalos.index
    df_subhalos = il.pandasformat.ssfr(df_subhalos)
    print("added ssfr")
    
    halos = il.groupcat.loadHalos(BASE_PATH, SNAPSHOT, halo_fields)
    df_halos = il.pandasformat.dict_to_pandas(halos)
    print("Done converting to pandas DataFrame")

    centrals = central_galaxies(df_halos, df_subhalos)
    centrals_min_mass = min_ymass(centrals, minMass=min_mass, Y="Stellar", haloType="Subhalo")
    #save_data_pickle(centrals_min_mass, haloType="Subhalo", filename="Centrals_minE9_SM", tngFolder="tng100-1")

    lates = late_type_gas(centrals_min_mass)
    #save_data_pickle(lates, haloType="Subhalo", filename="Centrals_minE9_SM_lateType_Gas", tngFolder="tng100-1")

    earlies = early_type_gas(centrals_min_mass)
    #save_data_pickle(earlies, haloType="Subhalo", filename="Centrals_minE9_SM_earlyType_Gas", tngFolder="tng100-1")
    return list(centrals_min_mass["id"])
#
#read in data

BASE_PATH = "./data/tng-100-3/output"
SNAPSHOT = 99
subhaloFields = ["SubhaloMass", 'SubhaloMassType', 'SubhaloFlag', "SubhaloLen", "SubhaloSFR",
                "SubhaloVel", "SubhaloVelDisp", "SubhaloHalfmassRadType", "SubhaloMassInHalfRadType",
                "SubhaloMassInHalfRad", "SubhaloVmax", "SubhaloVmaxRad", "SubhaloStellarPhotometrics", "SubhaloBHMass"]

haloFields = ["GroupMass", "GroupMassType", "GroupNsubs", "GroupFirstSub"]

centrals_id = create_data_subset(subhaloFields, haloFields, 9.5)
with open('./data/tng-100-3/cutdata/central_ids.txt', 'w') as file:
    for index in centrals_id:
        file.write("%i\n" % index)