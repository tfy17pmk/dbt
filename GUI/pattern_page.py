from tkinter import *
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk  # Import Pillow for image resizing
import constants
import button
import Hexagon
from Hexagon import HexagonShape
import math

# Page 3: Page Two
class Pattern_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)

        # Load the light icon for the dynamic buttons
        self.square_icon = ImageTk.PhotoImage(Image.open(constants.SQUARE).resize((40, 40)))
        self.hexagon_icon = self.create_hexagon_icon(40, outline_color="black")
        self.triangle_icon = ImageTk.PhotoImage(Image.open(constants.TRIANGLE).resize((40, 40)))
        self.star_icon = ImageTk.PhotoImage(Image.open(constants.STAR).resize((40, 40)))

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        button_width = int(screen_width * 0.05)
        button_height = int(screen_height * 0.05)

        # Setup grid pattern with equal weight for each row and column
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)


        # Button frame for holding buttons, now added to layout
        button_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0, height=screen_height*0.5, width=screen_width*0.1)
        button_frame.grid(row=1, column=2, sticky="nsew", rowspan=1, pady=180, padx=0)  # Set grid position for button_frame

        # Go back frame
        back_button_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0)
        back_button_frame.config(borderwidth=0, highlightthickness=0)
        back_button_frame.grid(row=2, column=0, sticky="sw")

        # pattern frame for holding drawing board and label
        pattern_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0,
                                  height=screen_height*0.7, width=screen_width*0.4)
        pattern_frame.grid(row=1, column=1, sticky="nsew", pady=0, padx=80, rowspan=2, columnspan=1)
        
         # Canvas to draw the line
        label_line_canvas = tk.Canvas(pattern_frame, width=200, height=2, bg=constants.background_color, highlightthickness=0)
        label_line_canvas.create_line(0, 0, 200, 0, fill=constants.text_color)
        
        label = tk.Label(pattern_frame, text="Skapa ett mönster", font=(constants.heading, 24), 
                         fg=constants.text_color, bg=constants.background_color, justify="center")
        
        # Canvas for creating patterns
        self.canvas = tk.Canvas(pattern_frame, width=800, height=680, bg=constants.background_color, highlightthickness=0)
        self.hex = Hexagon.HexagonShape(self.canvas, fill=constants.text_color, outline=constants.text_color)
        self.canvas.place(relx=0.5, rely=0.47, anchor="center")
        label.place(relx=0.5, rely=0.05, anchor="center")
        label_line_canvas.place(relx=0.5, rely=0.08, anchor="center")  # Add padding above and below the line

        # in button frame
        btn_rec = button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=200, 
                                       height=70, 
                                       btnbackground=constants.text_color, 
                                       btnforeground=constants.background_color, 
                                       image=self.square_icon,
                                       clicked=lambda: self.hex.draw_square())
        
        btn_hexa = button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=constants.text_color, 
                                        btnforeground=constants.background_color, 
                                        image=self.hexagon_icon,
                                        clicked=lambda: self.hex.draw_hexagon())
        
        btn_tri = button.RoundedButton(master = button_frame, 
                                       text="", 
                                       radius=25, 
                                       width=200, 
                                       height=70, 
                                       btnbackground=constants.text_color, 
                                       btnforeground=constants.background_color, 
                                       image=self.triangle_icon,
                                       clicked=lambda: self.hex.draw_triangle())
        
        btn_star = button.RoundedButton(master = button_frame, 
                                        text="", 
                                        radius=25, 
                                        width=200, 
                                        height=70, 
                                        btnbackground=constants.text_color, 
                                        btnforeground=constants.background_color, 
                                        image=self.star_icon,
                                        clicked=lambda: self.hex.draw_star())
        
        btn_label = tk.Label(master=button_frame, 
                             text = "Färdiga mönster", 
                             font=(constants.heading, 24), 
                             fg=constants.text_color, 
                             bg=constants.background_color)
        
        # Canvas to draw the line
        btn_line_canvas = tk.Canvas(button_frame, width=200, height=2, bg=constants.background_color, highlightthickness=0)
        btn_line_canvas.create_line(0, 0, 200, 0, fill=constants.text_color)

        btn_label.grid(row=0, column=4, sticky="nsew", pady=5)
        btn_line_canvas.grid(row=1, column=4)  # Add padding above and below the line
        btn_rec.grid(row=2, column=4, sticky="nsew", pady=20)
        btn_hexa.grid(row=3, column=4, sticky="nsew", pady=20)
        btn_tri.grid(row=4, column=4, sticky="nsew", pady=20)
        btn_star.grid(row=5, column=4, sticky="nsew", pady=20)

        # in pattern frame
        # Pattern Page title
        label = tk.Label(pattern_frame, text="Skapa ett mönster", font=(constants.heading, 24), 
                         fg=constants.text_color, bg=constants.background_color, justify="center")
        
        btn_undo = button.RoundedButton(
                    master = pattern_frame, 
                    text="Ångra", 
                    radius=25, 
                    width=200, 
                    height=70, 
                    btnbackground=constants.text_color, 
                    btnforeground=constants.background_color, 
                    clicked=lambda: self.hex.reset_mapped_points() #self.hex.remove_last_line(), använder clear_all() istället
                )
        btn_undo.place(relx=0.5, rely=0.9, anchor="center")

        # Lower-left corner button to go back
        self.back_button = button.RoundedButton(
            master = back_button_frame, 
            text="Bakåt", 
            radius=20, 
            width=200, 
            height=70, 
            btnbackground=constants.text_color, 
            btnforeground=constants.background_color, 
            clicked=lambda: (self.go_back(), self.hex.reset_mapped_points())
        )
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")
        
    def create_hexagon_icon(self, size, outline_color="#000000"):
        """
        Creates a hexagon-shaped icon as an image.
        
        Parameters:
            size (int): Size of the image (width and height) to contain the hexagon.
            outline_color (str): Outline color for the hexagon.
        
        Returns:
            ImageTk.PhotoImage: The generated hexagon icon image.
        """
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
    
    def go_back(self):
        print("inside go back")
        self.hex.clear_all()  # Clear all shapes and lines before navigating
        self.controller.show_frame("Home_page")