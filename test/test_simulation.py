import unittest

from src.simulation import Simulation

class TestSimulation(unittest.TestCase):
    
    def test_init(self):
        # Create new simulation.
        sim = Simulation(delta_time=1, max_time=2)
        
        # Test numerical variables.
        self.assertEqual(sim.time, 0)
        self.assertEqual(sim.timestep, 0)
        self.assertEqual(sim.delta_time, 1)
        self.assertEqual(sim.max_time, 2)
        self.assertFalse(sim.done)
        
        # Test iterable variables.
        self.assertIsInstance(sim.particles, list)
        self.assertIsInstance(sim.simdata, dict)
    
    def test_init_particles(self):
        # Create new simulation.
        sim = Simulation()
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=5, spawn_range=((-1, 1), (-10, 10)), \
            random_velocity=True)
        
        # Test particles list.
        self.assertIsInstance(sim.particles, list)
        self.assertEqual(len(sim.particles), 5)
        
        # Iterate over all particles.
        for particle in sim.particles:
            # Unpack particle.
            id_, position, velocity, mass, radius = particle
            
            # Check if id_ is greater than or equal to zero and is an integer.
            self.assertIsInstance(id_, int)
            self.assertTrue(id_ >= 0)
            
            # Check x range.
            self.assertTrue(-1 <= position[0] <= 1)
            
            # Check y range.
            self.assertTrue(-10 <= position[1] <= 10)
            
            # Check if the velocity is nonzero.
            self.assertTrue(not velocity[0] == 0 or not velocity[1] == 0)
            
            # Check if the mass equals one.
            self.assertEqual(mass, 1)
            
            # Check if the radius equals one.
            self.assertEqual(radius, 1)
        
        # Initialize particles with zero velocity.
        sim.initialize_particles(amount=5, spawn_range=((-1, 1), (-10, 10)), \
            random_velocity=False)
        
        # Iterate over all particles.
        velocities = []
        for particle in sim.particles:
            # Unpack particle.
            id_, position, velocity, mass, radius = particle
            
            # Check if the velocity is zero.
            self.assertTrue(velocity[0] == 0 and velocity[1] == 0)
    
    def test_run(self):
        # Create new simulation.
        sim = Simulation(delta_time=0.01, max_time=1)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=1, spawn_range=((-1, 1), (-1, 1)), \
            random_velocity=True)
        
        # Check if the timing variables are correct.
        self.assertTrue(sim.time <= sim.max_time)
        self.assertFalse(sim.done)
        
        # Run until done.
        sim.run()
        
        # Check if the timing variables are correct.
        self.assertTrue(sim.time >= sim.max_time)
        self.assertEqual(sim.timestep, int(sim.max_time / sim.delta_time))
        self.assertTrue(sim.done)
    
    def test_update(self):
        # Create new simulation.
        sim = Simulation(delta_time=0.01, max_time=1)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=1, spawn_range=((-1, 1), (-1, 1)), \
            random_velocity=True)
        
        # Save current timing variables.
        time = sim.time
        timestep = sim.timestep
        delta_time = sim.delta_time
        max_time = sim.max_time
        done = sim.done
        
        # Save current particle position.
        position = sim.particles[0][1][:]
        velocity = sim.particles[0][2][:]
        
        # Update simulation.
        sim.update()
        
        # Check if the timing variables are correct.
        self.assertEqual(sim.time, time + sim.delta_time)
        self.assertEqual(sim.timestep, timestep + 1)
        self.assertEqual(sim.delta_time, delta_time)
        self.assertEqual(sim.max_time, max_time)
        self.assertEqual(sim.done, done)
        
        # Check if the new position is correct.
        new_position = sim.particles[0][1]
        new_position_prediction = \
            [position[0] + sim.delta_time * velocity[0], \
             position[1] + sim.delta_time * velocity[1]]
        
        self.assertTrue(\
            abs(new_position_prediction[0] - new_position[0]) < 0.000000001)
        self.assertTrue(\
            abs(new_position_prediction[1] - new_position[1]) < 0.000000001)
