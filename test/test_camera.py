"""
Run tests by executing  `python -m unittest test.test_camera`.
Run linter by executing `pylint src/camera.py`.
"""
import copy
import math
import unittest

from src.camera import Camera

class TestCamera(unittest.TestCase):
    
    def test_init(self):
        # Create camera.
        camera = Camera(position=(0, 0), zoom=1)
        
        # Check if position, zoom, and zoom_target are set correctly.
        self.assertEqual(camera.position, [0, 0])
        self.assertEqual(camera.zoom, 1)
        self.assertEqual(camera.zoom_target, 1)
    
    def test_update(self):
        # Create camera.
        camera = Camera(position=(0, 0), zoom=1)
        
        # Test update with all combinations of movement keys.
        sqrt2 = math.sqrt(2) / 2
        tests = [
            [True, False, False, False, False, False],
            [False, True, False, False, False, False],
            [False, False, True, False, False, False],
            [False, False, False, True, False, False],
            
            [True, True, False, False, False, False],
            [True, False, True, False, False, False],
            [True, False, False, True, False, False],
            [False, True, True, False, False, False],
            [False, True, False, True, False, False],
            [False, False, True, True, False, False],
            
            [True, True, True, False],
            [True, True, False, True],
            [True, False, True, True],
            [False, True, True, True],
            
            [True, True, True, True]
        ]
        expected_position_change = [
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 0),
            
            (-1 * sqrt2, 1 * sqrt2),
            (0, 0),
            (1 * sqrt2, 1 * sqrt2),
            (-1 * sqrt2, -1 * sqrt2),
            (0, 0),
            (1 * sqrt2, -1 * sqrt2),
            
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
            
            (0, 0)
        ]
        
        for function_input, expected_output in zip(tests[0:4], expected_position_change[0:4]):
            camera_pos_before = copy.deepcopy(camera.get_position())
            camera.update(delta_time=1, keys_pressed=function_input)
            camera_pos_after  = copy.deepcopy(camera.get_position())
            
            dx = camera_pos_after[0] - camera_pos_before[0]
            dy = camera_pos_after[1] - camera_pos_before[1]
            
            if expected_output[0] < 0:
                self.assertTrue(camera.speed * expected_output[0] * 0.99 >= dx)
                self.assertTrue(camera.speed * expected_output[0] * 1.01 <= dx)
            else:
                self.assertTrue(camera.speed * expected_output[0] * 0.99 <= dx)
                self.assertTrue(camera.speed * expected_output[0] * 1.01 >= dx)
            
            if expected_output[1] < 0:
                self.assertTrue(camera.speed * expected_output[1] * 0.99 >= dy)
                self.assertTrue(camera.speed * expected_output[1] * 1.01 <= dy)
            else:
                self.assertTrue(camera.speed * expected_output[1] * 0.99 <= dy)
                self.assertTrue(camera.speed * expected_output[1] * 1.01 >= dy)
