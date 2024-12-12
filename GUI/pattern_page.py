from tkinter import *
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageEnhance
import GUI.constants
import GUI.button
import GUI.hexagon
from GUI.hexagon import HexagonShape
import math
import threading

# Page 3: Practice mode
class Pattern_page(tk.Frame):
    """Page containing buttons to make robot roll ball in a pattern 
    and drawing board to make ball roll in custom pattern."""

    def __init__(self, parent, controller, goal_pos_queue):
        """Initializes the page."""
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.button = GUI.button
        self.hexagon = GUI.hexagon
        self.goal_pos_queue = goal_pos_queue

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
        button_width = 200
        button_height = 70

        # Modifying the square image for the suare pattern button
        image = Image.open(self.constants.SQUARE).resize((40, 40))
        enhancer = ImageEnhance.Brightness(image)
        darker_image = enhancer.enhance(0.9)

        # Load the icons for the dynamic pattern buttons
        self.square_icon = ImageTk.PhotoImage(darker_image)
        self.hexagon_icon = ImageTk.PhotoImage(Image.open(self.constants.HEXAGON).resize((40, 45)).rotate(90, expand=True))
        self.triangle_icon = ImageTk.PhotoImage(Image.open(self.constants.TRIANGLE).resize((50, 50)))
        self.circle_icon = ImageTk.PhotoImage(Image.open(self.constants.CIRCLE_PATTERN).resize((40, 40)))
        self.star_icon = ImageTk.PhotoImage(Image.open(self.constants.STAR_PATTERN).resize((50, 50)))
        self.heart_icon = ImageTk.PhotoImage(Image.open(self.constants.HEART_PATTERN).resize((45, 45)))

        # Frame for holding buttons
        button_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0, height=screen_height*0.6, width=screen_width*0.1)
        button_frame.grid(row=1, column=2, sticky="nsew", rowspan=1, pady=(50,0), padx=0)

        # Frame for 'Back' button
        back_button_frame = tk.Frame(self, width=button_width, height=button_height,bg=self.constants.background_color, highlightthickness=0, borderwidth=0)
        back_button_frame.grid(row=2, column=0, sticky="sw", padx=20, pady=20)

        # Create 'back' button
        self.back_button = self.button.RoundedButton(
            master=back_button_frame,
            text=self.constants.translation[self.controller.set_language]["back"],
            radius=20,
            width=button_width,
            height=button_height,
            btnbackground=self.constants.text_color, 
            btnforeground=self.constants.background_color, 
            clicked=self.go_back
        )
        self.back_button.place(relx=0.5, rely=0.5, anchor="center")

        # Frames for each of the 'premade pattern' buttons
        # Square
        btn_rec = self.button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=button_width, 
                                       height=button_height, 
                                       btnbackground=self.constants.text_color, 
                                       btnforeground=self.constants.background_color, 
                                       image=self.square_icon,
                                       clicked=lambda: self.hex.draw_square())
        # Hexagon
        btn_hexa = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=button_width, 
                                        height=button_height, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.hexagon_icon,
                                        clicked=lambda: self.hex.draw_hexagon())
        # Triangle
        btn_tri = self.button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=button_width, 
                                       height=button_height, 
                                       btnbackground=self.constants.text_color, 
                                       btnforeground=self.constants.background_color, 
                                       image=self.triangle_icon,
                                       clicked=lambda: self.hex.draw_triangle())
        # Circle
        btn_circle = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=button_width, 
                                        height=button_height, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.circle_icon,
                                        clicked=lambda: self.hex.draw_circle())
        # Heart
        btn_heart = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=button_width, 
                                        height=button_height, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.heart_icon,
                                        clicked=lambda: self.hex.draw_heart())
        # Star
        btn_star = self.button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=button_width, 
                                        height=button_height, 
                                        btnbackground=self.constants.text_color, 
                                        btnforeground=self.constants.background_color, 
                                        image=self.star_icon,
                                        clicked=lambda: self.hex.draw_star())
        
        # Label for premade patterns & underline
        self.btn_label = tk.Label(master=button_frame, 
                             text = self.constants.translation[self.controller.set_language]["premade_patterns"], 
                             font=(self.constants.heading, 24), 
                             fg=self.constants.text_color, 
                             bg=self.constants.background_color)
        btn_line_canvas = tk.Canvas(button_frame, width=200, height=2, bg=self.constants.background_color, highlightthickness=0)
        btn_line_canvas.create_line(0, 0, 200, 0, fill=self.constants.text_color)

        # Aligning buttons within the premade button frame
        self.btn_label.grid(row=0, column=4, sticky="nsew", pady=5)
        btn_line_canvas.grid(row=1, column=4)
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
        self.label = tk.Label(pattern_frame, text=self.constants.translation[self.controller.set_language]["create_your_pattern"], font=(self.constants.heading, 24), 
                         fg=self.constants.text_color, bg=self.constants.background_color, justify="center")
        
        # Canvas for drawing patterns
        self.bg_canvas = tk.Canvas(pattern_frame, width=800, height=680, bg=self.constants.background_color, highlightthickness=0)
        self.hex = HexagonShape(self.bg_canvas, fill=self.constants.text_color, outline=self.constants.text_color)
        self.hex.set_goal_function(self.send_goal_pos)
        self.bg_canvas.place(relx=0.5, rely=0.47, anchor="center")
        self.label.place(relx=0.5, rely=0.05, anchor="center")
        label_line_canvas.place(relx=0.5, rely=0.08, anchor="center")
        
        # Create undo button
        self.btn_undo = self.button.RoundedButton(
            master = pattern_frame, 
            text=self.constants.translation[self.controller.set_language]["undo"], 
            radius=25, 
            width=button_width, 
            height=button_height, 
            btnbackground=self.constants.text_color, 
            btnforeground=self.constants.background_color, 
            clicked=lambda: self.hex.reset_mapped_points()
        )
        self.btn_undo.place(relx=0.5, rely=0.9, anchor="center") 
            
    def send_goal_pos(self, x, y):
        """Send new goal positions to main"""
        if not self.goal_pos_queue.full():
            try:
                self.goal_pos_queue.put((x, y), timeout=0.01)
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            # Empty the queue so it gets the most recent goal position.
            while not self.goal_pos_queue.empty():
                self.goal_pos_queue.get_nowait()
            print(f"Queue goal pos is full!")
    
    def go_back(self):
        """Clear drawing board of input and return to previous page"""
        self.controller.show_frame("Home_page")
        self.hex.clear_all()  # Clear all shapes and lines before navigating
        self.hex.clear_thread() # Dont need to kill the thread if we kill the power
        
    def update_labels(self, texts):    
        """Update labels when language is changed in home page."""
        self.btn_label.config(text=texts["premade_patterns"])    
        self.label.config(text=texts["create_your_pattern"])
        self.btn_undo.update_text(texts["undo"])
        self.back_button.update_text(texts["back"])

    def join_threads(self):
        """Kill thread when keyboard interrupt is called"""
        self.hex.join_threads()
