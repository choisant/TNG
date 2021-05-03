import numpy as np
import numpy.linalg as lg
import illustris_python as il
import physics

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
    if len(positions) > 1:
        subhalo["x"] = positions[:, 0] - catalogue["SubhaloPosX"][0]
        subhalo["y"] = positions[:, 1] - catalogue["SubhaloPosY"][0]
        subhalo["z"] = positions[:, 2] - catalogue["SubhaloPosZ"][0]
        subhalo["r"] = radius(subhalo)
    else:
        subhalo["x"] = np.array([0])
        subhalo["y"] = np.array([0])
        subhalo["z"] = np.array([0])
        subhalo["r"] = np.array([0])

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
    catalogue["SubhaloRad200"] = radius_200
    catalogue["SubhaloMass200"] = np.array(df_central_halos["Group_M_Crit200"])

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
    return catalogue

def relative_velocities(subhalo, catalogue):
    """
    Adds the relative velocity to the dataframes of a chosen particle type.
    """
    vel_av = [catalogue["SubhaloVelX"][0], catalogue["SubhaloVelY"][0], catalogue["SubhaloVelZ"][0]]
    velocities = np.array(list(subhalo["Velocities"].values))
    if len(velocities) > 1:
        vx = velocities[:, 0]
        vy = velocities[:, 1]
        vz = velocities[:, 2]
        #Subtracts subhalo velocity from global velocities to get local velocities
        subhalo["Vx"] = vx - vel_av[0]
        subhalo["Vy"] = vy - vel_av[1]
        subhalo["Vz"] = vz - vel_av[2]
    else:
        subhalo["Vx"] = np.array([0])
        subhalo["Vy"] = np.array([0])
        subhalo["Vz"] = np.array([0])
    return subhalo

def half_mass_radius(subhalo, catalogue, rad_key):
    """
    Calculates stellar half mass radius for a certain particle type and adds it to the group catalogue.
    """
    temp = subhalo.copy(deep=True)
    temp.sort_values(by="r", inplace=True) #sort particles by radius
    temp = temp.reset_index(drop=True)
    temp_mass = 0
    #Start adding the masses of all particles starting with smallest radius
    for j in range(len(temp["r"])):
        #Check if total mass is less than half total particle mass
        if temp_mass < (catalogue["SubhaloMassStellar" + rad_key][0]/2):
            temp_mass = temp_mass + temp["Masses"][j] #Add mass of next particle
        else:
            #Add half mass radius.
            #Some uncertainty on calculation method here, now center of mass between particle j and j-i.
            m1 = temp["Masses"][j-1]
            m2 = temp["Masses"][j]
            M = m1+m2
            halfmass_rad = (m1*temp["r"][j-1] + m2*temp["r"][j])/M
            break  #stop loop
        halfmass_rad = temp["r"][j]
    catalogue["SubhaloHalfmassRadStellar" + rad_key] = halfmass_rad #save to catalogue
    return catalogue

def ang_momentum(subhalo, catalogue, rad_key):
    r_max = 2*catalogue["SubhaloHalfmassRadStellar" + rad_key][0]
    temp1 = subhalo[subhalo["r"] > 0] #remove central particle
    temp = temp1[temp1["r"] < r_max].copy(deep=True)
    m = np.array(temp["Masses"])
    p = np.array([np.array(temp["Vx"]*m), np.array(temp["Vy"]*m), np.array(temp["Vz"]*m)])
    r = np.array([np.array(temp["x"]), np.array(temp["y"]), np.array(temp["z"])])
    l = np.cross(np.transpose(r), np.transpose(p))
    L = np.sum(l, axis=0)
    J = np.sum(l, axis=0)/np.sum(m)
    catalogue["AngularMomentumX" + rad_key] = L[0]
    catalogue["AngularMomentumY" + rad_key] = L[1]
    catalogue["AngularMomentumZ" + rad_key] = L[2]

    catalogue["SpecificAngularMomentumX" + rad_key] = J[0]
    catalogue["SpecificAngularMomentumY" + rad_key] = J[1]
    catalogue["SpecificAngularMomentumZ" + rad_key] = J[2]
    return catalogue

def rot_energy(subhalo, catalogue, rad_key):
    rot_vector = np.transpose(np.array([catalogue["AngularMomentumX" + rad_key][0],
        catalogue["AngularMomentumY" + rad_key][0],
        catalogue["AngularMomentumZ" + rad_key][0]]))
    
    subhalo_rot = physics.geometry.rotate_pos_vel(subhalo, rot_vector)
    subhalo_rot = subhalo_rot[subhalo_rot["r"] > 0]
    v = np.array([np.array(subhalo_rot["Vx"]), np.array(subhalo_rot["Vy"]), np.array(subhalo_rot["Vz"])])
    V = (v[0]**2 + v[1]**2 + v[2]**2)**(1/2)
    r = np.array([np.array(subhalo_rot["x"]), np.array(subhalo_rot["y"]), np.array(subhalo_rot["z"])])
    R = (r[0]**2 + r[1]**2)**(1/2)
    m = np.array(subhalo_rot["Masses"])
    j = np.cross(np.transpose(r), np.transpose(v)) #gives angular momentum about origo, but about z axis for j_z
    j_z = np.transpose(j)[2]
    E_rot = 0.5*m*(j_z/R)**2
    E_kin = 0.5*m*V**2
    catalogue["RotationalEnergy" + rad_key] = np.sum(E_rot)
    catalogue["KineticEnergy" + rad_key] = np.sum(E_kin)
    catalogue["Kappa_rot" + rad_key] = np.sum((j_z/R)**2)/np.sum(V**2)
    return catalogue

def rotational_vel(gas, dm, stars, catalogue, r_vel, v_key="SubhaloRotVel"):
    """
    Calculates dynamical velocity at radius r_vel.
    """
    G = 4.3*10**(-3)
    m_gas = gas[gas["r"] < r_vel]["Masses"].sum()
    m_dm = dm[dm["r"] < r_vel]["Masses"].sum()
    m_stars = stars[stars["r"] < r_vel]["Masses"].sum()
    m_tot = (m_gas + m_dm + m_stars)*10**10
    catalogue[v_key] = np.sqrt((G*m_tot)/(r_vel*1000))
    return catalogue

def velocity_disp_3D(particle, catalogue, radius, vd_key="SubhaloVelDisp3D"):
    temp = particle[particle["r"] < radius]
    sigma_x = np.array(temp["Vx"]).std()
    sigma_y = np.array(temp["Vy"]).std()
    sigma_z = np.array(temp["Vz"]).std()
    sigma = np.sqrt((sigma_x**2 + sigma_y**2 + sigma_z**2))
    catalogue[vd_key] = sigma
    return catalogue

def velocity_disp_projected_stars(stars, catalogue, rad_key, vd_key="SubhaloVelDispReProjected"):
    #xy
    temp = stars.copy(deep=True)
    temp_cat = catalogue.copy(deep=True)
    temp["r"] = (temp["x"]**2 + temp["y"]**2)**(1/2)
    temp_cat = half_mass_radius(temp, temp_cat, rad_key)
    catalogue["SubhaloHalfmassRad_xy" + rad_key] = temp_cat["SubhaloHalfmassRadStellar" + rad_key]
    r_half = temp_cat["SubhaloHalfmassRadStellar" + rad_key][0]
    temp = temp[temp["r"] < r_half]
    sigma_z = np.array(temp["Vz"]).std()

    #xz
    temp = stars.copy(deep=True)
    temp_cat = catalogue.copy(deep=True)
    temp["r"] = (temp["x"]**2 + temp["z"]**2)**(1/2)
    temp_cat = half_mass_radius(temp, temp_cat, rad_key)
    catalogue["SubhaloHalfmassRad_xz" + rad_key] = temp_cat["SubhaloHalfmassRadStellar" + rad_key]
    r_half = temp_cat["SubhaloHalfmassRadStellar" + rad_key][0]
    temp = temp[temp["r"] < r_half]
    sigma_y = np.array(temp["Vy"]).std()

    #yz
    temp = stars.copy(deep=True)
    temp_cat = catalogue.copy(deep=True)
    temp["r"] = (temp["y"]**2 + temp["z"]**2)**(1/2)
    temp_cat = half_mass_radius(temp, temp_cat, rad_key)
    catalogue["SubhaloHalfmassRad_yz" + rad_key] = temp_cat["SubhaloHalfmassRadStellar" + rad_key]
    r_half = temp_cat["SubhaloHalfmassRadStellar" + rad_key][0]
    temp = temp[temp["r"] < r_half]
    sigma_x = np.array(temp["Vx"]).std()

    catalogue[vd_key] = ((1/3)*(sigma_z**2 + sigma_y**2 + sigma_x**2))**(1/2)
    return catalogue

def photometrics(stars, catalogue, rad_key):
    luminosities_g = 10**(-0.4*stars["StellarPhotometrics_g"]) #Drop zero points as it falls out in conversion back to mag
    luminosities_r = 10**(-0.4*stars["StellarPhotometrics_r"])
    luminosities_i = 10**(-0.4*stars["StellarPhotometrics_i"])
    luminosities_z = 10**(-0.4*stars["StellarPhotometrics_z"])
    g_band = -2.5*np.log10(luminosities_g.sum())
    r_band = -2.5*np.log10(luminosities_r.sum())
    i_band = -2.5*np.log10(luminosities_i.sum())
    z_band = -2.5*np.log10(luminosities_z.sum())
    catalogue["SubhaloStellarPhotometrics_g" + rad_key] = g_band
    catalogue["SubhaloStellarPhotometrics_r" + rad_key] = r_band
    catalogue["SubhaloStellarPhotometrics_i" + rad_key] = i_band
    catalogue["SubhaloStellarPhotometrics_z" + rad_key] = z_band
    return catalogue
