import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from astropy.cosmology import FlatLambdaCDM

# TNG cosmology
cosmo = FlatLambdaCDM(H0=67.7, Om0=0.31, Ob0=0.0486)

h=0.6774 #Planck 2015

df1 = pd.read_csv("./data/SAMI/stellar_kin_data.csv")
df2 = pd.read_csv("./data/SAMI/gas_kin_data.csv")
df3 = pd.read_csv("./data/SAMI/morph_data.csv")
df4 = pd.read_csv("./data/SAMI/mge_data.csv")
df5 = pd.read_csv("./data/SAMI/input_cat.csv")
df6 = pd.read_csv("./data/SAMI/vrot_data.csv")

df1.set_index('catid', inplace=True)
df2.set_index('catid', inplace=True)
df3.set_index('catid', inplace=True)
df4.set_index('catid', inplace=True)
df5.set_index('catid', inplace=True)
df6.set_index('catid', inplace=True)

"""
data1 = df1.join(df2, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data2 = df3.join(df4, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data3 = data2.join(data1, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data4 = data3.join(df5, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data5 = data4.join(df6, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data = data5.join(df7, lsuffix="DROP").filter(regex="^(?!.*DROP)")
"""

data1 = df1.join(df2, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data2 = df3.join(df4, lsuffix="DROP").filter(regex="^(?!.*DROP)")
data3 = data2.join(data1, lsuffix="DROP")
data4 = data3.join(df5, rsuffix="input")
data = data4.join(df6, rsuffix="cluster")

#adding useful fields
data["mstar_log"] = data["mstar"]
data["mstar"] = 10**data["mstar_log"]
data["mstarhalf"] = data["mstar"]*0.5
#data["MSAMI_log"] = data["MSAMI"]
#data["MSAMI"] = 10**data["MSAMI_log"]
indexNames = data[data["r_e"] < 0].index
data.drop(indexNames, inplace=True)
data["r_e_angles"] = data["r_e"]
data["r_e"] = (np.sin(np.radians(data["r_e_angles"]/3600))*cosmo.luminosity_distance(data["z_spec"]))*1000 #kpc
data["r_e_circ"] = np.sqrt(1-data["ellip"])*data["r_e"]
data["r_mge_angles"] = data["remge"]
data["r_mge"] = (np.sin(np.radians(data["r_mge_angles"]/3600))*cosmo.luminosity_distance(data["z_spec"]))*1000 #kpc
data = data.sort_values(by=["catid"])

data.to_csv("./data/SAMI/dr3.csv")

