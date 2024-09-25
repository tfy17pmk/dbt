import numpy as np

class Kinematics:
    # setup init
    def __init__(self):
        # Lengths for the robot arms and platform:
        # lengths = [origin to servo, first arm, second arm, radius of hexagonal platform]
        self.lengths = [0.04, 0.04, 0.065, 0.065]

        # Initial position of table (theta, phi, height)
        self.initial_position = [0, 0, 0.0632]

        # High limits for the platform
        self.height_max = 0.0732 
        self.height_min = 0.0532 

        # Maximum tilt angle
        self.phi_max = 20

    def inverse_kinematics(self, normal_vector, height):
        base_to_servo_length = self.lengths[0]
        arm_1_length = self.lengths[1]
        arm_2_length = self.lengths[2]
        platform_radius = self.lengths[3]
        initial_orientation = self.initial_position[:2]
        initial_height = self.initial_position[2]
        max_tilt_angle = self.phi_max

        # Set reference height for arms (A-E are intermediate variables for simplified calculations)
        A = (base_to_servo_length + arm_1_length) / height
        B = (height**2 + arm_2_length**2 - (base_to_servo_length + arm_1_length)**2 - platform_radius**2) / (2*height)
        C = A**2 + 1
        D = 2 * (A * B - (base_to_servo_length + arm_1_length))
        E = B**2 + (base_to_servo_length + arm_1_length)**2 - arm_2_length**2

        Pmx = (-D + np.sqrt(D**2 - 4 * C * E)) / (2 * C)
        Pmz = np.sqrt(arm_2_length**2 - Pmx**2 + 2 * (base_to_servo_length + arm_1_length) * Pmx - (base_to_servo_length + arm_1_length)**2)

        """ --------------------------------------- FIRST ARM --------------------------------------- """
        # Mounting point on the platform
        arm_1_x_mount = normal_vector[2] * platform_radius / np.sqrt(normal_vector[0]**2 + normal_vector[2]**2)
        arm_1_y_mount = 0
        arm_1_z_mount = height + normal_vector[0] * platform_radius / np.sqrt(normal_vector[0]**2 + normal_vector[2]**2)
        arm_1_mount_array = [arm_1_x_mount, arm_1_y_mount, arm_1_z_mount]

        # Define knee coordinates (A1-E1 are intermediate variables for simplified calculations)
        A1 = (base_to_servo_length - arm_1_x_mount) / arm_1_z_mount
        B1 = -(arm_1_x_mount**2 + arm_1_z_mount**2 + arm_1_length**2 - base_to_servo_length**2 - arm_2_length**2)
        C1 = A1**2 + 1
        D1 = 2 * (A1 * B1 + base_to_servo_length)
        E1 = B1**2 - base_to_servo_length**2 - arm_1_length**2

        arm_1_x_knee = (-D1 + np.sqrt(D1**2 - 4 * C1 * E1)) / (2 * C1)
        arm_1_y_knee = 0
        arm_1_z_knee = np.sqrt(arm_1_length**2 - (arm_1_x_knee - base_to_servo_length)**2)

        if (arm_1_z_mount < Pmz):
            arm_1_z_knee = -arm_1_z_knee
        arm_1_knee_array = [arm_1_x_knee, arm_1_y_knee, arm_1_z_knee]

        arm_1_costheta = (arm_1_knee_array[0] - base_to_servo_length) / arm_1_length
        arm_1_sintheta = (arm_1_knee_array[2]) / arm_1_length

        arm_1_theta = np.arctan2(arm_1_costheta, arm_1_sintheta)

        """ --------------------------------------- SECOND ARM --------------------------------------- """
        # Mounting point on the platform
        arm_2_x_mount = (-platform_radius * normal_vector[2]) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_2_y_mount = (np.sqrt(3) * platform_radius * normal_vector[2]) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_2_z_mount = height + (platform_radius * (-np.sqrt(3) * normal_vector[0] + normal_vector[1])) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_2_mount_array = [arm_2_x_mount, arm_2_y_mount, arm_2_z_mount]

        # Define knee coordinates (A2-E2 are intermediate variables for simplified calculations)
        A2 = (-arm_2_mount_array[0] + np.sqrt(3) * arm_2_mount_array[1] - 2 * base_to_servo_length) / arm_2_mount_array[2]
        B2 = (arm_2_mount_array[0]**2 + arm_2_mount_array[1]**2 + arm_2_mount_array[2]**2 + arm_1_length**2 - base_to_servo_length**2 - arm_2_length**2) / (2 * arm_2_mount_array[2])
        C2 = A2**2 + 4 
        D2 = 2 * A2 * B2 + 4 * base_to_servo_length
        E2 = B2**2 + base_to_servo_length**2 - arm_1_length**2

        arm_2_x_knee = (-D2 - np.sqrt(D2**2 - 4 * C2 * E2)) / (2 * C2)
        arm_2_y_knee = -np.sqrt(3) * arm_2_x_knee
        arm_2_z_knee = np.sqrt(arm_1_length**2 - 4 * arm_2_x_knee**2 - 4 * base_to_servo_length * arm_2_x_knee - base_to_servo_length**2)

        if (arm_2_z_mount < Pmz):
            arm_2_z_knee = -arm_2_z_knee
        arm_2_knee_array = [arm_2_x_knee, arm_2_y_knee, arm_2_z_knee]

        arm_2_theta = np.arctan2(arm_2_knee_array[2]**2, np.sqrt(arm_2_knee_array[0]**2 + arm_2_knee_array[1]**2) - base_to_servo_length)

        """ --------------------------------------- THIRD ARM --------------------------------------- """
        # Mounting point on the platform
        arm_3_x_mount = (-platform_radius * normal_vector[2]) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_3_y_mount = (-np.sqrt(3) * platform_radius * normal_vector[2]) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_3_z_mount = height + (platform_radius * (np.sqrt(3) * normal_vector[0] + normal_vector[1])) / np.sqrt(normal_vector[0]**2 + 3 * normal_vector[1]**2 + 4 * normal_vector[2]**2 - 2 * np.sqrt(3) * normal_vector[0] * normal_vector[1])
        arm_3_mount_array = [arm_3_x_mount, arm_3_y_mount, arm_3_z_mount]

        # Define knee coordinates (A3-E3 are intermediate variables for simplified calculations)
        A3 = -(arm_3_mount_array[0] + np.sqrt(3) * arm_3_mount_array[1] + 2 * base_to_servo_length) / arm_3_mount_array[2]
        B3 = (arm_3_mount_array[0]**2 + arm_3_mount_array[1]**2 + arm_3_mount_array[2]**2 + arm_1_length**2 - base_to_servo_length**2 - arm_2_length**2) / (2 * arm_3_mount_array[2])
        C3 = A3**2 + 4 
        D3 = 2 * A3 * B3 + 4 * base_to_servo_length
        E3 = B3**2 + base_to_servo_length**2 - arm_1_length**2

        arm_3_x_knee = (-D3 - np.sqrt(D3**2 - 4 * C3 * E3)) / (2 * C3)
        arm_3_y_knee = np.sqrt(3) * arm_3_x_knee
        arm_3_z_knee = np.sqrt(arm_1_length**2 - 4 * arm_3_x_knee**2 - 4 * base_to_servo_length * arm_3_x_knee - base_to_servo_length**2)

        if (arm_3_z_mount < Pmz):
            arm_3_z_knee = -arm_3_z_knee
        arm_3_knee_array = [arm_3_x_knee, arm_3_y_knee, arm_3_z_knee]

        arm_3_theta = np.arctan2(arm_3_knee_array[2]**2, np.sqrt(arm_3_knee_array[0]**2 + arm_3_knee_array[1]**2) - base_to_servo_length)

        """ ---------------------------------------------------------------------------------------- """

        # Return the three calculated theta values for the arms
        thetas = [arm_1_theta, arm_2_theta, arm_3_theta]

        return thetas
