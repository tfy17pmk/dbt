import math
import numpy as np
import time

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
		index = 0
		# Distance between ball and set_position
		distance = math.sqrt((current(1)-set_points[index, 1])^2 + (current(2)-set_points[index, 2])^2)
		

		if(distance > self.goal_rad):
			return set_points[index, :]
		else:
			# Loops through set_points matrices rows with index
			index = (index + 1) % set_points.shape(0) 
			return set_points[index, :]

	def pattern4(self, start_time):
		time = time.time()-start_time # index for curve
		A = 3 # parameters for Lissajous curve
		B = 2
		a = 2
		b = 2
		delta = math.pi/4
		reference_x = A*math.sin(a*(time) + delta) #reference for x position
		reference_y = B*math.sin(b*(time)) # reference for y position

		return reference_x, reference_y