"""
Camera class.
"""
import math

class Camera:
    """
    Camera class for the visualization class.
    """
    
    def __init__(self, position=(0, 0), zoom=1):
        """
        Initialize camera class.
        """
        # Set member variables.
        self.position = list(position)
        self.zoom = zoom
        self.zoom_target = zoom
        
        # Camera speed.
        self.speed = 1000
        self.normalized_speed = self.speed / math.sqrt(2)
        
        # Variables to keep track of if an up/down keypress has been handled or
        # not.
        self.up_key_press_handled = False
        self.down_key_press_handled = False
    
    def update(self, delta_time, keys_pressed):
        """
        Update camera, called from the render loop. Delta time is the time 
        that passed since the last update call. Keys pressed is a list of the 
        following form: [w, a, s, d, up, down]. It is used to update the 
        camera properties.
        """
        # Calculate velocity.
        velocity_x = 0
        velocity_y = 0
        if keys_pressed[0]:
            velocity_y += self.speed
        if keys_pressed[1]:
            velocity_x -= self.speed
        if keys_pressed[2]:
            velocity_y -= self.speed
        if keys_pressed[3]:
            velocity_x += self.speed
        
        # Normalize velocity if required.
        if abs(velocity_x) > 0 and abs(velocity_y) > 0:
            velocity_x_sign = 1 if velocity_x > 0 else -1
            velocity_y_sign = 1 if velocity_y > 0 else -1
            velocity_x = velocity_x_sign * self.normalized_speed
            velocity_y = velocity_y_sign * self.normalized_speed
        
        # Update camera position.
        self.position[0] += delta_time * velocity_x / self.zoom
        self.position[1] += delta_time * velocity_y / self.zoom
        
        # Calculate zoom target.
        if keys_pressed[4]:
            if not self.up_key_press_handled:
                self.zoom_target *= 2
                self.up_key_press_handled = True
        else:
            if self.up_key_press_handled:
                self.up_key_press_handled = False
        
        if keys_pressed[5]:
            if not self.down_key_press_handled:
                self.zoom_target /= 2
                self.down_key_press_handled = True
        else:
            if self.down_key_press_handled:
                self.down_key_press_handled = False
        
        # Restrict zoom target.
        self.zoom_target = max(self.zoom_target, 0.001)
        
        # Update zoom.
        self.zoom += (self.zoom_target - self.zoom) * 0.05
        if self.zoom > 0.99 * self.zoom_target \
            and self.zoom < 1.01 * self.zoom_target:
            self.zoom = self.zoom_target
    
    def get_position(self):
        """
        Return the camera's position.
        """
        # Return camera position.
        return self.position
    
    def get_zoom(self):
        """
        Returns the camera's zoom.
        """
        # Return camera zoom.
        return self.zoom
