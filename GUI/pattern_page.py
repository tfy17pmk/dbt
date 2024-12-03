from tkinter import *
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance  # Import Pillow for image resizing
import GUI.constants
import GUI.button
import GUI.patterns
from GUI.patterns import Patterns
import math
import threading

# Page 3: Practice mode
class Pattern_page(tk.Frame):
    def __init__(self, parent, controller, patterns, resources):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.button = GUI.button
        self.hexagon = patterns
        self.goal_pos_queue = resources.goal_position_queue
        """Patterns init"""




        # Setup grid pattern with equal weight for each row and column
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)

        # Set presets for screen dimensions, background color and button dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.configure(bg=self.constants.background_color)
        button_width = int(screen_width * 0.05)
        button_height = int(screen_height * 0.05)

        #the square image for the patterns page
        image = Image.open(self.constants.SQUARE).resize((40, 40))
        # make the png darker due to not being able to find a better png
        enhancer = ImageEnhance.Brightness(image)
        darker_image = enhancer.enhance(0.9)

        # Load the icons for the dynamic buttons
        self.square_icon = ImageTk.PhotoImage(darker_image)
        self.hexagon_icon = ImageTk.PhotoImage(Image.open(self.constants.HEXAGON).resize((40, 45)).rotate(90, expand=True))
        self.triangle_icon = ImageTk.PhotoImage(Image.open(self.constants.TRIANGLE).resize((50, 50)))
        self.circle_icon = ImageTk.PhotoImage(Image.open(self.constants.CIRCLE_PATTERN).resize((40, 40)))
        self.star_icon = ImageTk.PhotoImage(Image.open(self.constants.STAR_PATTERN).resize((50, 50)))
        self.heart_icon = ImageTk.PhotoImage(Image.open(self.constants.HEART_PATTERN).resize((45, 45)))

        # Button frame for holding buttons, now added to layout
        button_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0, height=screen_height*0.6, width=screen_width*0.1)
        button_frame.grid(row=1, column=2, sticky="nsew", rowspan=1, pady=(50,0), padx=0)  # Set grid position for button_frame

        # Define 'Back' button dimensions and create a fram to place it in
        button_width, button_height = 200, 70
        back_button_frame = tk.Frame(self, width=button_width, height=button_height,bg=self.constants.background_color, highlightthickness=0, borderwidth=0)
        back_button_frame.grid(row=2, column=0, sticky="sw", padx=20, pady=20)

        # Add the 'back' button on top of the background image
        back_button = self.button.RoundedButton(
            master=back_button_frame,
            text="Bakåt",
            radius=20,
            width=200,
            height=70,
            btnbackground=self.constants.text_color, 
            btnforeground=self.constants.background_color, 
            clicked=self.go_back
        )
        back_button.place(relx=0.5, rely=0.5, anchor="center")

        # Frames for each of the 'premade pattern' buttons
        # Square
        btn_rec = self.button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=200, 
                                       height=70, 
                                       btnbackground=self.constants.text_color, 
                                       btnforeground=self.constants.background_color, 
                                       image=self.square_icon,
                                       clicked=lambda: self.hex.draw_square())
        # Hexagon
        btn_hexa = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.hexagon_icon,
                                        clicked=lambda: self.hex.draw_hexagon())
        # Triangle
        btn_tri = self.button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=200, 
                                       height=70, 
                                       btnbackground=self.constants.text_color, 
                                       btnforeground=self.constants.background_color, 
                                       image=self.triangle_icon,
                                       clicked=lambda: self.hex.draw_triangle())
        # Circle
        btn_circle = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.circle_icon,
                                        clicked=lambda: self.hex.draw_circle())
        # Heart
        btn_heart = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.heart_icon,
                                        clicked=lambda: self.hex.draw_heart())
        # Star
        btn_star = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.star_icon,
                                        clicked=lambda: self.hex.draw_star())
        
        # Label for premade patterns & underline
        btn_label = tk.Label(master=button_frame, 
                             text = "Färdiga mönster", 
                             font=(self.constants.heading, 24), 
                             fg=self.constants.text_color, 
                             bg=self.constants.background_color)
        btn_line_canvas = tk.Canvas(button_frame, width=200, height=2, bg=self.constants.background_color, highlightthickness=0)
        btn_line_canvas.create_line(0, 0, 200, 0, fill=self.constants.text_color)

        # Aligning buttons within the premade button frame
        btn_label.grid(row=0, column=4, sticky="nsew", pady=5)
        btn_line_canvas.grid(row=1, column=4)  # Add padding above and below the line
        btn_rec.grid(row=2, column=4, sticky="nsew", pady=20)
        btn_hexa.grid(row=3, column=4, sticky="nsew", pady=20)
        btn_tri.grid(row=4, column=4, sticky="nsew", pady=20)
        btn_circle.grid(row=5, column=4, sticky="nsew", pady=20)
        btn_heart.grid(row=6, column=4, sticky="nsew", pady=20)
        btn_star.grid(row=7, column=4, sticky="nsew", pady=20)


        # pattern frame for holding drawing board and label
        pattern_frame = tk.Frame(self, bg=self.constants.background_color, height=screen_height*0.7, width=screen_width*0.4)
        pattern_frame.grid(row=1, column=1, sticky="nsew", pady=0, padx=80, rowspan=2, columnspan=1)
        
         # Canvas to draw label
        label_line_canvas = tk.Canvas(pattern_frame, width=200, height=2, bg=self.constants.background_color, highlightthickness=0)
        label_line_canvas.create_line(0, 0, 200, 0, fill=self.constants.text_color)
        label = tk.Label(pattern_frame, text="Skapa ett mönster", font=(self.constants.heading, 24), 
                         fg=self.constants.text_color, bg=self.constants.background_color, justify="center")
        
        # Canvas for drawing patterns
        self.bg_canvas = tk.Canvas(pattern_frame, width=800, height=680, bg=self.constants.background_color, highlightthickness=0)
        self.hex = Patterns(self.bg_canvas, fill=self.constants.text_color, outline=self.constants.text_color)

        
        # Bind to draw the hexagon in the case of window resize
        self.bg_canvas.bind("<Configure>", self.on_resize)

        # Bind to handle mouse interactions
        self.bg_canvas.bind("<Button-1>", self.start_drawing)
        self.bg_canvas.bind("<B1-Motion>", self.draw)
        self.bg_canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Create initial hexagon
        self.create_hexagon()   


        self.hex.set_goal_function(self.send_goal_pos)
        self.bg_canvas.place(relx=0.5, rely=0.47, anchor="center")
        label.place(relx=0.5, rely=0.05, anchor="center")
        label_line_canvas.place(relx=0.5, rely=0.08, anchor="center")




        # in pattern frame
        # Pattern Page title
        label = tk.Label(pattern_frame, text="Skapa ett mönster", font=(self.constants.heading, 24), 
                         fg=self.constants.text_color, bg=self.constants.background_color, justify="center")
        
        btn_undo = self.button.RoundedButton(
                    master = pattern_frame, 
                    text="Ångra", 
                    radius=25, 
                    width=200, 
                    height=70, 
                    btnbackground=self.constants.text_color, 
                    btnforeground=self.constants.background_color, 
                    clicked=lambda: self.hex.reset_mapped_points() #self.hex.remove_last_line(), använder clear_all() istället
                )
        btn_undo.place(relx=0.5, rely=0.9, anchor="center")

       
        
    def create_hexagon_icon(self, size, outline_color="#000000"):
        # Create a transparent image
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Calculate the radius and center for the hexagon
        radius = size / 2
        center_x = size / 2
        center_y = size / 2

        # Calculate hexagon points
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append((x, y))
        
        # Draw hexagon on the image
        draw.polygon(points, fill=None, outline=outline_color)
        
        # Convert to a Tkinter-compatible image
        return ImageTk.PhotoImage(img)
    
    def send_goal_pos(self, x, y):
        if not self.goal_pos_queue.full():
            try:
                self.goal_pos_queue.put((x, y), timeout=0.01)
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            print(f"Queue goal pos is full!")
    
    def go_back(self):
        self.controller.show_frame("Home_page")
        self.hex.clear_all()  # Clear all shapes and lines before navigating
        self.hex.clear_pattern_data() #dont need to kill if we kill the power :)

    """---------------------------------------------PATTERN METHODS--------------------------------------------"""
    def create_hexagon(self):
        # Clear canvas
        self.bg_canvas.delete("all")
        
        # Find center and radius
        width = self.bg_canvas.winfo_width()
        height = self.bg_canvas.winfo_height()
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
        self.bg_canvas.create_polygon(self.points, outline=self.outline, fill=self.fill, width=2)


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
                    line_id = self.bg_canvas.create_line(last_x, last_y, event.x, event.y, fill="black")
                    self.current_line_ids.append(line_id)
                    self.drawing_points.append((event.x, event.y))

    def stop_drawing(self, event):
        self.clear_all()
        self.mapped_points = []
        # Connect the last point to the first to close the shape, if close enough
        if len(self.drawing_points) > 1:
            first_x, first_y = self.drawing_points[0]
            last_x, last_y = self.drawing_points[-1]
            if abs(last_x - first_x) <= 20 and abs(last_y - first_y) <= 20:
                line_id = self.bg_canvas.create_line(last_x, last_y, first_x, first_y, fill="black")
                self.current_line_ids.append(line_id)
        
        # Store the current completed line segments
        if self.current_line_ids:
            self.line_ids.append(self.current_line_ids)
            self.current_line_ids = []  # Reset for next line

        # Remap coordinates into cropped camera picture
        self.mapped_points = [self.map_coordinates(x, y) for x, y in self.drawing_points]
        print("Mapped drawing points", self.mapped_points)


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
    
    def clear_shapes_if_present(self):
        # Check if any shapes are in line_ids and remove them
        if self.line_ids:
            # Filter out all items tagged as "shape" from line_ids
            self.line_ids = [line for line in self.line_ids if "shape" not in self.canvas.gettags(line[0])]
            # Remove all items tagged "shape" from the canvas
            self.canvas.delete("shape")


    def reset_mapped_points(self):
        # Function for reseting position to [0, 0] when reseting pattern or going back to prev GUI slide

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
    
    def clear_pattern_data(self):

        while not self.data_queue.empty():
            self.data_queue.get_nowait()
        
        self.mapped_points = []
        self.send_goal_pos(0, 0)
        ''' # If we want to kill the thread 
        self.stop_event.set()
        self.thread.join()
        self.thread_started = False
        '''