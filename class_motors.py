import pigpio
import numpy as np

class Motors:
    def __init__(self, MODE, DIR, STEP):
        # Connect to pigpiod daemon
        self.pi = pigpio.pi()
        
        self.MODE = MODE
        self.DIR = DIR
        self.STEP = STEP
        
        self.degree_per_step = 1.8/32
        self.PWM_frequency = 8000
        self.PWM = 128

        RESOLUTION = {'1/32': (1, 0, 1)}
        for i in range(3):
            self.pi.write(self.MODE[i], RESOLUTION['1/32'][i])
            self.pi.set_mode(self.DIR[i], pigpio.OUTPUT)
            self.pi.set_mode(self.STEP[i], pigpio.OUTPUT)
            self.pi.set_PWM_dutycycle(self.STEP[i], 0)
            self.pi.set_PWM_frequency(self.STEP[i], self.PWM_frequency)

    def initial_position(self):
        self.current_angles = np.zeros(3)

    def set_angle(self, goal_angles):
        relative_angles = goal_angles - self.current_angles
        self.current_angles = goal_angles
        required_steps = abs(relative_angles) / self.degree_per_step # angle to absolute steps
        rotation_times = required_steps*1000000/self.PWM_frequency
        
        for i in range(3):
            if relative_angles[i] != 0:
                step_direction = np.where(relative_angles[i] > 0, 1, 0)
                self.pi.write(self.DIR[i], step_direction)
                self.pi.set_PWM_dutycycle(self.STEP[i], 128)

        start_tick = self.pi.get_current_tick()
        while self.pi.get_current_tick() - start_tick < max(rotation_times):
            for i in range(3):
                if self.pi.get_current_tick() - start_tick >= rotation_times[i]:
                    self.pi.set_PWM_dutycycle(self.STEP[i], 0)
        
        for i in range(3):
            self.pi.set_PWM_dutycycle(self.STEP[i])
                
    def clean_up(self):
        for i in range(3):
            self.pi.set_PWM_dutycycle(self.STEP[i])
        self.pi.stop()