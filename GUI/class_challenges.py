import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import random
import time

class Challenges:
    def __init__(self):
        self.patterns = {"square": np.array([[50,50], [200, 50], [200, 200], [50, 200]])}
        self.tags = ["square"]
        self.dot_radius = 10

    def start_challenge(self):
        self.isFinished = False
        tag = self.tags[random.randint(0, len(self.patterns)-1)]
        self.array = self.patterns[tag]
        self.circle_colors = np.zeros((len(self.array[:,0]), 3))
        for i in range(len(self.circle_colors[:,1])):
            self.circle_colors[i, :] = [0,0,255]
        self.goals_hit = np.zeros(len(self.array[:,0]))
        self.nr_of_goals = len(self.array[:,0])
        self.start_time = time.time()

    def create_dots(self, frame, ball_x, ball_y):
        height, width, _ = frame.shape
        rescaled_x = self.array[:,0] - (width/2)
        rescaled_y = self.array[:,1] - (height/2)
        rescaled_y = -rescaled_y
        
        if [ball_x, ball_y] != [-1, -1]:
            for i in range(len(self.array[:,0])):
                if abs(ball_x-rescaled_x[i]) <= self.dot_radius and abs(ball_y-rescaled_y[i]) <= self.dot_radius and self.goals_hit[i] != 1:
                    print("Hi!")
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
        
