import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il

basePath = "./data/tng-100-1/subhalos/subhalo"
subhalo_id = "371259"

stars = pd.read_pickle(basePath + subhalo_id + "_stars.pkl")


fig = plt.figure()

x = stars[stars["r"] < 50]["x_rot"]
y = stars[stars["r"] < 50]["y_rot"]
z = stars[stars["r"] < 50]["z_rot"]

#ax.scatter(dm_pos[:,0], dm_pos[:,1], dm_pos[:,2], c = "black", s=2, alpha = 0.7, label = "dm particles")
#ax.scatter(gas_pos[:,0], gas_pos[:,1], gas_pos[:,2], c = "orange", s=2, alpha = 0.8, label = "gas particles")
plt.scatter(x, y, c = "orange", s=3, alpha = 1, label ="stellar particles")
plt.xlabel('x [ckpc/h]')
plt.ylabel('y [ckpc/h]')
plt.legend()
plt.show()
plt.scatter(y, z, c = "orange", s=3, alpha = 1, label ="stellar particles")
plt.show()
plt.xlabel('y [ckpc/h]')
plt.ylabel('z [ckpc/h]')
plt.legend()
plt.scatter(x, z, c = "orange", s=3, alpha = 1, label ="stellar particles")
plt.show()
plt.xlabel('x [ckpc/h]')
plt.ylabel('z [ckpc/h]')
plt.legend()


