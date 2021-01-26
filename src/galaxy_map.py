import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il

basePath = "./data/tng-100-3/output"
subhalo_id = 4678

stars = il.snapshot.loadSubhalo(basePath, 99, subhalo_id, 'stars')
gas = il.snapshot.loadSubhalo(basePath, 99, subhalo_id, 'gas')
dm = il.snapshot.loadSubhalo(basePath, 99, subhalo_id, 'dm')

print(gas.keys())
gas_pos = gas["Coordinates"]
star_pos = stars["Coordinates"]
dm_pos = dm["Coordinates"]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#ax.scatter(dm_pos[:,0], dm_pos[:,1], dm_pos[:,2], c = "black", s=2, alpha = 0.7, label = "dm particles")
#ax.scatter(gas_pos[:,0], gas_pos[:,1], gas_pos[:,2], c = "orange", s=2, alpha = 0.8, label = "gas particles")
ax.scatter(star_pos[:,0], star_pos[:,1], star_pos[:,2], c = "orange", s=5, alpha = 1, label ="stellar particles")


#plt.xlim([800, 1000])
#plt.ylim([26550, 26750])
plt.xlabel('x [ckpc/h]')
plt.ylabel('y [ckpc/h]')
plt.legend()
plt.show()
