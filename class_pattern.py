import math
import numpy as np

class Pattern:
	def __init__(self):
		self.goal_rad = 50

	def pattern1(self, current):
		# HEXAGON

		# Manually set positions for ball
		set_points = np.array[[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6]]
		index = 0
		
		# Distance between ball and set_position
		distance = math.sqrt((current(1)-set_points[index, 1])^2 + (current(2)-set_points[index, 2])^2)
		
		if(distance > self.goal_rad):
			return set_points[index, :]
		else:
			# Loops through set_points matrices rows with index
			index = (index + 1) % set_points.shape(0) 
			return set_points[index, :]


	def pattern2(self, current):
		# SQUARE
		set_points = np.array[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
		index = 0
		
		# Distance between ball and set_position
		distance = math.sqrt((current(1)-set_points[index, 1])^2 + (current(2)-set_points[index, 2])^2)
		

		if(distance > self.goal_rad):
			return set_points[index, :]
		else:
			# Loops through set_points matrices rows with index
			index = (index + 1) % set_points.shape(0) 
			return set_points[index, :]
	
	def pattern3(self, current):
		# TRIANGLE
		set_points = np.array[[x1, y1], [x2, y2], [x3, y3]]
		
		# Distance between ball and set_position
		distance = math.sqrt((current(1)-set_points[index, 1])^2 + (current(2)-set_points[index, 2])^2)
		

		if(distance > self.goal_rad):
			return set_points[index, :]
		else:
			# Loops through set_points matrices rows with index
			index = (index + 1) % set_points.shape(0) 
			return set_points[index, :]