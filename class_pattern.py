import math
import numpy as np
import time

class Pattern:
	def __init__(self):
		self.goal_rad = 50
		self.index = 0

	def pattern1(self, current, goal):
		# HEXAGON

		# Manually set positions for ball
		#set_points = np.array[[x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6]]
		self.index = self.index % goal.shape(0) 
		
		# Distance between ball and set_position
		distance = math.sqrt((current(0)-goal[self.index, 0])^2 + (current(1)-goal[self.index, 1])^2)
		
		if(distance > self.goal_rad):
			return goal[self.index, :]
		else:
			# Loops through set_points matrices rows with index
			self.index = (self.index + 1)
			return goal[self.index, :]

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