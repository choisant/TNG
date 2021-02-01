import numpy as np
import numpy.linalg as lg

def relative_pos_radius(particles, N, catalogue):
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

    center_of_halo = np.zeros([N,3]) #list for saving the central positions for all subhalos
    for i in range(N):
        #find center of halo
        min_pot = 0 #all grav pot is <0
        for particle in particles: #look through all particle types for lowest potential
            #Find particle with lowest potential
            min_pot_value = particle[i]["Potential"].min()
            if min_pot_value < min_pot:
                min_pot = min_pot_value
                #Get particle position and assign as center of galaxy
                min_pot_pos = particle[i][particle[i]["Potential"] == min_pot_value]["Coordinates"].values[0]
        
        center_of_halo[i] = min_pot_pos
        #Calculate new coordinates
        for particle in particles:
            positions = np.array(list(particle[i]["Coordinates"].values))
            particle[i]["x"] = positions[:, 0] - min_pot_pos[0]
            particle[i]["y"] = positions[:, 1] - min_pot_pos[1]
            particle[i]["z"] = positions[:, 2] - min_pot_pos[2]
            particle[i]["r"] = radius(particle[i])
    #Save to group catalogue
    catalogue["SubhaloPosX"] = center_of_halo[:, 0]
    catalogue["SubhaloPosY"] = center_of_halo[:, 1]
    catalogue["SubhaloPosZ"] = center_of_halo[:, 2]


    return particles, catalogue

def galaxy_radius(stellar_particles, N, catalogue):

    #Decide on galaxy radius. 10% of total halo radius.
    max_rad = np.zeros(N)
    gal_rad = np.zeros(N)
    for i in range(N):
        max_rad[i] = np.array(stellar_particles[i]["r"].max())
    gal_rad = 0.1*max_rad
    catalogue["SubhaloGalaxyRad"] = gal_rad
    catalogue["SubhaloRad"] = max_rad

    return catalogue

def galaxy_stellar_mass(stellar_particles, N, catalogue):
    stellar_masses = np.zeros(N)
    for i in range(N):
        max_rad = catalogue["SubhaloGalaxyRad"][i]
        temp = stellar_particles[i][stellar_particles[i]["r"] < max_rad]
        stellar_masses[i] = temp["Masses"].sum()
    catalogue["SubhaloGalaxyMassStellar"] = stellar_masses
    return catalogue

def total_mass(particles, N, catalogue):
    """
    Calculate total mass for each particle type and saves it to the group catalogue
    """
    particle_mass = np.zeros([len(particles), N])
    p = 0
    for particle in particles:
        for i in range(N):
            particle_mass[p][i] = particle[i]["Masses"].sum() #or load from snapshot to save time
        p = p + 1
    mass_total = particle_mass.sum()

    #save value to catalogue
    catalogue["SubhaloMassGas"] = particle_mass[0]
    catalogue["SubhaloMassDM"] = particle_mass[1]
    catalogue["SubhaloMassStellar"] = particle_mass[2]
    catalogue["SubhaloMass"] = mass_total
    return particles, catalogue

def subhalo_velocity(particles, N, catalogue):
    """
    Calculates the mass weighted average velocity of the particles in a subhalo and save them to the group catalogue.
    """
    subhalo_velocities = np.zeros([N, 3]) #Empty list
    for i in range(N):
        v_m_sum = np.zeros([len(particles), 3]) #List for saving the sum of velocities*mass for each particle type
        j = 0
        masses = np.zeros(len(particles))
        for particle in particles:
            m = np.array(particle[i]["Masses"]) 
            masses[j] = np.sum(m)
            velocities = np.array(list(particle[i]["Velocities"].values))
            #Velocity times mass for each particle
            vx_m = velocities[:, 0]*m
            vy_m = velocities[:, 1]*m
            vz_m = velocities[:, 2]*m
            v_m_sum[j] = [vx_m.sum(), vy_m.sum(), vz_m.sum()]
            j = j + 1
        M_tot = masses.sum() #total mass of subhalo
        subhalo_velocities[i] = np.sum(v_m_sum, axis=0)/M_tot #Mass weighted average velocity
    #save to group catalogue
    catalogue["SubhaloVelX"] = subhalo_velocities[:, 0]
    catalogue["SubhaloVelY"] = subhalo_velocities[:, 1]
    catalogue["SubhaloVelZ"] = subhalo_velocities[:, 2]
    return particles, catalogue

def relative_velocities(particle, N, catalogue):
    """
    Adds the relative velocity to the dataframes of a chosen particle type.
    """
    central_vel = np.zeros([N,3]) #empty list
    for i in range (N):
        vel_av = [catalogue["SubhaloVelX"][i], catalogue["SubhaloVelY"][i], catalogue["SubhaloVelZ"][i]]
        velocities = np.array(list(particle[i]["Velocities"].values))
        vx = velocities[:, 0]
        vy = velocities[:, 1]
        vz = velocities[:, 2]
        #Subtracts subhalo velocity from global velocities to get local velocities
        particle[i]["Vx"] = vx - vel_av[0]
        particle[i]["Vy"] = vy - vel_av[1]
        particle[i]["Vz"] = vz - vel_av[2]
    return particle

def half_mass_radius(particle, N, catalogue, particle_type="Stellar"):
    """
    Calculates half mass radius for a certain particle type and adds it to the group catalogue.
    """
    halfmass_rad = np.zeros(N) #empty list
    mass_key = "SubhaloMass" + particle_type
    rad_key = "SubhaloHalfmassRad" + particle_type
    for i in range(N):
        temp = particle[i].copy(deep=True)
        temp.sort_values(by="r", inplace = True) #sort particles by radius
        temp = temp.reset_index(drop=True)
        temp_mass = 0
        #Start adding the masses of all particles starting with smallest radius
        for j in range(len(temp["r"])):
            #Check if total mass is less than half total particle mass
            if temp_mass < (catalogue[mass_key][i]/2):
                temp_mass = temp_mass + temp["Masses"][j] #Add mass of next particle
            else:
                #Add half mass radius.
                #Some uncertainty on calculation method here, now center of mass between particle j and j-i.
                m1 = temp["Masses"][j-1]
                m2 = temp["Masses"][j]
                M = m1+m2
                halfmass_rad[i] = (m1*temp["r"][j-1] + m2*temp["r"][j])/M
                break  #stop loop
    catalogue[rad_key] = halfmass_rad #save to catalogue
    return particle, catalogue

def max_ang_momentum(particle, N, catalogue):
    j_dir = np.zeros([N, 3])
    for i in range(N):
        r_max = 5*catalogue["SubhaloHalfmassRadStellar"][i]
        temp = particle[i][particle[i]["r"] < r_max].copy(deep=True)
        m = np.array(temp["Masses"])
        p = np.array([np.array(temp["Vx"]*m), np.array(temp["Vy"]*m), np.array(temp["Vz"]*m)])
        r = np.array([np.array(temp["x"]), np.array(temp["y"]), np.array(temp["z"])])
        l = np.cross(np.transpose(r), np.transpose(p))
        J = np.sum(l, axis= 0)/np.sum(m)
        j_dir[i] = J/lg.norm(J)

    catalogue["RotationAxisX"] = [item[0] for item in j_dir]
    catalogue["RotationAxisY"] = [item[1] for item in j_dir]
    catalogue["RotationAxisZ"] = [item[2] for item in j_dir]
    return catalogue