import math
import threading
from multiprocessing import Queue
import time
import numpy as np

class Patterns:
    def __init__(self, fill="#ffffff", outline="#ffffff"):
        self.points = []  # Hexagon corner points
        self.fill = fill
        self.outline = outline
        self.drawing_points = []  # Store drawing points
        self.mapped_points = [] # Store remapped points
        self.line_ids = []  # Store IDs for each complete drawn line
        self.current_line_ids = []  # Track segment IDs for current line
        self.is_freehand = False  # Track if drawing is freehand
        self.target_width = 320
        self.target_height = 285
        self.send_goal_pos = None
        self.stop_event = threading.Event()
        self.thread_started = False
        self.data_queue = Queue(maxsize=500)
        self.prev_goal_pos = (0, 0)
        self.restart_delay = 0.01


        self.start_thread()
        
    def send_data(self):
        while not self.stop_event.is_set():
            try:
                if not self.data_queue.empty():
                    coordinates = self.data_queue.get_nowait()
                    
                    dist = math.sqrt((self.prev_goal_pos[0] - coordinates[0]) ** 2 + (self.prev_goal_pos[1] - coordinates[1]) ** 2)
                    delay = abs((dist/80) - self.restart_delay)
                    self.send_goal_pos(coordinates[0], coordinates[1])
                    self.prev_goal_pos = coordinates
                    time.sleep(delay)
                elif len(self.mapped_points):
                    [self.data_queue.put((x,y)) for x, y in self.mapped_points]
                time.sleep(self.restart_delay)  # Add a small delay to observe the behavior
        
            except Exception as e:
                pass
        
    def start_thread(self):
        self.thread_started = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.send_data)
        self.thread.start()
    
    def set_goal_function(self, send_goal_pos_function):
        self.send_goal_pos = send_goal_pos_function
        
          
    def clear_all(self):
        # Function to overwrite previous goal points
        while not self.data_queue.empty():
            self.data_queue.get_nowait()
            
        # Clear all lines
        while self.line_ids:
            last_line = self.line_ids.pop()
            for line_id in last_line:
                self.canvas.delete(line_id)
        
        # Clear any shapes by deleting all items with the "shape" tag
        self.canvas.delete("shape")


    def map_coordinates(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Remap coordinates with a linear scale factor
        mapped_x = x * (self.target_width / canvas_width)
        mapped_y = y * (self.target_height / canvas_height)

        if not self.thread_started:
            self.start_thread()
        
        if not self.data_queue.full():
            try:
                self.data_queue.put((int(mapped_x-self.target_width/2), int(mapped_y-self.target_height/2)), timeout=0.01)
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            print(f"Queue with goal pos is full!")
            
        # Return remapped coordinates with redefined origin in the middle    
        return int(mapped_x-self.target_width/2), int(mapped_y-self.target_height/2) 
        
    def log_shape_coordinates(self, points):
        # Example of mapping coordinates (optional)
        self.mapped_points = [self.map_coordinates(x, y) for x, y in points]
        print("Mapped shape coordinates:", self.mapped_points)

    def draw_square(self):
        self.is_freehand = False
        self.clear_all()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height) // 2
        x0, y0 = (width - size) / 2, (height - size) / 2
        x1, y1 = (width + size) / 2, (height + size) / 2
        shape_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", tags="shape")
        self.line_ids.append([shape_id])
        # Log the coordinates of the square
        self.log_shape_coordinates([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])

    def draw_hexagon(self):
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2.5  # Radius for the hexagon to fit within canvas

        # Calculate the six vertices of the hexagon
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        points.append(points[0])
        # Draw the hexagon on the canvas
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates of the hexagon vertices
        self.log_shape_coordinates(points)

    def draw_triangle(self):
        self.is_freehand = False
        self.clear_all()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height) // 2
        points = [
            (width / 2, (height - size) / 2),
            ((width - size) / 2, (height + size) / 2),
            ((width + size) / 2, (height + size) / 2),
            (width / 2, (height - size) / 2)
        ]
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])
        # Log the coordinates of the triangle vertices
        self.log_shape_coordinates(points)

    def draw_star(self):
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        outer_radius = min(width, height) / 2.5  # Radius for the hexagon to fit within canvas
        inner_radius = outer_radius/3
        starpoints = 5

        # Calculate the six vertices of the hexagon
        points = []
        for i in range(starpoints*2):
            angle  = (i-0.5) * math.pi / starpoints
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        points.append(points[0])
        # Draw the hexagon on the canvas
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates of the hexagon vertices
        self.log_shape_coordinates(points)

    def draw_heart(self):
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        #radius = min(width, height) / 2.5  # Radius for the hexagon to fit within canvas
        scale = 12.5
        pointnumber = 20

        # Calculate the six vertices of the hexagon
        points = []
        for i in range(pointnumber):
            t = i * 2 * math.pi / pointnumber  # Generate n_points evenly spaced values for t
            x = scale * (16 * np.sin(t)**3) + center_x
            y = -scale * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) + center_y
            points.append((x, y))
        points.append(points[0])
        print(points)
        # Draw the hexagon on the canvas
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates of the hexagon vertices
        self.log_shape_coordinates(points)



    def draw_circle(self):
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2.5  # Radius for the hexagon to fit within canvas

        # Calculate the six vertices of the hexagon
        points = []
        for i in range(45):
            angle_deg = 8 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        points.append(points[0])
        print(points)
        # Draw the hexagon on the canvas
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates of the hexagon vertices
        self.log_shape_coordinates(points)
    

    '''def remove_last_line(self):
        # Remove the last drawn line or shape
        if self.line_ids:
            last_item = self.line_ids.pop()
            print("Funkade najs (interupt grej)!!")
            for item_id in last_item:
                self.canvas.delete(item_id)'''