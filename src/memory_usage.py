import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import illustris_python as il
import physics

tng_run = input("TNG run: tng-xxx-x -- ")
snapshot = 99
indices = np.genfromtxt("./data/" + tng_run + "/cutdata/central_id.txt", int)
base_path = "./data/" + str(tng_run) + "/output"
fields = {"stars": ["Coordinates", "Potential", "Masses", "Velocities"],
    "gas": ["Coordinates", "Masses"],
    "dm": ["Coordinates", "Potential"]
    }
N = len(indices)
stars = [0]*N
gas = [0]*N
dm = [0]*N

#Load all particles

for i in range(N):
        print("Subhalo ", indices[i])
        input("Load stellar particles")
        stars[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'stars', fields["stars"]))
        stars[i].info(verbose=False)
        input("Load gas particles")
        gas[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'gas', fields["gas"]))
        gas[i].info(verbose=False)
        input("Load dm particles")
        dm[i] = il.pandasformat.dict_to_pandas(il.snapshot.loadSubhalo(base_path, snapshot, indices[i], 'dm', fields["dm"]))
        gas[i].info(verbose=False)
        check = input("type 'yes' to continue: ")
        if check != "yes":
            quit

            