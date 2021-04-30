import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import illustris_python as il
import physics
"""
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

def stars_out(tng_run, snapshot, i):
    #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    print("Loading stellar particles")

    print("Subhalo ", i)
    stars_dict = il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"])
    stars = il.pandasformat.dict_to_pandas(stars_dict)
    group_cat = physics.properties.group_properties(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, group_cat)
    stars = physics.properties.relative_pos_radius(stars, group_cat)
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum()
    group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    group_cat = physics.properties.half_mass_radius(stars, group_cat)

    return stars

def velocities(tng_run, snapshot, dm_mass, i):
     #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
        "gas": ["Coordinates", "Masses", "StarFormationRate", "Velocities"],
        "dm": ["Coordinates", "Potential", "Velocities"]
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
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
    group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    gas = physics.properties.relative_velocities(gas, group_cat)
    dm = physics.properties.relative_velocities(dm, group_cat)
    #Calculate masses
    group_cat["SubhaloMassTotalGas"] = gas["Masses"].sum()
    group_cat["SubhaloMassTotalDM"] = dm["Masses"].sum()
    group_cat["SubhaloMassTotalStellar"] = stars["Masses"].sum()
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum() #Will get overwritten, necessary for calculations
    group_cat["SubhaloMassTotal"] = group_cat["SubhaloMassTotalGas"] + group_cat["SubhaloMassTotalDM"] + group_cat["SubhaloMassTotalStellar"]
    #Calculate SFR
    group_cat["SubhaloSFRTotal"] = gas["StarFormationRate"].sum()
    #Calculate half mass rad
    group_cat = physics.properties.half_mass_radius(stars, group_cat)
    group_cat["SubhaloHalfmassRadTotalStellar"] = group_cat["SubhaloHalfmassRadStellar"]
    #Kinematics before data_reduction
    rad = group_cat["SubhaloRad"][0]
    group_cat = physics.properties.velocity_disp_projected_stars(stars, group_cat, "SubhaloVelDispTotalStellar")
    group_cat = physics.properties.velocity_disp_3D(stars, group_cat, rad, "SubhaloVelDispTotalStellar3D")
    
    group_cat = physics.properties.velocity_disp_projected(gas, group_cat, "SubhaloVelDispTotalGas")
    group_cat = physics.properties.velocity_disp_3D(gas, group_cat, rad, "SubhaloVelDispTotalGas3D")
    
    group_cat = physics.properties.velocity_disp_projected(dm, group_cat, "SubhaloVelDispTotalDM")
    group_cat = physics.properties.velocity_disp_3D(dm, group_cat, rad, "SubhaloVelDispTotalDM3D")
    #Reduce data size
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    gas = gas[gas["r"] < max_rad]
    dm = dm[dm["r"] < max_rad]
    
    if gas.empty:
        gas = il.pandasformat.empty_gas_df()
        gas = physics.properties.relative_pos_radius(gas, group_cat)
        gas = physics.properties.relative_velocities(gas, group_cat)

    #Calculate masses
    group_cat["SubhaloMassGas"] = gas["Masses"].sum()
    group_cat["SubhaloMassDM"] = dm["Masses"].sum()
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum()
    group_cat["SubhaloMass"] = group_cat["SubhaloMassGas"] + group_cat["SubhaloMassDM"] + group_cat["SubhaloMassStellar"]
    #Calculate SFR
    group_cat["SubhaloSFR"] = gas["StarFormationRate"].sum()
    #Calculate half mass rad
    group_cat = physics.properties.half_mass_radius(stars, group_cat)
    #velocities
    group_cat = physics.properties.velocity_disp_projected_stars(stars, group_cat, "SubhaloVelDispStellar")
    group_cat = physics.properties.velocity_disp_3D(stars, group_cat, max_rad, "SubhaloVelDispStellar3D")
    group_cat = physics.properties.velocity_disp_3D(gas, group_cat, max_rad, "SubhaloVelDispGas3D")
    group_cat = physics.properties.velocity_disp_3D(dm, group_cat, max_rad, "SubhaloVelDispDM3D")

    return group_cat


def mass_vel_photo(tng_run, snapshot, dm_mass, i):
     #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities", "GFM_StellarPhotometrics"],
        "gas": ["Coordinates", "Masses", "StarFormationRate"],
        "dm": ["Coordinates", "Potential"]
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))
    gas = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'gas', fields["gas"]))
    dm = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'dm', fields["dm"]))
    dm["Masses"] = dm_mass
    #Get position, radius and change coordinates
    group_cat = physics.properties.group_properties(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, group_cat)
    stars = physics.properties.relative_pos_radius(stars, group_cat)
    gas = physics.properties.relative_pos_radius(gas, group_cat)
    dm = physics.properties.relative_pos_radius(dm, group_cat)
    group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    #Reduce data size
    max_rad = group_cat["SubhaloGalaxyRad"][0]
    stars = stars[stars["r"] < max_rad]
    gas = gas[gas["r"] < max_rad]
    dm = dm[dm["r"] < max_rad]

    if gas.empty:
        gas = il.pandasformat.empty_gas_df()
        gas = physics.properties.relative_pos_radius(gas, group_cat)
        gas = physics.properties.relative_velocities(gas, group_cat)
    
    #Calculate SFR
    group_cat["SubhaloSFR"] = gas["StarFormationRate"].sum()
    #Calculate masses
    group_cat["SubhaloMassGas"] = gas["Masses"].sum()
    group_cat["SubhaloMassDM"] = dm["Masses"].sum()
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum()
    group_cat["SubhaloMass"] = group_cat["SubhaloMassGas"] + group_cat["SubhaloMassDM"] + group_cat["SubhaloMassStellar"]
    #Calculate half mass rad
    group_cat = physics.properties.half_mass_radius(stars, group_cat)
    half_rad = group_cat["SubhaloHalfmassRadStellar"][0]
    #Mass in half mass rad
    group_cat["SubhaloMassInHalfRadGas"] = gas[gas["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadDM"] = dm[dm["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadStellar"] = group_cat["SubhaloMassStellar"]/2
    group_cat["SubhaloMassInHalfRad"] = (group_cat["SubhaloMassInHalfRadGas"] 
        + group_cat["SubhaloMassInHalfRadDM"] + group_cat["SubhaloMassInHalfRadStellar"])
    #Mass in 2* half mass rad
    group_cat["SubhaloMassInRadGas"] = gas[gas["r"] < 2*half_rad]["Masses"].sum()
    group_cat["SubhaloMassInRadDM"] = dm[dm["r"] < 2*half_rad]["Masses"].sum()
    group_cat["SubhaloMassInRadStellar"] = stars[stars["r"] < 2*half_rad]["Masses"].sum()
    
    #Kinematics
    group_cat = physics.properties.ang_momentum(stars, group_cat)
    group_cat = physics.properties.rot_energy(stars, group_cat)
    group_cat = physics.properties.rotational_vel(gas, dm, stars, group_cat, 2.2*half_rad, "SubhaloRotVel2_2Re")
    group_cat = physics.properties.velocity_disp_projected_stars(stars, group_cat, "SubhaloVelDispStellar")
    #Photometrics
    group_cat = physics.properties.photometrics(stars, group_cat, "15Rvir")

    return group_cat
"""
def set_aperture(tng_run, snapshot, dm_mass, i):
     #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities", "GFM_StellarPhotometrics"],
        "gas": ["Coordinates", "Masses", "StarFormationRate", "Velocities"],
        "dm": ["Coordinates", "Potential", "Velocities"]
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
    stars = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'stars', fields["stars"]))
    gas = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'gas', fields["gas"]))
    dm = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, i, 'dm', fields["dm"]))
    dm["Masses"] = dm_mass
    #Get position, radius and change coordinates
    group_cat = physics.properties.group_properties(group_cat, base_path)
    group_cat = physics.properties.center_halo(stars, group_cat)
    stars = physics.properties.relative_pos_radius(stars, group_cat)
    gas = physics.properties.relative_pos_radius(gas, group_cat)
    dm = physics.properties.relative_pos_radius(dm, group_cat)
    group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    gas = physics.properties.relative_velocities(gas, group_cat)
    dm = physics.properties.relative_velocities(dm, group_cat)
    
    #30 kpc
    max_rad = 30
    #Reduce data size
    stars = stars[stars["r"] < max_rad]
    gas = gas[gas["r"] < max_rad]
    dm = dm[dm["r"] < max_rad]

    if gas.empty:
        gas = il.pandasformat.empty_gas_df()
        gas = physics.properties.relative_pos_radius(gas, group_cat)
        gas = physics.properties.relative_velocities(gas, group_cat)
    
    #Calculate SFR
    group_cat["SubhaloSFR30kpc"] = gas["StarFormationRate"].sum()
    
    #Calculate masses
    group_cat["SubhaloMassGas30kpc"] = gas["Masses"].sum()
    group_cat["SubhaloMassDM30kpc"] = dm["Masses"].sum()
    group_cat["SubhaloMassStellar30kpc"] = stars["Masses"].sum()
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum() #Will get overwritten, necessary for calculations
    group_cat["SubhaloMass30kpc"] = group_cat["SubhaloMassGas30kpc"] + group_cat["SubhaloMassDM30kpc"] + group_cat["SubhaloMassStellar30kpc"]
    #Calculate half mass rad
    group_cat = physics.properties.half_mass_radius(stars, group_cat, rad_key="30kpc")
    group_cat["SubhaloHalfmassRadStellar"] = group_cat["SubhaloHalfmassRadStellar30kpc"] #Will get overwritten, necessary for calculations
    half_rad = group_cat["SubhaloHalfmassRadStellar30kpc"][0]
    #Mass in half mass rad
    group_cat["SubhaloMassInHalfRadGas30kpc"] = gas[gas["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadDM30kpc"] = dm[dm["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadStellar30kpc"] = group_cat["SubhaloMassStellar30kpc"]/2
    group_cat["SubhaloMassInHalfRad30kpc"] = (group_cat["SubhaloMassInHalfRadGas30kpc"] 
        + group_cat["SubhaloMassInHalfRadDM30kpc"] + group_cat["SubhaloMassInHalfRadStellar30kpc"])
    
    #Kinematics
    group_cat = physics.properties.ang_momentum(stars, group_cat, "30kpc")
    group_cat = physics.properties.rot_energy(stars, group_cat, "30kpc")
    group_cat = physics.properties.rotational_vel(gas, dm, stars, group_cat, half_rad, "SubhaloRotVelRe30kpc")
    group_cat = physics.properties.rotational_vel(gas, dm, stars, group_cat, 2.2*half_rad, "SubhaloRotVelRe2230kpc")
    group_cat = physics.properties.velocity_disp_projected_stars(stars, group_cat, rad_key="30kpc")
    group_cat = physics.properties.velocity_disp_3D(stars, group_cat, 30, "SubhaloVelDisp3D_Stellar_30kpc")
    group_cat = physics.properties.velocity_disp_3D(gas, group_cat, 30, "SubhaloVelDisp3D_Gas_30kpc")
    group_cat = physics.properties.velocity_disp_3D(dm, group_cat, 30, "SubhaloVelDisp3D_DM_30kpc")
    #Photometrics
    group_cat = physics.properties.photometrics(stars, group_cat, "30kpc")

    return group_cat

"""
def mass_vel_photo_whole(tng_run, snapshot, dm_mass, i):
     #intitial setup
    base_path = "./data/" + str(tng_run) + "/output"
    fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities", "GFM_StellarPhotometrics"],
        "gas": ["Coordinates", "Masses", "StarFormationRate"],
        "dm": ["Coordinates", "Potential"]
            }
    group_cat = pd.DataFrame({"id": [i]})
    #Load particles
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
    group_cat = physics.properties.subhalo_velocity(stars, group_cat)
    stars = physics.properties.relative_velocities(stars, group_cat)
    #Calculate SFR
    group_cat["SubhaloSFR"] = gas["StarFormationRate"].sum()
    #Calculate masses
    group_cat["SubhaloMassGas"] = gas["Masses"].sum()
    group_cat["SubhaloMassDM"] = dm["Masses"].sum()
    group_cat["SubhaloMassStellar"] = stars["Masses"].sum()
    group_cat["SubhaloMass"] = group_cat["SubhaloMassGas"] + group_cat["SubhaloMassDM"] + group_cat["SubhaloMassStellar"]
    #Calculate half mass rad
    group_cat = physics.properties.half_mass_radius(stars, group_cat)
    half_rad = group_cat["SubhaloHalfmassRadStellar"][0]
    #Mass in half mass rad
    group_cat["SubhaloMassInHalfRadGas"] = gas[gas["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadDM"] = dm[dm["r"] < half_rad]["Masses"].sum()
    group_cat["SubhaloMassInHalfRadStellar"] = group_cat["SubhaloMassStellar"]/2
    group_cat["SubhaloMassInHalfRad"] = (group_cat["SubhaloMassInHalfRadGas"] 
        + group_cat["SubhaloMassInHalfRadDM"] + group_cat["SubhaloMassInHalfRadStellar"])
    #Mass in 2* half mass rad
    group_cat["SubhaloMassInRadGas"] = gas[gas["r"] < 2*half_rad]["Masses"].sum()
    group_cat["SubhaloMassInRadDM"] = dm[dm["r"] < 2*half_rad]["Masses"].sum()
    group_cat["SubhaloMassInRadStellar"] = stars[stars["r"] < 2*half_rad]["Masses"].sum()
    
    #Kinematics
    group_cat = physics.properties.ang_momentum(stars, group_cat)
    group_cat = physics.properties.rot_energy(stars, group_cat)
    group_cat = physics.properties.rotational_vel(gas, dm, stars, group_cat, 2.2*half_rad, "SubhaloRotVel2_2Re")
    group_cat = physics.properties.velocity_disp_projected_stars(stars, group_cat, "SubhaloVelDispStellar")
    #Photometrics
    group_cat = physics.properties.photometrics(stars, group_cat, "Total")

    return group_cat


def save_particle_fields(particle, indices):
    #About 30MB for a 9.5 10^10 M_o galaxy
    #Save all fields for particles in one subhalo for later inspection
    g = 0
    particle[g].to_pickle("./data/tng-100-1/subhalos/subhalo" + str(indices[g]) +"_stars.pkl")
"""