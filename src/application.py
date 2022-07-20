from simulation import Simulation
from visualization import Visualization

import os
import pickle

delta_time = 0.025
delta_time_string = "0_025"
max_time = 500
number_of_particles = 125
spawn_size = 20000
start_velocity_magnitude = 5

def read_timing_data(simulation_name):
    filename = f"saves/{simulation_name}/timing.pickle"
    with open(filename, "rb") as file:
        d = pickle.load(file)
    
    timing = 0
    gravity = 0
    positions = 0
    collisions = 0
    save_checking = 0
    total_update_time = 0
    for timestep, data in d.items():
        timing_variables_time = data['gravity_start'] - data['update_start']
        gravity_time = data['positions_start'] - data['gravity_start']
        positions_time = data['collisions_start'] - data['positions_start']
        collisions_time = data['done_start'] - data['collisions_start']
        save_checking_time = data['update_end'] - data['done_start']
        
        timing += timing_variables_time
        gravity += gravity_time
        positions += positions_time
        collisions += collisions_time
        save_checking += save_checking_time
        total_update_time += data['update_end']
    
    total_time = timing + gravity + positions + collisions + save_checking
    misc_time = total_update_time - total_time
    print(f"Timing\t\t{timing / total_update_time * 100:.2f}%")
    print(f"Gravity\t\t{gravity / total_update_time * 100:.2f}%")
    print(f"Positions\t{positions / total_update_time * 100:.2f}%")
    print(f"Collisions\t{collisions / total_update_time * 100:.2f}%")
    print(f"Save checking\t{save_checking / total_update_time * 100:.2f}%")
    print(f"Misc\t\t{misc_time / total_update_time * 100:.2f}%")
    print(f"Total time taken: {total_update_time / 1000000000:.3f} s")

def create_new_simulation(sim_name):
    # Enable global variables.
    global delta_time, delta_time_string, max_time, number_of_particles, \
        spawn_size, start_velocity_magnitude
    
    # Create simulation.
    sim = Simulation(simulation_name=sim_name, delta_time=delta_time, \
        max_time=max_time)
    
    # Initialize particles.
    sim.initialize_particles(amount=number_of_particles, \
        spawn_range=((-spawn_size // 2, spawn_size // 2), \
            (-spawn_size // 2, spawn_size // 2)), \
        random_velocity=True, velocity_magnitude=start_velocity_magnitude)
    
    # Return simulation.
    return sim

def run_simulation(sim):
    # Run simulation.
    sim.run()
    
    # Return simulation.
    return sim

def main():
    # Tested the consistency of the simulation generation by generating it 
    # twice from the same starting simulation object and verifying that the 
    # results were identical by loading in the timestep pickle files one by 
    # one and comparing them (the result was True).
    """
    WHAT YOU SHOULD DO TO TEST COLLISIONS AND PERFORMANCE:
        - Create simulation and initialize particles, then serialize it.
        - Load simulation by deserializing.
        - Run simulation to test collision code performance and correctness 
            and to test gravity calculation code performance.
    """
    
    # Generate simulation name.
    benchmark_sim = True
    only_visualize = True
    
    global delta_time, delta_time_string, max_time, number_of_particles, \
        spawn_size, start_velocity_magnitude
    sim_name = f"delta{delta_time_string}-maxtime{max_time}" \
        f"-amount{number_of_particles}-spawn{spawn_size}x{spawn_size}" \
        f"-startvel{start_velocity_magnitude}-g10-optim1-test"
    
    if benchmark_sim:
        sim_name = f"benchmarksim_{sim_name}"
    
    # Check if the simulation already exists.
    uniqifier = 0
    while os.path.isdir(f"saves/{sim_name}_{uniqifier}/"):
        uniqifier += 1
    
    if only_visualize:
        uniqifier -= 1
    
    sim_name = f"{sim_name}_{uniqifier}"
    
    # Create simulation.
    #sim = create_new_simulation(sim_name)
    
    #with open("saves/test_sim.pickle", "wb") as file:
    #    pickle.dump(sim, file)
    
    # Run simulation.
    #sim = run_simulation(sim)
    
    # Create simulation.
    """sim = Simulation(simulation_name=sim_name, delta_time=delta_time, \
        max_time=max_time)
    sim.initialize_particles(amount=number_of_particles, \
        spawn_range=((-spawn_size // 2, spawn_size // 2), \
            (-spawn_size // 2, spawn_size // 2)), \
        random_velocity=True, velocity_magnitude=start_velocity_magnitude)"""
    
    # Create test simulation.
    #with open("saves/test_simulation.pickle", "wb") as file:
    #    pickle.dump(sim, file)
    
    # Load test simulation.
    #with open("saves/test_simulation.pickle", "rb") as file:
    #    sim = pickle.load(file)
    
    # Run simulation.
    #sim.run()
    
    """
    Save simulation, save collisions with time.
    Verify in test scenario: load simulation, check collisions
    """
    
    """collision_dict = {}
    
    for t, c in sim.collision_tracker:
        print(f"{t:.2f} {c}")
        collision_dict[round(t, 2)] = c
    
    with open("saves/test_sim_collisions.pickle", "wb") as file:
        pickle.dump(collision_dict, file)"""
    
    # Show timing data.
    read_timing_data(sim_name)
    
    # Run visualizer.
    vis = Visualization(sim_name, (1920, 1080))
    vis.run(120)

if __name__ == "__main__":
    main()