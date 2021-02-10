import numpy as np
import numpy.linalg as lg
import illustris_python as il

def center_halo(subhalo, catalogue):
    center_of_halo = np.zeros(3) #list for saving the central positions for all subhalos
    #find center of halo
    #Find particle with lowest potential
    min_pot_value = subhalo["Potential"].min()
    center_of_halo = subhalo[subhalo["Potential"] == min_pot_value]["Coordinates"].values[0]

    #Save to group catalogue
    catalogue["SubhaloPosX"] = center_of_halo[0]
    catalogue["SubhaloPosY"] = center_of_halo[1]
    catalogue["SubhaloPosZ"] = center_of_halo[2]
    return catalogue

def relative_pos_radius(subhalo, catalogue):
    """
    Finds the center of the subhalo by locating  the particle with the lowest gravitational potential.
    Saves this to group catalogue.
    Calculates the relative positions of all particles and adds the new fields to dataframe.
    Calculates distance from center (radius) for all particles and adds the field to dataframe.
    """
    def radius(df):
        x = np.array(df["x"])
        y = np.array(df["y"])
        z = np.array(df["z"])
        r = (x**2 + y**2 + z**2)**(1/2)
        return r

    #Calculate new coordinates
    positions = np.array(list(subhalo["Coordinates"].values))
    subhalo["x"] = positions[:, 0] - catalogue["SubhaloPosX"][0]
    subhalo["y"] = positions[:, 1] - catalogue["SubhaloPosY"][0]
    subhalo["z"] = positions[:, 2] - catalogue["SubhaloPosZ"][0]
    subhalo["r"] = radius(subhalo)

    return subhalo

def group_properties(catalogue, base_path):

    #Decide on galaxy radius. 10% of total halo radius.
    subhalo_indices = np.array(catalogue["id"])
    halo_fields = ["Group_R_Crit200", "Group_M_Crit200"]
    subhalo_fields = ["SubhaloGrNr"]
    df_halos = il.pandasformat.dict_to_pandas(il.groupcat.loadHalos(base_path, 99, halo_fields))
    df_subhalos = il.pandasformat.dict_to_pandas(il.groupcat.loadSubhalos(base_path, 99, subhalo_fields))

    df_central_subhalos = df_subhalos.iloc[subhalo_indices]
    halo_indices = df_central_subhalos["SubhaloGrNr"]
    df_central_halos = df_halos.iloc[halo_indices]
    radius_200 = np.array(df_central_halos["Group_R_Crit200"])

    catalogue["SubhaloGalaxyRad"] = 0.15*radius_200
    catalogue["SubhaloRad"] = radius_200
    catalogue["SubhaloMass200"] = np.array(df_central_halos["Group_M_Crit200"])

    return catalogue

def total_stellar_mass(stars, catalogue):
    """
    Calculate total mass for a particle type and saves it to the group catalogue
    """
    #save value to catalogue
    catalogue["SubhaloMassStellar"] = stars["Masses"].sum()
    return catalogue


def subhalo_velocity(subhalo, catalogue):
    """
    Calculates the mass weighted average velocity of the particles in a subhalo and save them to the group catalogue.
    """
    subhalo_velocities = np.zeros(3) #Empty list
    m = np.array(subhalo["Masses"]) 
    M = np.sum(m)
    velocities = np.array(list(subhalo["Velocities"].values))
    #Velocity times mass for each particle
    vx_m = velocities[:, 0]*m
    vy_m = velocities[:, 1]*m
    vz_m = velocities[:, 2]*m
    subhalo_velocities = (vx_m.sum(), vy_m.sum(), vz_m.sum())/M #Mass weighted average velocity
    #save to group catalogue
    catalogue["SubhaloVelX"] = subhalo_velocities[0]
    catalogue["SubhaloVelY"] = subhalo_velocities[1]
    catalogue["SubhaloVelZ"] = subhalo_velocities[2]
    return subhalo, catalogue

def relative_velocities(subhalo, catalogue):
    """
    Adds the relative velocity to the dataframes of a chosen particle type.
    """

    vel_av = [catalogue["SubhaloVelX"][0], catalogue["SubhaloVelY"][0], catalogue["SubhaloVelZ"][0]]
    velocities = np.array(list(subhalo["Velocities"].values))
    vx = velocities[:, 0]
    vy = velocities[:, 1]
    vz = velocities[:, 2]
    #Subtracts subhalo velocity from global velocities to get local velocities
    subhalo["Vx"] = vx - vel_av[0]
    subhalo["Vy"] = vy - vel_av[1]
    subhalo["Vz"] = vz - vel_av[2]
    return subhalo

def half_mass_radius(subhalo, catalogue):
    """
    Calculates stellar half mass radius for a certain particle type and adds it to the group catalogue.
    """
    mass_key = "SubhaloMassStellar"
    rad_key = "SubhaloHalfmassRadStellar"
    temp = subhalo.copy(deep=True)
    temp.sort_values(by="r", inplace = True) #sort particles by radius
    temp = temp.reset_index(drop=True)
    temp_mass = 0
    #Start adding the masses of all particles starting with smallest radius
    for j in range(len(temp["r"])):
        #Check if total mass is less than half total particle mass
        if temp_mass < (catalogue[mass_key][0]/2):
            temp_mass = temp_mass + temp["Masses"][j] #Add mass of next particle
        else:
            #Add half mass radius.
            #Some uncertainty on calculation method here, now center of mass between particle j and j-i.
            m1 = temp["Masses"][j-1]
            m2 = temp["Masses"][j]
            M = m1+m2
            halfmass_rad = (m1*temp["r"][j-1] + m2*temp["r"][j])/M
            break  #stop loop
    catalogue[rad_key] = halfmass_rad #save to catalogue
    return catalogue

def max_ang_momentum(subhalo, catalogue):
    j_dir = np.zeros(3)
    r_max = 5*catalogue["SubhaloHalfmassRadStellar"][0]
    temp = subhalo[subhalo["r"] < r_max].copy(deep=True)
    m = np.array(temp["Masses"])
    p = np.array([np.array(temp["Vx"]*m), np.array(temp["Vy"]*m), np.array(temp["Vz"]*m)])
    r = np.array([np.array(temp["x"]), np.array(temp["y"]), np.array(temp["z"])])
    l = np.cross(np.transpose(r), np.transpose(p))
    J = np.sum(l, axis= 0)/np.sum(m)
    j_dir = J/lg.norm(J)

    catalogue["RotationAxisX"] = j_dir[0]
    catalogue["RotationAxisY"] = j_dir[1]
    catalogue["RotationAxisZ"] = j_dir[2]
    return catalogue

def rotational_vel(gas, dm, stars, catalogue):
    G = 4.3*10**(-3)
    r_max = 2.2*catalogue["SubhaloHalfmassRadStellar"]
    m_gas = gas[gas["r"] < r_max]["Masses"].sum()
    m_dm = dm[dm["r"] < r_max]["Masses"].sum()
    m_stars = stars[stars["r"] < r_max]["Masses"].sum()
    m_tot = m_gas + m_dm + m_stars
    catalogue["SubhaloRotVel_2_2Re"] = np.sqrt((G*m_tot)/r_max)
    return catalogue

def velocity_disp(stars, catalogue):
    sigma_x = np.array(stars["vx"]).std()
    sigma_y = np.array(stars["vy"]).std()
    sigma_z = np.array(stars["vz"]).std()
    sigma = (1/3)*(sigma_x + sigma_y + sigma_z) #this is not right
    catalogue["SubhaloVelDisp"] = sigma
    return catalogue

#def photometrics(stars, catalogue):
