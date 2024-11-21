import math
import time
import numpy as np
    
class PID:
    def __init__(self, K_PID, k, alpha):
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

    def compute(self, Goal, Current_value):
        current_time = time.perf_counter()
        if self.last_time is None:
            self.last_time = current_time
            return 0, 0
        
        error_x = (Goal[0] - Current_value[0]) 
        error_y = (Goal[1] - Current_value[1])

        if np.abs(error_x) < 2:
            error_x = 0 

        if np.abs(error_y) < 2:
            error_y = 0

        self.integral_x += error_x * (current_time - self.last_time)
        self.integral_y += error_y * (current_time - self.last_time)

        derivative_x = (error_x - self.last_error_x) / (current_time - self.last_time)
        derivative_y = (error_y - self.last_error_y) / (current_time - self.last_time)

        output_x = self.kpx * error_x + self.kix * self.integral_x + self.kdx * derivative_x
        output_y = self.kpy * error_y + self.kiy * self.integral_y + self.kdy * derivative_y

        output_x = self.alpha * output_x + (1 - self.alpha) * self.last_output_x
        output_y = self.alpha * output_y + (1 - self.alpha) * self.last_output_y

        self.last_error_x = error_x
        self.last_error_y = error_y
        self.last_output_x = output_x
        self.last_output_y = output_y
        self.last_time = current_time
        print(f"In PID x: {output_x} y: {output_y}" )

        return output_x, output_y

    def reset(self):
        # Reset integrals, last errors, and outputs to clear controller state
        self.last_output_x = 0
        self.last_output_y = 0
        self.last_error_x = 0
        self.integral_x = 0
        self.last_error_y = 0
        self.integral_y = 0
        self.last_time = None
