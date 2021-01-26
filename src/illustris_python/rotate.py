import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import pandas as pd

def rotate_basis(old_basis, new_z_axis):

    v = new_z_axis
    v_xy = np.array([v[0], v[1], 0])
    v_len = np.linalg.norm(v)
    v_xy_len = np.linalg.norm(v_xy)

    #Get rotation angles
    theta = np.nan_to_num(np.arccos(np.dot(v, old_basis[:, 2])/v_len)) #get angle between new z axis and old z axis
    phi = np.nan_to_num(np.arccos(np.dot(v_xy, old_basis[:, 0])/v_xy_len)) #get angle between projected new z axis and old x axis
    print(np.degrees(theta), np.degrees(phi))
    #Create rotation matrix
    #Rotate phi radians about z and theta radians about y
    r = R.from_euler('zyx', [phi, theta, 0])
    new_basis = np.array(r.as_matrix())
    return new_basis
new_z = [1, 1, 1]
test_vec = [1, 4, 1]
B2 = rotate_basis(np.identity(3), new_z)


new_vec = np.dot(B2, np.transpose(test_vec))
#print(np.linalg.norm(test_vec), np.linalg.norm(new_vec))

g = pd.read_pickle("./data/disk_galaxy.pkl")
x = g[g["r"]<100]["x"]
y = g[g["r"]<100]["y"]
z = g[g["r"]<100]["z"]


y_rot = g[g["r"]<0.1]["y_rot"].values
i=0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(xs=g[g["r"]<200]["x_rot"].values, ys=g[g["r"]<200]["y"].values, zs=g[g["r"]<200]["z"].values)
ax.scatter(xs=x, ys=y, zs=z, s=list(g[g["r"]<100]["Masses"].values*10))
plt.show()

"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(0,0,0, 0, 0, 1, color = "black")
ax.quiver(0,0,0, 0, 1, 0, color = "black")
ax.quiver(0,0,0, 1, 0, 0, color = "black")
ax.quiver(0,0,0, test_vec[0], test_vec[1], test_vec[2], color = "red")
ax.quiver(0,0,0, new_vec[0], new_vec[1], new_vec[2], color = "blue")
ax.quiver(0,0,0, new_z[0], new_z[1], new_z[2], color = "orange")

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_zlim(-2,2)
plt.show()
"""