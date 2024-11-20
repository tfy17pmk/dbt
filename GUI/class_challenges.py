import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import random
import time
import math

class Challenges:
    def __init__(self, height, width):
        self.frame_height, self.frame_width = height, width
        self.create_patterns()
        self.dot_radius = 10

    def create_patterns(self):
        size = min(self.frame_width, self.frame_height)/2

        # Square
        x0 = (self.frame_width - size)/2
        y0 = (self.frame_height - size)/2
        x1 = (self.frame_width + size)/2
        y1 = (self.frame_height + size)/2
        square = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])

        # Hexagon
        hexagon = np.zeros((6, 2))
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = self.frame_width/2 + size/1.5 * math.cos(angle_rad)
            y = self.frame_height/2 + size/1.5 * math.sin(angle_rad)
            hexagon[i, :] = [x, y]

        # Triangle
        triangle = np.array([[self.frame_width/2, (self.frame_height-size)/2], 
                             [(self.frame_width - size)/2, (self.frame_height + size)/2],
                             [(self.frame_width + size)/2, (self.frame_height + size)/2]])

        self.patterns = {"Medel": square, "Svår": hexagon, "Lätt": triangle}

    def start_challenge(self, nivå):
        self.isFinished = False

        self.array = self.patterns[nivå]
        self.goal_array = np.zeros(self.array.shape)
        rescaled_x = self.array[:,0] - (self.frame_width/2)
        rescaled_y = self.array[:,1] - (self.frame_height/2)
        rescaled_y = -rescaled_y
        for i in range(len(rescaled_x)):
            self.goal_array[i,0], self.goal_array[i,1] = rescaled_x[i], rescaled_y[i]
        
        self.circle_colors = np.zeros((len(self.array[:,0]), 3))
        for i in range(len(self.circle_colors[:,1])):
            self.circle_colors[i, :] = [0,0,255]
        
        self.goals_hit = np.zeros(len(self.array[:,0]))
        self.nr_of_goals = len(self.array[:,0])
        self.start_time = time.time()

    def create_dots(self, frame, ball_x, ball_y):
        
        if [ball_x, ball_y] != [-1, -1]:
            for i in range(len(self.array[:,0])):
                if abs(ball_x-self.goal_array[i,0]) <= self.dot_radius and abs(ball_y-self.goal_array[i,1]) <= self.dot_radius and self.goals_hit[i] != 1:
                    self.circle_colors[i, :] = [255,0,0]
                    self.goals_hit[i] = 1
        
        for i in range(len(self.array[:,0])):
            cv.circle(frame, (int(self.array[i,0]), int(self.array[i,1])), int(self.dot_radius), color=self.circle_colors[i, :], thickness=2)

        if np.sum(self.goals_hit) == self.nr_of_goals:
            result_time = time.time()-self.start_time
            self.isFinished = True
        else:
            result_time = None
        
        return self.isFinished, result_time
        
