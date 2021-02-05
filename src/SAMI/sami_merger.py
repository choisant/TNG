import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from astropy.cosmology import FlatLambdaCDM

# TNG cosmology
cosmo = FlatLambdaCDM(H0=67.7, Om0=0.31, Ob0=0.0486)

h=0.6774 #Planck 2015

#df1 = pd.read_csv("./data/SAMI/dr1.csv")
df2 = pd.read_csv("./data/SAMI/dr2_stellar_kinematics.csv")
df3 = pd.read_csv("./data/SAMI/dr2_gas.csv")
df4 = pd.read_csv("./data/SAMI/dr2_gas_recom.csv")
df1 = pd.read_csv("./data/SAMI/dr2_sample.csv")
df5 = pd.read_csv("./data/SAMI/STELLAR_details.csv")
#datalist = [df1, df2, df3, df4]
#data = pd.DataFrame(data = df1)
data1 = pd.merge(df1, df2, how="outer", on='cataid')
data2 = pd.merge(df3, df4, how="outer", on='cataid')
data3 = pd.merge(data2, df5, how="outer", on='cataid')
data = pd.merge(data1, data3, how = "outer", on='cataid')
#data = pd.merge(data3, df5, how = "outer", on="cataid")

#adding useful fields
data["mstar_log"] = data["mstar"]
data["mstar"] = 10**data["mstar_log"]
data["mstarhalf"] = data["mstar"]*0.5
data["MSAMI_log"] = data["MSAMI"]
data["MSAMI"] = 10**data["MSAMI_log"]
indexNames = data[data["r_e"] < 0].index
data.drop(indexNames, inplace=True)
data["r_e_angles"] = data["r_e"]
data["r_e"] = (np.sin(np.radians(data["r_e_angles"]/3600))*cosmo.luminosity_distance(data["z_spec"]))*1000 #kpc
data["r_e_circ"] = np.sqrt(1-data["ellip"])*data["r_e"]
data["r_petro_angles"] = data["r_petro"]
data["r_petro"] = (np.sin(np.radians(data["r_petro_angles"]/3600))*cosmo.luminosity_distance(data["z_spec"]))*1000 #kpc
data["r_auto_angles"] = data["r_auto"]
data["r_auto"] = (np.sin(np.radians(data["r_auto_angles"]/3600))*cosmo.luminosity_distance(data["z_spec"]))*1000 #kpc
data = data.sort_values(by=["cataid"])

data.to_csv("./data/SAMI/all_data_vrot.csv")

