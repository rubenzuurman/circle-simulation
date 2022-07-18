"""
Run tests by executing  `python -m unittest test.test_simulation`.
Run linter by executing `pylint src/simulation.py`.
Test code import solution: https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure.
"""
import os
import pickle
import shutil
import unittest

from src.simulation import Simulation

class TestSimulation(unittest.TestCase):
    """
    Class for testing src/simulation.py
    """
    
    def test_init(self):
        """
        Test simulation.py __init__() function.
        """
        # Create temporary directory for tests.
        if os.path.exists("__temp_tests"):
            print("Please remove folder '__temp_tests' before running the " \
                "tests.")
            self.assertTrue(False)
            return
        os.mkdir("__temp_tests")
        
        # Create new simulation.
        sim = Simulation(simulation_name="test_sim", \
            saves_folder="__temp_tests", delta_time=1, max_time=2)
        
        # Test numerical variables.
        self.assertEqual(sim.time, 0)
        self.assertEqual(sim.timestep, 0)
        self.assertEqual(sim.delta_time, 1)
        self.assertEqual(sim.max_time, 2)
        self.assertFalse(sim.done)
        
        # Test iterable variables.
        self.assertIsInstance(sim.particles, list)
        self.assertIsInstance(sim.simdata, dict)
        
        # Delete temporary directory.
        shutil.rmtree("__temp_tests")
    
    def test_init_particles(self):
        """
        Test simulation.py initialize_particles() function.
        """
        # Create temporary directory for tests.
        if os.path.exists("__temp_tests"):
            print("Please remove folder '__temp_tests' before running the " \
                "tests.")
            self.assertTrue(False)
            return
        os.mkdir("__temp_tests")
        
        # Create new simulation.
        sim = Simulation(simulation_name="test_sim", \
            saves_folder="__temp_tests", delta_time=0.01, max_time=10.0)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=5, spawn_range=((-1, 1), (-10, 10)), \
            random_velocity=True, velocity_magnitude=10)
        
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
        for particle in sim.particles:
            # Unpack particle.
            id_, position, velocity, mass, radius = particle
            
            # Check if the velocity is zero.
            self.assertTrue(velocity[0] == 0 and velocity[1] == 0)
        
        # Delete temporary directory.
        shutil.rmtree("__temp_tests")
    
    def test_run(self):
        """
        Test simulation.py run() function.
        """
        # Create temporary directory for tests.
        if os.path.exists("__temp_tests"):
            print("Please remove folder '__temp_tests' before running the " \
                "tests.")
            self.assertTrue(False)
            return
        os.mkdir("__temp_tests")
        
        # Create new simulation.
        sim = Simulation(simulation_name="test_sim", \
            saves_folder="__temp_tests", delta_time=0.01, max_time=1)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=1, spawn_range=((-1, 1), (-1, 1)), \
            random_velocity=True, velocity_magnitude=10)
        
        # Check if the timing variables are correct.
        self.assertTrue(sim.time <= sim.max_time)
        self.assertFalse(sim.done)
        
        # Run until done.
        sim.run()
        
        # Check if the timing variables are correct.
        self.assertTrue(sim.time >= sim.max_time)
        self.assertEqual(sim.timestep, int(sim.max_time / sim.delta_time))
        self.assertTrue(sim.done)
        
        # Delete temporary directory.
        shutil.rmtree("__temp_tests")
    
    def test_update(self):
        """
        Test simulation.py update() function.
        """
        # Create temporary directory for tests.
        if os.path.exists("__temp_tests"):
            print("Please remove folder '__temp_tests' before running the " \
                "tests.")
            self.assertTrue(False)
            return
        os.mkdir("__temp_tests")
        
        # Create new simulation.
        sim = Simulation(simulation_name="test_sim", \
            saves_folder="__temp_tests", delta_time=0.01, max_time=1)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=1, spawn_range=((-1, 1), (-1, 1)), \
            random_velocity=True, velocity_magnitude=10)
        
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
        
        # Delete temporary directory.
        shutil.rmtree("__temp_tests")
    
    def test_collisions_scenario1(self):
        """
        This function is to test if the simulation still works as expected 
        after maybe optimizing some things.
        """
        # Initialize simulation settings.
        delta_time = 0.01
        max_time = 10
        amount = 250
        spawn_range = 200
        random_velocity = True
        velocity_magnitude = 10
        
        # Create and save simulation to test on.
        """sim = Simulation(simulation_name="original", \
            saves_folder="test/scenarios/scenario1_collisions_verification", \
            delta_time=delta_time, max_time=max_time)
        sim.initialize_particles(amount=amount, \
            spawn_range=((-spawn_range // 2, spawn_range // 2), \
                (-spawn_range // 2, spawn_range // 2)), \
            random_velocity=random_velocity, \
            velocity_magnitude=velocity_magnitude)
        with open("test/scenarios/scenario1_collisions_verification/" \
            "initial_state.pickle", "wb") as file:
            pickle.dump(sim, file)
        sim.run()
        return"""
        
        # Load simulation created by the code above.
        with open("test/scenarios/scenario1_collisions_verification/" \
            "initial_state.pickle", "rb") as file:
            original_sim_initial_state = pickle.load(file)
        
        # Create new simulation with the same settings.
        test_sim = Simulation(simulation_name="test", \
            saves_folder="test/scenarios/scenario1_collisions_verification", \
            delta_time=delta_time, max_time=max_time)
        test_sim.initialize_particles(amount=amount, \
            spawn_range=((-spawn_range // 2, spawn_range // 2), \
                (-spawn_range // 2, spawn_range // 2)), \
            random_velocity=random_velocity, \
            velocity_magnitude=velocity_magnitude)
        
        # Extract particles and update test_sim particles and initial 
        # timestep data.
        original_particles = original_sim_initial_state.particles
        test_sim.particles = original_particles
        test_sim.simdata[0]["particles"] = original_particles
        
        # Run test simulation.
        test_sim.run()
        
        # Load timestep0 from test simulation.
        with open("test/scenarios/scenario1_collisions_verification/" \
            "test/timestep0.pickle", "rb") as file:
            timestep0_test = pickle.load(file)
        
        # Load timestep0 from original simulation.
        with open("test/scenarios/scenario1_collisions_verification/" \
            "original/timestep0.pickle", "rb") as file:
            timestep0_original = pickle.load(file)
        
        # Code for printing collided particles for every timestep.
        """prev_timestep = 0
        counter = 0
        for timestep, data in timestep0_original.items():
            if counter == 0:
                prev_timestep = timestep
                counter += 1
                continue
            
            particles_prev = [particle[0] for particle \
                in timestep0_original[prev_timestep]["particles"]]
            particles_cur  = [particle[0] for particle \
                in timestep0_original[timestep]["particles"]]
            print(timestep, list(set(particles_prev) - set(particles_cur)))
            
            prev_timestep = timestep"""
        
        # Print if the results are equal.
        self.assertTrue(timestep0_test == timestep0_original)
