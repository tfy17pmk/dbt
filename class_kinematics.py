import numpy as np

class Kinematics:
    # setup init
    def __init__(self):
        # define lengths [origin to servo, first arm, second arm, radius of hexagon]
        self.L = [0.04, 0.04, 0.065, 0.065]
        # initial pose of table (theta, phi, h)
        self.initial_position = [0, 0, 0.0632]
        self.h_max = 0.0732 # max height
        self.h_min = 0.0532 # min height
        self.phi_max = 20 # max angle

    def InverseKinematics(self, n, h):
        L = self.L

        # Set reference height for leg
        A = (L[0] + L[1]) / h
        B = (h**2 + L[2]**2 - (L[0] + L[1])**2 - L[3]**2) / (2*h)
        C = A**2 + 1
        D = 2 * (A * B - (L[0] + L[1]))
        E = B**2 + (L[0] + L[1])**2 - L[2]**2

        Pmx = (-D + np.sqrt(D**2 - 4 * C * E)) / (2 * C)
        Pmz = np.sqrt(L[2]**2 - Pmx**2 + 2 * (L[0] + L[1]) * Pmx - (L[0] + L[1])**2)

        # First leg
        # coordinates of mounting point for a1 arm on table
        a1_x_mount = n[2] * L[3] / np.sqrt(n[0]**2 + n[2]**2)
        a1_y_mount = 0
        a1_z_mount = h + n[0] * L[3] / np.sqrt(n[0]**2 + n[2]**2)
        A1_mount = [a1_x_mount, a1_y_mount, a1_z_mount]

        # Define knee coordinates
        A1 = (L[0] - a1_x_mount) / a1_z_mount
        B1 = -(a1_x_mount**2 + a1_z_mount**2 + L[1]**2 - L[0]**2 - L[2]**2)
        C1 = A1**2 + 1
        D1 = 2 * (A1 * B1 + L[0])
        E1 = B1**2 - L[0]**2 - L[1]**2


        a1_x_knee = (-D1 + np.sqrt(D1**2 - 4 * C1 * E1)) / (2 * C1)
        a1_y_knee = 0
        a1_z_knee = np.sqrt(L[1]**2 - (a1_x_knee - L[0])**2)

        if (a1_z_mount < Pmz):
            a1_z_knee = -a1_z_knee
        A1_knee = [a1_x_knee, a1_y_knee, a1_z_knee]

        a1_costheta = (A1_knee[0] - L[0]) / L[1]
        a1_sintheta = (A1_knee[2]) / L[1]

        a1_theta = np.arctan2(a1_costheta, a1_sintheta)

        # Second leg
        a2_x_mount = (-L[3] * n[2]) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        a2_y_mount = (np.sqrt(3) * L[3] * n[2]) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        a2_z_mount = h + (L[3] * (-np.sqrt(3) * n[0] + n[1])) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        A2_mount = [a2_x_mount, a2_y_mount, a2_z_mount]

        # Define knee coordinates
        A2 = (-A2_mount[0] + np.sqrt(3) * A2_mount[1] - 2 * L[0]) / A2_mount[2]
        B2 = (A2_mount[0]**2 + A2_mount[1]**2 + A2_mount[2]**2 + L[1]**2 - L[0]**2 - L[2]**2) / (2 * A2_mount[2])
        C2 = A2**2 + 4 
        D2 = 2 * A2 * B2 + 4 * L[0]
        E2 = B2**2 + L[0]**2 - L[1]**2

        a2_x_knee = (-D2 - np.sqrt(D2**2 - 4 * C2 * E2)) / (2 * C2)
        a2_y_knee = -np.sqrt(3) * a2_x_knee
        a2_z_knee = np.sqrt(L[1]**2 - 4 * a2_x_knee**2 - 4 * L[0] * a2_x_knee - L[0]**2)

        if (a2_z_mount < Pmz):
            a2_z_knee = -a2_z_knee
        A2_knee = [a2_x_knee, a2_y_knee, a2_z_knee]

        a2_theta = np.arctan2(A2_knee[2]**2, np.sqrt(A2_knee[0]**2 + A2_knee[1]**2) - L[0])


        # Third leg
        a3_x_mount = (-L[3] * n[2]) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        a3_y_mount = (-np.sqrt(3) * L[3] * n[2]) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        a3_z_mount = h + (L[3] * (np.sqrt(3) * n[0] + n[1])) / np.sqrt(n[0]**2 + 3 * n[1]**2 + 4 * n[2]**2 - 2 * np.sqrt(3) * n[0] * n[1])
        A3_mount = [a3_x_mount, a3_y_mount, a3_z_mount]

        # Define knee coordinates
        A3 = -(A3_mount[0] + np.sqrt(3) * A3_mount[1] + 2 * L[0]) / A3_mount[2]
        B3 = (A3_mount[0]**2 + A3_mount[1]**2 + A3_mount[2]**2 + L[1]**2 - L[0]**2 - L[2]**2) / (2 * A3_mount[2])
        C3 = A3**2 + 4 
        D3 = 2 * A3 * B3 + 4 * L[0]
        E3 = B3**2 + L[0]**2 - L[1]**2

        a3_x_knee = (-D3 - np.sqrt(D3**2 - 4 * C3 * E3)) / (2 * C3)
        a3_y_knee = np.sqrt(3) * a3_x_knee
        a3_z_knee = np.sqrt(L[1]**2 - 4 * a3_x_knee**2 - 4 * L[0] * a3_x_knee - L[0]**2)

        if (a3_z_mount < Pmz):
            a3_z_knee = -a3_z_knee
        A3_knee = [a3_x_knee, a3_y_knee, a3_z_knee]

        a3_theta = np.arctan2(A3_knee[2]**2, np.sqrt(A3_knee[0]**2 + A3_knee[1]**2) - L[0])

        thetas = [a1_theta, a2_theta, a3_theta]
        return thetas
