import math
import threading
from multiprocessing import Queue
import time
import numpy as np
from scipy.spatial import distance

class HexagonShape:
    """Handles pattern page drawing board interactions"""

    def __init__(self, canvas, fill="#ffffff", outline="#ffffff"):
        "Initialize drawing board"
        self.canvas = canvas
        self.points = []  # Hexagon corner points
        self.fill = fill
        self.outline = outline
        self.drawing_points = []  # Store drawing points
        self.mapped_points = [] # Store remapped drawing points
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
        self.epsilon = 15 # deviation for draw patterns optimization

        # Bind to draw the hexagon in the case of window resizing
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind to handle mouse interactions
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Create initial hexagon
        self.create_hexagon()
        self.start_thread()
        
    def send_data(self):
        """Send new goal positions to main"""
        while not self.stop_event.is_set():
            try:
                if not self.data_queue.empty():
                    # Get distance from previous position to new goal
                    coordinates = self.data_queue.get_nowait()
                    dist = math.sqrt((self.prev_goal_pos[0] - coordinates[0]) ** 2 + (self.prev_goal_pos[1] - coordinates[1]) ** 2)
                    # Send new goal position and delay for time it will take to reach new goal position
                    delay = abs((dist/80) - self.restart_delay)
                    self.send_goal_pos(coordinates[0], coordinates[1])
                    self.prev_goal_pos = coordinates
                    time.sleep(delay)
                elif len(self.mapped_points):
                    # If there are mapped points put them in data queue
                    [self.data_queue.put((x,y)) for x, y in self.mapped_points]
                time.sleep(self.restart_delay)  # Add a small delay to observe the behavior
        
            except Exception as e:
                pass
        
    def start_thread(self):
        "Start thread sending goal positions to main"
        self.thread_started = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.send_data)
        self.thread.start()
    
    def set_goal_function(self, send_goal_pos_function):
        """Connect to pattern page function sending goal positions to main"""
        self.send_goal_pos = send_goal_pos_function
        
    def clear_thread(self):
        """Empty data queue and set origin as goal position"""
        self.mapped_points = []
        while not self.data_queue.empty():
            self.data_queue.get_nowait()
        
        self.send_goal_pos(0, 0)
          
    def clear_all(self):
        """Clear drawing board and data queue"""
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

    def reset_mapped_points(self):
        """Resets position to origin when pressing undo or returning to prev page"""

        # Clear all lines
        while self.line_ids:
            last_line = self.line_ids.pop()
            for line_id in last_line:
                self.canvas.delete(line_id)
        
        # Clear any shapes by deleting all items with the "shape" tag
        self.canvas.delete("shape")

        # Resets ball position to origin
        while not self.data_queue.empty():
            self.data_queue.get_nowait()
        self.mapped_points = []
        self.send_goal_pos(0, 0)

    def map_coordinates(self, x, y):
        """Remap position data to balancing plate dimensions with origin in the center"""
        # Get screen dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Remap coordinates with a linear scale factor
        mapped_x = x * (self.target_width / canvas_width)
        mapped_y = y * (self.target_height / canvas_height)

        if not self.thread_started:
            self.start_thread()
        
        # Put coordinate data in data queuee
        if not self.data_queue.full():
            try:
                self.data_queue.put((int(mapped_x-self.target_width/2), int(mapped_y-self.target_height/2)), timeout=0.01)
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            print(f"Queue with goal pos is full!")
            
        # Return remapped coordinates   
        return int(mapped_x-self.target_width/2), int(mapped_y-self.target_height/2) 
        
    def log_shape_coordinates(self, points):
        """Puts mapped coordinates into array"""
        self.mapped_points = [self.map_coordinates(x, y) for x, y in points]

    def draw_square(self):
        """Draw square on drawing board and get mapped goal position coordinates"""
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate corner points and draw square on drawing board
        size = min(width, height) // 2
        x0, y0 = (width - size) / 2, (height - size) / 2
        x1, y1 = (width + size) / 2, (height + size) / 2
        shape_id = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates of the square
        self.log_shape_coordinates([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])

    def draw_hexagon(self):
        """Draw hexagon on drawing board and get mapped goal position coordinates"""
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

        # Log the coordinates
        self.log_shape_coordinates(points)

    def draw_triangle(self):
        """Draw triangle on drawing board and get mapped goal position coordinates"""        
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height) // 2
        
        # Calculate points of triangle and draw on drawing board
        points = [
            (width / 2, (height - size) / 2),
            ((width - size) / 2, (height + size) / 2),
            ((width + size) / 2, (height + size) / 2),
            (width / 2, (height - size) / 2)
        ]
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates
        self.log_shape_coordinates(points)

    def draw_star(self):
        """Draw star on drawing board and get mapped goal position coordinates"""
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        outer_radius = min(width, height) / 2.5
        inner_radius = outer_radius/3
        starpoints = 5

        # Calculate the points of the star and draw on drawing board
        points = []
        for i in range(starpoints*2):
            angle  = (i-0.5) * math.pi / starpoints
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        points.append(points[0])
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates
        self.log_shape_coordinates(points)

    def draw_heart(self):
        """Draw heart on drawing board and get mapped goal position coordinates"""
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        scale = 12.5
        pointnumber = 20

        # Calculate the points of the heart and draw on drawing board
        points = []
        for i in range(pointnumber):
            t = i * 2 * math.pi / pointnumber  # Generate n_points evenly spaced values for t
            x = scale * (16 * np.sin(t)**3) + center_x
            y = -scale * (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) + center_y
            points.append((x, y))
        points.append(points[0])
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates
        self.log_shape_coordinates(points)

    def draw_circle(self):
        """Draw heart on drawing board and get mapped goal position coordinates"""
        self.is_freehand = False
        self.clear_all()

        # Calculate the width, height, and center of the canvas
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2.5

        # Calculate the points of the circle and draw on drawing board
        points = []
        for i in range(45):
            angle_deg = 8 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        points.append(points[0])
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])

        # Log the coordinates
        self.log_shape_coordinates(points)
    
    def clear_shapes_if_present(self):
        """Clear any shapes on the drawing board"""
        # Check if any shapes are in line_ids and remove them
        if self.line_ids:
            # Filter out all items tagged as "shape" from line_ids
            self.line_ids = [line for line in self.line_ids if "shape" not in self.canvas.gettags(line[0])]
            # Remove all items tagged "shape" from the canvas
            self.canvas.delete("shape")

    def create_hexagon(self):
        """Create drawing board hexagon"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Find center and radius
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = width // 2.05  # Making sure hexagon fits on the canvas

        # Finding the corner positions of the hexagon
        self.points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            self.points.append((x, y))
            
        # Fill the canvas with the hexagon
        self.canvas.create_polygon(self.points, outline=self.outline, fill=self.fill, width=2)

    def on_resize(self, event):
        """Rescale the hexagon in case of window size changing"""
        self.create_hexagon()
        self.redraw_points()  # Redraw points on resize

    def start_drawing(self, event):
        """If touching screen within drawing board boundaries, enable drawing"""
        self.clear_all()
		# Start drawing if inside hexagon
        if self.is_point_inside_hexagon(event.x, event.y):
            self.clear_shapes_if_present()
            self.drawing_points = []  # Reset points when starting a new drawing
            self.current_line_ids = []  # Reset current line segments
            self.drawing_points.append((event.x, event.y))  # Register initial point

    def draw(self, event):
        """Capture points as the mouse moves, only add if distance from last point is sufficient"""
        if self.is_point_inside_hexagon(event.x, event.y):
            if not self.drawing_points:
                self.drawing_points.append((event.x, event.y))
            else:
                last_x, last_y = self.drawing_points[-1]
                # Only add point if x or y difference is more than 5
                if abs(event.x - last_x) > 5 or abs(event.y - last_y) > 5:
                    # Draw and add segment ID to current line
                    line_id = self.canvas.create_line(last_x, last_y, event.x, event.y, fill="black")
                    self.current_line_ids.append(line_id)
                    self.drawing_points.append((event.x, event.y))

    def stop_drawing(self, event):
        """Append drawned points to mapped points if user is no longer drawing"""
        self.clear_all()
        self.mapped_points = []
        # Connect the last point to the first to close the shape, if close enough
        if len(self.drawing_points) > 1:
            first_x, first_y = self.drawing_points[0]
            last_x, last_y = self.drawing_points[-1]
            if abs(last_x - first_x) <= 20 and abs(last_y - first_y) <= 20:
                line_id = self.canvas.create_line(last_x, last_y, first_x, first_y, fill="black")
                self.current_line_ids.append(line_id)
        
        # Store the current completed line segments
        if self.current_line_ids:
            self.line_ids.append(self.current_line_ids)
            self.current_line_ids = []  # Reset for next line

        # Remap coordinates into cropped camera picture
        self.mapped_points = [self.map_coordinates(x, y) for x, y in self.drawing_points]
        self.mapped_points = self.douglas_peucker(self.mapped_points)

    def redraw_points(self):
        """Redraw the stored lines between points"""
        for line in self.line_ids:
            for line_id in line:
                # Canvas automatically keeps deleted segments removed
                pass

    def is_point_inside_hexagon(self, x, y):
        """Point-within-polygon test (Ray-casting algorithm)"""
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    def perpendicular_distance(self, point, line_start, line_end):
        """
        Calculate the perpendicular distance of a point from a line.
        
        Args:
            point (tuple): (x, y) coordinates of the point.
            line_start (tuple): (x, y) coordinates of the line's start point.
            line_end (tuple): (x, y) coordinates of the line's end point.
            
        Returns:
            float: The perpendicular distance.
        """
        if line_start == line_end:
            return np.sqrt((point[0] - line_start[0])**2 + (point[1] - line_start[1])**2)
        
        x0, y0 = point
        x1, y1 = line_start
        x2, y2 = line_end

        num = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        den = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        return num / den
    
    def douglas_peucker(self, points):
        """
        Simplify a curve using the Douglas-Peucker algorithm.
        
        Args:
            points (list of tuples): List of (x, y) coordinates.
            
        Returns:
            list of tuples: Simplified curve as a list of points.
        """
        # Base case: If the segment has fewer than 3 points, return it
        if len(points) < 3:
            return points

        # Find the point with the maximum perpendicular distance
        start, end = points[0], points[-1]
        max_dist = 0
        index = 0
        for i in range(1, len(points) - 1):
            dist = self.perpendicular_distance(points[i], start, end)
            if dist > max_dist:
                max_dist = dist
                index = i

        # If the maximum distance is greater than epsilon, recurse
        if max_dist > self.epsilon:
            # Recursive call on both segments
            left = self.douglas_peucker(points[:index + 1])
            right = self.douglas_peucker(points[index:])
            return left[:-1] + right  # Combine results, removing duplicate at the join
        else:
            # Return the endpoints as the simplified segment
            return [start, end]
        
    def join_threads(self):
        "Kill thread"
        self.stop_event.set()
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
