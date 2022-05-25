from simulation import Simulation

def main():
    # Run simulation.
    sim = Simulation(max_time=100.0)
    sim.initialize_particles(amount=10, spawn_range=((-10, 10), (-10, 10)))
    sim.run()
    
    # Run visualizer.

if __name__ == "__main__":
    main()