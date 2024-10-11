import pigpio

# Connect to pigpiod daemon
pi = pigpio.pi()

class Motors:
    def __init__(self):
        pass
        
    def setup_motor(self, resolution):
        MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins

        RESOLUTION = {'Full': (0, 0, 0),
                      'Half': (1, 0, 0),
                      '1/4': (0, 1, 0),
                      '1/8': (1, 1, 0),
                      '1/16': (0, 0, 1),
                      '1/32': (1, 0, 1)}
        
        for i in range(3):
            pi.write(MODE[i], RESOLUTION[resolution][i])
        

    def initial_position():
        pass

    def set_angle(direction, steps, angle, current_step, resolution):

        absolute_steps = (angle / 1.8) * resolution # angle to absolute steps

        relative_steps = absolute_steps - current_step

        if relative_steps < 0:
            direction = 
            pi.write(DI, 1)







    def clean_up():