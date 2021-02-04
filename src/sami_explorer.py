import illustris_python as il
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from astropy.cosmology import FlatLambdaCDM

#df = pd.read_pickle("./data/SAMI/sami.pkl")
df1 = pd.read_csv("./data/SAMI/allData.csv")

cosmo = FlatLambdaCDM(H0=67, Om0=0.31, Ob0=0.0486)
df1["r_e_67"] = (np.sin(np.radians(df1["r_e_angles"]/3600))*cosmo.comoving_distance(df1["z_spec"]))*1000 #kpc

cosmo = FlatLambdaCDM(H0=70, Om0=0.31, Ob0=0.0486)
#df1["r_e"] = (np.sin(np.radians(df1["r_e_angles"]/3600))*cosmo.luminosity_distance(df1["z_spec"]))*1000 #kpc
df1["r_e_70"] = (np.sin(np.radians(df1["r_e_angles"]/3600))*cosmo.comoving_distance(df1["z_spec"]))*1000 #kpc

df1["r_e_circ"] = np.sqrt(1-df1["ellip"])*df1["r_e_70"]
df1["r_e_circ_3D"] = df1["r_e_circ"]*(4/3)

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (8,8))
df1.plot.scatter(x="mstar", y="r_e_70" ,s=3, ax=ax, color = "blue")
df1.plot.scatter(x="mstar", y="r_e_circ_3D" ,s=3, ax=ax, color = "red")
il.formatplot.SM_R(title="Effective radius-mass", ax=ax, y0=10**(-1), x0 = 10**7, x1=10**12)
plt.show()
