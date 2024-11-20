from advanced_pid import PID
import time

class PID_control:

	def __init__(self, k_pid):
		self.kp = k_pid[0]
		self.ki = k_pid[1]
		self.kd = k_pid[2]
		self.tf = k_pid[3]

		# Creates PID-controler
		self.pid_x = PID(self.kp, self.ki, self.kd, self.tf)
		self.pid_y = PID(self.kp, self.ki, self.kd, self.tf)

	def get_angles(self, goal, current):
		
		timestamp = time.time()
		
		x_goal = goal[0]
		y_goal = goal[1]

		x_current = current[0]
		y_current = current[1]


		control_x = self.pid_x(timestamp, (x_goal-x_current)*(0.4/270))
		control_y = self.pid_y(timestamp, (y_goal-y_current)*(0.4/270))

		return control_x, control_y
	
	
	
"""if __name__ == "__main__":
	k_pid = [0.1, 0.5, 0.3, 0.1]
	pid_controller = PID_control(k_pid)
	while(1):
		goal = [0, 0]
		current = [10, 0]
		
		control_x, control_y = pid_controller.get_angles(goal, current)
		print(f"X:{control_x}, Y:{control_y}")"""

