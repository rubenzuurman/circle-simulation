"""
Simulation class.
"""
import copy
import os
import pickle
import random as rnd

class Simulation:
    """
    Simulates the circles.
    """
    
    def __init__(self, simulation_name="sim", delta_time=0.01, max_time=10.0):
        """
        Initializes the simulation.
        Every particle is a list of the form 
            [id, position, velocity, mass, radius].
        """
        # Set simulation name member variable.
        self.simulation_name = simulation_name
        
        # Create simulation folder if does not exist.
        if not os.path.isdir(f"saves/{self.simulation_name}/"):
            os.mkdir(f"saves/{self.simulation_name}/")
        
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
    
    def initialize_particles(self, amount, spawn_range, random_velocity=True):
        """
        Initialize the particles list with `amount` number of randomly 
        positioned particles. The `spawn_range` parameter specifies the spawn 
        limits of the particles, it must be of the form 
            [[min_x, max_x], [min_y, max_y]].
        The velocities of the particles will be random (-1<=vx,vy<=1) if 
        `random_velocity` is equal to True, else the velocities will be zero.
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
                vel_x = rnd.randint(-1000, 1000) / 1000 * 10
                vel_y = rnd.randint(-1000, 1000) / 1000 * 10
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
            print(f"Simulating... {self.timestep}/{max_steps}", end="\r")
            self.update()
        print("\nSimulation done.")
    
    def update(self):
        """
        For now just update the position by the velocity.
        """
        # Update timing variables.
        if self.done or self.time >= self.max_time:
            self.done = True
            return
        
        self.timestep += 1
        self.time = self.timestep * self.delta_time
        
        # Update positions.
        for index, particle in enumerate(self.particles):
            # Unpack particle.
            velocity = particle[2]
            
            # Calculate scaled velocity.
            velocity_x_scaled = velocity[0] * self.delta_time
            velocity_y_scaled = velocity[1] * self.delta_time
            
            # Update position.
            self.particles[index][1][0] += velocity_x_scaled
            self.particles[index][1][1] += velocity_y_scaled
        
        # Save current state to simdata dictionary.
        self.simdata[self.timestep] = {"current_time": self.time, \
            "max_time": self.max_time, "timestep": self.timestep, \
            "number_of_particles": len(self.particles), \
            "particles": copy.deepcopy(self.particles)}
        
        # Check size of the simdata dictionary to see if it needs to be saved.
        total = [v["number_of_particles"] \
            for _, v in self.simdata.items()]
        if sum(total) > 4000:
            # Save data.
            filename = f"saves/{self.simulation_name}/" \
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
                filename = f"saves/{self.simulation_name}/" \
                    f"timestep{self.saved_counter-1}.pickle"
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        last_simdata = pickle.load(file)
                    
                    # Combine the loaded dictionary and currently active 
                    # dictionary by using the | operator.
                    self.simdata = last_simdata | self.simdata
                
                # Save to file.
                with open(filename, "wb") as file:
                    pickle.dump(self.simdata, file)
