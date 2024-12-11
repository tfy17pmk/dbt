import math
import time
import numpy as np

class PID:
    """PID controller class for controlling the position of a system."""

    def __init__(self, K_PID, k, alpha):
        """ Initialize the PID controller with given parameters."""
        self.kpx = K_PID[0]
        self.kix = K_PID[1]
        self.kdx = K_PID[2]
        self.kpy = K_PID[3]
        self.kiy = K_PID[4]
        self.kdy = K_PID[5]
        self.k = k
        self.alpha = alpha 
        self.last_output_x = 0
        self.last_output_y = 0
        self.last_error_x = 0
        self.integral_x = 0
        self.last_error_y = 0
        self.integral_y = 0
        self.last_time = None
        self.count = 0
        self.F = 0

    def compute(self, goal, current_value):
        """Compute the control output based on the goal and current value."""
        current_time = time.perf_counter()
        if self.last_time is None:
            self.last_time = current_time
            return 0, 0
        
        # Calculate the error between the goal and current position
        error_x = (goal[0] - current_value[0]) 
        error_y = (goal[1] - current_value[1])

        # Ignore small errors to avoid unnecessary adjustments
        if np.abs(error_x) < 2:
            error_x = 0 

        if np.abs(error_y) < 2:
            error_y = 0

        # Calculate the integral of the error
        self.integral_x += error_x * (current_time - self.last_time)
        self.integral_y += error_y * (current_time - self.last_time)

        # Calculate the derivative of the error
        derivative_x = (error_x - self.last_error_x) / (current_time - self.last_time)
        derivative_y = (error_y - self.last_error_y) / (current_time - self.last_time)

        # Calculate the PID output
        output_x = self.kpx * error_x + self.kix * self.integral_x + self.kdx * derivative_x
        output_y = self.kpy * error_y + self.kiy * self.integral_y + self.kdy * derivative_y

        # Apply smoothing to the output
        output_x = self.alpha * output_x + (1 - self.alpha) * self.last_output_x
        output_y = self.alpha * output_y + (1 - self.alpha) * self.last_output_y

         # Update the last error and output values
        self.last_error_x = error_x
        self.last_error_y = error_y
        self.last_output_x = output_x
        self.last_output_y = output_y
        self.last_time = current_time

        return output_x, output_y

    def reset(self):
        """
        Reset integrals, last errors, and outputs to clear controller state.
        """
        self.last_output_x = 0
        self.last_output_y = 0
        self.last_error_x = 0
        self.integral_x = 0
        self.last_error_y = 0
        self.integral_y = 0
        self.last_time = None
