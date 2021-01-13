import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il

fields = ['Masses']
basePath = "./data/tng-100-3/output"
gas_mass = il.snapshot.loadSubset(basePath, 99,'gas', fields=fields)
print (np.log10(np.mean(gas_mass, dtype='double')*1e10/0.704))
"""
dm_pos = il.snapshot.loadSubset(basePath, 99, 'dm', ['Coordinates'])
plt.hist2d(dm_pos[:,0], dm_pos[:,1], norm = mpl.colors.LogNorm(), bins=64)
plt.xlim([0,75000])
plt.ylim([0,75000])
plt.xlabel('x [ckpc/h]')
plt.ylabel('y [ckpc/h]')
plt.show()
"""
stars = il.snapshot.loadSubhalo(basePath, 99, 1893, 'stars')
print(stars.keys())
for i in range(3):
    print(np.min(stars['Coordinates'][:,i]), np.max(stars['Coordinates'][:,i]))

subhaloFields = ["SubhaloMass", 'SubhaloMassType', "SubhaloHalfmassRadType"]
haloFields = ["GroupMass", "GroupMassType"]
subhalos = il.groupcat.loadSubhalos(basePath, 99, fields=subhaloFields)
df_subhalos = il.pandasformat.dict_to_pandas(subhalos)

halos = il.groupcat.loadHalos(basePath, 99, fields=haloFields)
df_halos = il.pandasformat.dict_to_pandas(halos)

print("Mass second subhalo:", df_subhalos["SubhaloMass"][1893])
print("Mass second halo:", df_halos["GroupMass"][1893])
