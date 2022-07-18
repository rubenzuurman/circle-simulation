"""
Simulation class.
"""
import copy
import math
import os
import pickle
import random as rnd
import time

class Simulation:
    """
    Simulates the circles.
    """
    
    def __init__(self, simulation_name="sim", saves_folder="saves", \
        delta_time=0.01, max_time=10.0):
        """
        Initializes the simulation.
        Every particle is a list of the form 
            [id, position, velocity, mass, radius].
        """
        # Set simulation name member variable.
        self.simulation_name = simulation_name
        self.saves_folder = saves_folder
        
        # Create simulation folder if does not exist.
        if not os.path.isdir(f"{self.saves_folder}/{self.simulation_name}/"):
            os.mkdir(f"{self.saves_folder}/{self.simulation_name}/")
        
        # Initialize list of particles.
        self.particles = []
        
        # Initialize timing variables.
        self.time = 0
        self.timestep = 0
        self.delta_time = delta_time
        self.max_time = max_time
        self.done = False
        
        # Initialize simulation data dictionary.
        self.simdata = {}
        
        # Counts the number of times the simulation has been saved. This will 
        # be used in the names of the save files.
        self.saved_counter = 0
        
        self.timing_data = {}
        
        self.collision_tracker = []
    
    def initialize_particles(self, amount, spawn_range, \
        random_velocity=True, velocity_magnitude=10):
        """
        Initialize the particles list with `amount` number of randomly 
        positioned particles. The `spawn_range` parameter specifies the spawn 
        limits of the particles, it must be of the form 
            [[min_x, max_x], [min_y, max_y]].
        The velocities of the particles will be random 
        (-velocity_magnitude<=vx,vy<=velocity_magnitude) if `random_velocity` 
        is equal to True, else the velocities will be zero.
        """
        # Initialize particles list.
        self.particles = []
        
        # Extract spawn limits.
        min_x, max_x = spawn_range[0]
        min_y, max_y = spawn_range[1]
        
        # Add particles.
        for id_ in range(amount):
            # Calculate random position.
            pos_x = rnd.randint(min_x * 100, max_x * 100) / 100
            pos_y = rnd.randint(min_y * 100, max_y * 100) / 100
            
            # Calculate random or zero velocity.
            if random_velocity:
                vel_x = rnd.randint(-1000, 1000) / 1000 * velocity_magnitude
                vel_y = rnd.randint(-1000, 1000) / 1000 * velocity_magnitude
            else:
                vel_x = 0
                vel_y = 0
            
            # Calculate radius and mass.
            radius = 1
            mass = radius ** 2
            
            # Add particle to list.
            self.particles.append([id_, [pos_x, pos_y], [vel_x, vel_y], \
                mass, radius])
        
        # Save current state to simdata dictionary.
        self.simdata[self.timestep] = {"current_time": self.time, \
            "max_time": self.max_time, "timestep": self.timestep, \
            "number_of_particles": len(self.particles), \
            "particles": self.particles}
    
    def run(self):
        """
        Executes the update function until the `done` variable is equal to 
        True.
        """
        max_steps = int(self.max_time / self.delta_time)
        print(f"Simulating... 0/{max_steps}", end="\r")
        while not self.done:
            print(f"Simulating... {self.timestep}/{max_steps} " \
                f"({len(self.particles)} particles)", end="\r")
            self.update()
        print("\nSimulation done.")
        
        with open(f"{self.saves_folder}/{self.simulation_name}/timing.pickle", "wb") as file:
            pickle.dump(self.timing_data, file)
    
    def update(self):
        """
        Update the position by adding the velocity. Check for collisions and 
        merge particles if they collide.
        """
        update_start = time.time_ns()
        
        # Update timing variables.
        if self.done or self.time >= self.max_time:
            self.done = True
            return
        
        self.timestep += 1
        self.time = self.timestep * self.delta_time
        
        gravity_start = time.time_ns()
        # Calculate gravitational force of every particle.
        G = 10
        for particle1 in self.particles:
            acceleration_x = 0
            acceleration_y = 0
            for particle2 in self.particles:
                if particle1[0] == particle2[0]:
                    continue
                
                # Calculate vector from particle1 to particle2.
                difference_vector = [particle2[1][0] - particle1[1][0], \
                    particle2[1][1] - particle1[1][1]]
                
                # Calculate distance squared.
                distance_sq = difference_vector[0] * difference_vector[0] \
                    + difference_vector[1] * difference_vector[1]
                distance = math.sqrt(distance_sq)
                
                # Calculate unit direction vector.
                unit_difference_vector = [difference_vector[0] / distance, \
                    difference_vector[1] / distance]
                acceleration_x += G * particle2[3] \
                    / distance_sq * unit_difference_vector[0]
                acceleration_y += G * particle2[3] \
                    / distance_sq * unit_difference_vector[1]
            
            particle1[2][0] += acceleration_x
            particle1[2][1] += acceleration_y
        
        positions_start = time.time_ns()
        # Update positions.
        for particle in self.particles:
            # Unpack particle.
            _, position, velocity, _, _ = particle
            
            # Calculate scaled velocity.
            velocity_x_scaled = velocity[0] * self.delta_time
            velocity_y_scaled = velocity[1] * self.delta_time
            
            # Update position.
            #self.particles[index][1][0] += velocity_x_scaled
            #self.particles[index][1][1] += velocity_y_scaled
            position[0] += velocity_x_scaled
            position[1] += velocity_y_scaled
        
        collisions_start = time.time_ns()
        # Collect collisions.
        collisions = []
        particles_sorted = sorted(self.particles, key=lambda x: x[0])
        for particle1 in particles_sorted:
            for particle2 in particles_sorted:
                # Cut the comparison matrix in half.
                if particle2[0] <= particle1[0]:
                    continue
                
                # Extract components.
                # id, pos, vel, mass, radius
                id1, p1, v1, m1, r1 = particle1
                id2, p2, v2, m2, r2 = particle2
                
                # Calculate distance squared.
                distance_x = p1[0] - p2[0]
                if distance_x > r1 + r2:
                    continue
                
                distance_y = p1[1] - p2[1]
                if distance_y > r1 + r2:
                    continue
                
                distance_sq = distance_x * distance_x + distance_y * distance_y
                
                # If the distance is less than r1+r2 there is a collision.
                if distance_sq <= (r1 + r2) * (r1 + r2):
                    collision_merged = False
                    for collision in collisions:
                        if id1 in collision and id2 not in collision:
                            collision.append(id2)
                            collision_merged = True
                            break
                        if id2 in collision and id1 not in collision:
                            collision.append(id1)
                            collision_merged = True
                            break
                        if id1 in collision and id2 in collision:
                            collision_merged = True
                            break
                    
                    if not collision_merged:
                        collisions.append([id1, id2])
        
        #if len(collisions) > 0:
        #    self.collision_tracker.append([self.time, collisions])
        
        # Create new particles list containing all particles that are not 
        # undergoing a collision.
        new_particles = []
        for particle in self.particles:
            in_collision = False
            for collision in collisions:
                if particle[0] in collision:
                    in_collision = True
                    break
            if not in_collision:
                new_particles.append(particle)
        
        # Append new particles after applying collision rules.
        for collision in collisions:
            # Get new particle id.
            new_id = min(collision)
            
            # Create particles list for this collision.
            colliding_particles = []
            for id_ in collision:
                for particle in self.particles:
                    if particle[0] == id_:
                        colliding_particles.append(particle)
                        break
            
            # Get average position, new velocity from conservation of 
            # momentum, new mass, and new radius.
            total_position_x = 0
            total_position_y = 0
            total_momentum_x = 0
            total_momentum_y = 0
            total_mass  = 0
            for particle in colliding_particles:
                id_, position, velocity, mass, radius = particle
                total_position_x += position[0] * mass
                total_position_y += position[1] * mass
                total_momentum_x += velocity[0] * mass
                total_momentum_y += velocity[1] * mass
                total_mass += mass
            
            # Construct new position.
            new_position_x = total_position_x / total_mass
            new_position_y = total_position_y / total_mass
            new_position = [new_position_x, new_position_y]
            
            # Construct new velocity.
            new_velocity_x = total_momentum_x / total_mass
            new_velocity_y = total_momentum_y / total_mass
            new_velocity = [new_velocity_x, new_velocity_y]
            
            # Construct new mass and radius.
            new_mass = total_mass
            new_radius = math.sqrt(total_mass)
            
            # Construct new particle.
            new_particle = [new_id, new_position, new_velocity, new_mass, \
                new_radius]
            
            # Add new particle to new particles list.
            new_particles.append(new_particle)
        
        # Replace self.particles with new_particle.
        self.particles = copy.deepcopy(new_particles)
        
        # Save current state to simdata dictionary.
        self.simdata[self.timestep] = {"current_time": self.time, \
            "max_time": self.max_time, "timestep": self.timestep, \
            "number_of_particles": len(self.particles), \
            "particles": copy.deepcopy(self.particles)}
        
        done_start = time.time_ns()
        
        # Check size of the simdata dictionary to see if it needs to be saved.
        total = [v["number_of_particles"] \
            for _, v in self.simdata.items()]
        if sum(total) > 500000:
            # Save data.
            filename = f"{self.saves_folder}/{self.simulation_name}/" \
                f"timestep{self.saved_counter}.pickle"
            with open(filename, "wb") as file:
                pickle.dump(self.simdata, file)
            
            # Reset dict and increment saved counter.
            self.simdata = {}
            self.saved_counter += 1
        else:
            # If the maximum size was not hit but the next update will 
            # terminate the simulation, the data will be appended to the last 
            # save file.
            if self.time >= self.max_time:
                # Load last save file if it exists.
                filename = f"{self.saves_folder}/{self.simulation_name}/" \
                    f"timestep{self.saved_counter-1}.pickle"
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        last_simdata = pickle.load(file)
                    
                    # Combine the loaded dictionary and currently active 
                    # dictionary by using the | operator.
                    self.simdata = last_simdata | self.simdata
                
                # File does not exist, edit filename so that it's valid.
                filename = f"{self.saves_folder}/{self.simulation_name}/" \
                    f"timestep{self.saved_counter}.pickle"
                
                # Save to file.
                with open(filename, "wb") as file:
                    pickle.dump(self.simdata, file)
        
        update_end = time.time_ns()
        
        self.timing_data[self.timestep] = {"update_start": update_start - update_start, \
            "gravity_start": gravity_start - update_start, \
            "positions_start": positions_start - update_start, \
            "collisions_start": collisions_start - update_start, \
            "done_start": done_start - update_start, \
            "update_end": update_end - update_start}
