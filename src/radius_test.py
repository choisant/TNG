import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import illustris_python as il
import pandas as pd

basePath = "./data/tng-100-3/output"
fields = {"stars": ["Coordinates", "Masses", "Velocities"],
        "gas": ["Coordinates", "Masses", "Velocities"],
        "dm": ["Coordinates", "Potential"]
        }

indices = [1893, 2164, 3043, 3229, 3403, 3605, 3760] #np.genfromtxt("./data/tng-100-3/cutdata/early_type_indices.csv")
stars = [0]*(len(indices))
gas = [0]*(len(indices))
dm = [0]*(len(indices))

for i in range(len(indices)):
    stars[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, 99, indices[i], 'stars', fields["stars"]))
    gas[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, 99, indices[i], 'gas', fields["gas"]))
    dm[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(basePath, 99, indices[i], 'dm', fields["dm"]))
