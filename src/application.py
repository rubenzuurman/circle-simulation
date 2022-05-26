from simulation import Simulation
from visualization import Visualization

def main():
    # Run simulation.
    sim = Simulation(max_time=100.0)
    sim.initialize_particles(amount=10, spawn_range=((-100, 100), (-100, 100)))
    sim.run()
    
    # Run visualizer.
    vis = Visualization("sim", (1920, 1080))
    vis.run(60)

if __name__ == "__main__":
    main()