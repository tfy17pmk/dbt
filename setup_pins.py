import numpy as np

# Pins for micro stepping resolution
MODE = np.array([14, 15, 18])   # Microstep Resolution GPIO Pins

direction_pins = np.array([20, 7, 23]) # directions pins for motors 1-3
step_pins = np.array([21, 8, 24]) # step pins for motors 1-3
