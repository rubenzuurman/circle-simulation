"""
Run tests by executing  `python -m unittest test.test_visualization`.
Run linter by executing `pylint src/vizualization.py`.
"""
import unittest

from src.simulation import Simulation
from src.visualization import Visualization

class TestVisualization(unittest.TestCase):
    """
    Class for testing src/visualization.py
    """
    
    def test_init(self):
        """
        Test visualization.py __init__() function.
        """
        # Create new simulation.
        sim = Simulation(simulation_name="test_sim", delta_time=0.1, \
            max_time=1.0)
        
        # Initialize particles with random velocity.
        sim.initialize_particles(amount=5, spawn_range=((-1, 1), (-10, 10)), \
            random_velocity=True)
        
        # Run simulation.
        sim.run()
        
        # Create visualization.
        vis = Visualization(simulation_name="test_sim", \
            window_dimensions=(100, 100))
        
        # Test simulation name and window dimensions.
        self.assertEqual(vis.simulation_name, "test_sim")
        self.assertEqual(vis.window_width, 100)
        self.assertEqual(vis.window_height, 100)
        self.assertEqual(vis.window_dimensions, (100, 100))
        
        # Check if simdata is a dictionary (but not an empty dictionary), 
        # current chunk is equal to zero, timestep is equal to zero, display 
        # is not none, and clock is also not none.
        self.assertIsInstance(vis.simdata, dict)
        self.assertFalse(vis.simdata == {})
        self.assertFalse(vis.display is None)
        self.assertEqual(vis.current_chunk, 0)
        self.assertEqual(vis.timestep, 0)
        self.assertFalse(vis.clock is None)
        
        # Check if simulation properties contains the keys `indices` and 
        # `max_index`.
        self.assertIsInstance(vis.simprops, dict)
        self.assertTrue("indices" in vis.simprops.keys())
        self.assertTrue("max_index" in vis.simprops.keys())
