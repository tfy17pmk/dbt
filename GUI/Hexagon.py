import tkinter as tk
import math

class HexagonShape:
    def __init__(self, canvas, fill="#ffffff", outline="#ffffff"):
        self.canvas = canvas
        self.points = []  # Hexagon corner points
        self.fill = fill
        self.outline = outline
        self.drawing_points = []  # Store drawing points
        self.line_ids = []  # Store IDs for each complete drawn line
        self.current_line_ids = []  # Track segment IDs for current line
        self.is_freehand = False  # Track if drawing is freehand

        # Bind to draw the hexagon in the case of window resize
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind to handle mouse interactions
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Create initial hexagon
        self.create_hexagon()
        
    def clear_all(self):
        # Clear all lines
        while self.line_ids:
            last_line = self.line_ids.pop()
            for line_id in last_line:
                self.canvas.delete(line_id)
        
        # Clear any shapes by deleting all items with the "shape" tag
        self.canvas.delete("shape")
        
        print("Cleared all lines and shapes")
        print("Funkade najs (interupt grej)!!")
        mapped_points = [0,0]
        print("Mapped shape coordinates:", mapped_points)
        
    def log_shape_coordinates(self, points):
        # Calculate and print the coordinates
        print("Shape coordinates:", points)

        # Example of mapping coordinates (optional)
        target_width = 320
        target_height = 285
        mapped_points = [self.map_coordinates(x, y, target_width, target_height) for x, y in points]
        print("Mapped shape coordinates:", mapped_points)

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
        self.log_shape_coordinates([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

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
        ]
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])
        # Log the coordinates of the triangle vertices
        self.log_shape_coordinates(points)


    def draw_star(self):
        self.is_freehand = False
        self.clear_all()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height) // 3
        cx, cy = width / 2, height / 2
        points = []
        for i in range(10):
            angle = i * 36
            radius = size if i % 2 == 0 else size / 2
            x = cx + radius * math.cos(math.radians(angle - 90))
            y = cy + radius * math.sin(math.radians(angle - 90))
            points.append((x, y))
        shape_id = self.canvas.create_polygon(points, outline="black", fill="", tags="shape")
        self.line_ids.append([shape_id])
        # Log the coordinates of the star points
        self.log_shape_coordinates(points)
    
    def clear_shapes_if_present(self):
        # Check if any shapes are in line_ids and remove them
        if self.line_ids:
            # Filter out all items tagged as "shape" from line_ids
            self.line_ids = [line for line in self.line_ids if "shape" not in self.canvas.gettags(line[0])]
            # Remove all items tagged "shape" from the canvas
            self.canvas.delete("shape")

    def create_hexagon(self):
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
        # Rescale the hexagon in case of window size changing
        self.create_hexagon()
        self.redraw_points()  # Redraw points on resize

    def start_drawing(self, event):
        self.clear_all()
		# Start drawing if inside hexagon
        if self.is_point_inside_hexagon(event.x, event.y):
            self.clear_shapes_if_present()
            self.drawing_points = []  # Reset points when starting a new drawing
            self.current_line_ids = []  # Reset current line segments
            self.drawing_points.append((event.x, event.y))  # Register initial point

    def draw(self, event):
        # Capture points as the mouse moves, only add if distance is sufficient
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
					
    def map_coordinates(self, x, y, target_width, target_height):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Remap coordinates with a linear scale factor
        mapped_x = x * (target_width / canvas_width)
        mapped_y = y * (target_height / canvas_height)

        # Return remapped coordinates with redefined origin in the middle    
        return int(mapped_x-target_width/2), -int(mapped_y-target_height/2) 

    def stop_drawing(self, event):
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

        print("Final drawing points:", self.drawing_points)

        # Remap coordinates into cropped camera picture
        target_width = 320
        target_height = 285
        mapped_points = [self.map_coordinates(x, y, target_width, target_height) for x, y in self.drawing_points]
        print("Mapped drawing points", mapped_points)

    #Tog bort den här koden för den behövs tyderligrn inte, använder clear_all() istället
    #def remove_last_line(self):
        # Remove the last drawn line or shape
       # if self.line_ids:
       #     last_item = self.line_ids.pop()
        #    print("Funkade najs (interupt grej)!!")
         #   for item_id in last_item:
          #      self.canvas.delete(item_id)

    def redraw_points(self):
        # Redraw the stored lines between points
        for line in self.line_ids:
            for line_id in line:
                # Canvas automatically keeps deleted segments removed
                pass

    def is_point_inside_hexagon(self, x, y):
        # Point-within-polygon test (Ray-casting algorithm)
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


'''def draw_circle(self):
        self.is_freehand = False
        self.clear_all()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        radius = min(width, height) // 2
        x0, y0 = (width - radius) / 2, (height - radius) / 2
        x1, y1 = (width + radius) / 2, (height + radius) / 2
        shape_id = self.canvas.create_oval(x0, y0, x1, y1, outline="black", tags="shape")
        self.line_ids.append([shape_id])
        # Log the bounding box coordinates for the circle
        self.log_shape_coordinates([(x0, y0), (x1, y1)])'''