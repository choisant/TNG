import numpy as np
import numpy.linalg as lg
from scipy.spatial.transform import Rotation as R

def rotate_coordinates(subhalo, rot_vector):
    """
    Rotates the coordinates of the particles such that the z-sxis aligns with rot_vector.
    """
    def rotate_basis(new_z_axis):
        """
        Returns the rotation matrix for a rotation where the new z-axis is alligned with the axis "new_z_axis".
        """
        old_basis = np.identity(3)
        v = new_z_axis
        v_xy = np.array([v[0], v[1], 0])
        theta = np.nan_to_num(np.arccos(np.dot(v/lg.norm(v), old_basis[:, 2]))) #get angle between new z axis and old z axis
        phi = np.nan_to_num(np.arccos(np.dot(v_xy/lg.norm(v_xy), old_basis[:, 0]))) #get angle between projected new z axis and old x axis
        #Rotate phi radians about z and theta radians about y
        r = R.from_euler('zyx', [phi, -theta, 0])
        rot_matrix = np.array(r.as_matrix()) #convert to numpy array
        return rot_matrix

    rotation_matrix = rotate_basis(rot_vector)
    #print("Rotating galaxy ", i) #This function takes a lot of time
    temp = subhalo.copy(deep=True)
    old_positions = np.transpose(np.array([temp["x"], temp["y"], temp["z"]])) #get coordinates in vector form
    new_positions = np.zeros([len(old_positions), 3]) #empty list
    for j in range(len(old_positions)): #If this could be done faster, code would improve
        new_positions[j] = np.dot(rotation_matrix, np.transpose(old_positions[j]))# r' = Rr
    #new_positions = np.transpose(new_positions)
    subhalo["x_rot"] = new_positions[:, 0]
    subhalo["y_rot"] = new_positions[:, 1]
    subhalo["z_rot"] = new_positions[:, 2]
    return subhalo

def rotate_pos_vel(subhalo, rot_vector):
    """
    Rotates the coordinates of the particles such that the z-sxis aligns with rot_vector.
    """
    def rotate_basis(new_z_axis):
        """
        Returns the rotation matrix for a rotation where the new z-axis is alligned with the axis "new_z_axis".
        """
        old_basis = np.identity(3)
        v = new_z_axis
        if lg.norm(v) > 0: #Check that the new z-axis is non-zero
            v_xy = np.array([v[0], v[1], 0])
            theta = np.arccos(np.dot(v/lg.norm(v), old_basis[:, 2])) #get angle between new z axis and old z axis
            phi = np.arccos(np.dot(v_xy/lg.norm(v_xy), old_basis[:, 0])) #get angle between projected new z axis and old x axis
        else:
            theta = 0
            phi = 0
        #Rotate phi radians about z and theta radians about y
        r = R.from_euler('zyx', [phi, -theta, 0])
        rot_matrix = np.array(r.as_matrix()) #convert to numpy array
        return rot_matrix

    rotation_matrix = rotate_basis(rot_vector)
    #print("Rotating galaxy ", i) #This function takes a lot of time
    temp = subhalo.copy(deep=True)
    new = subhalo.copy(deep=True)
    old_positions = np.transpose(np.array([temp["x"], temp["y"], temp["z"]])) #get coordinates in vector form
    old_velocities = np.transpose(np.array([temp["Vx"], temp["Vy"], temp["Vz"]])) #get coordinates in vector form
    new_positions = np.zeros([len(old_positions), 3]) #empty list
    new_velocities = np.zeros([len(old_velocities), 3]) #empty list
    for j in range(len(old_positions)): #If this could be done faster, code would improve
        new_positions[j] = np.dot(rotation_matrix, np.transpose(old_positions[j]))# r' = Rr
        new_velocities[j] = np.dot(rotation_matrix, np.transpose(old_velocities[j]))
    
    new["x"] = new_positions[:, 0]
    new["y"] = new_positions[:, 1]
    new["z"] = new_positions[:, 2]

    new["Vx"] = new_velocities[:, 0]
    new["Vy"] = new_velocities[:, 1]
    new["Vz"] = new_velocities[:, 2]
    return new