from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for image resizing
import GUI.constants

# Page 1: Home Page
class Home_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        

       # bg_img = tk.PhotoImage(file = "orange.png")
        #label = tk.Label( self, image = bg_img) 
        #label.place(x = 0, y = 0) 
        
        #photo = PhotoImage(file = "orange.png")
        #lbl = Label(image=photo)
        #lbl.image = photo # keep a reference!
        #lbl.pack()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Scale button size relative to screen size (e.g., 10% of the screen width)
        button_diameter = int(screen_width * 0.25)  # Adjust the percentage as needed

        # Load and resize images for each button
        # Replace 'path_to_image1.png' with the path to your actual image files
        self.info_image = Image.open(constants.INFO_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.competition_image = Image.open(constants.COMPETITION_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.pattern_image = Image.open(constants.PATTERN_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        
        # Convert images to PhotoImage for tkinter compatibility
        self.info_image = ImageTk.PhotoImage(self.info_image)
        self.competition_image = ImageTk.PhotoImage(self.competition_image)
        self.pattern_image = ImageTk.PhotoImage(self.pattern_image)

        # Frame to hold buttons and text in a single row, centered
        self.image = PhotoImage(file="orange.png")  # Replace with your file path

        # Create a label to hold the image
        background_label = tk.Label(self, image=self.image)
        background_label.place(relwidth=1, relheight=1)

        button_frame = tk.Frame(self)
        button_frame.pack(anchor="center", expand=True) 


       # button_frame = tk.Frame(self, bg=constants.background_color)
        #button_frame.pack(anchor="center", expand=True)  # Center button frame in the middle of Home_page

        # Custom function to create circular buttons with labels and images
        def create_circular_button(frame, text, command, image):
            # Frame for each button and its label
            btn_container = tk.Frame(frame, bg=self.constants.background_color)
            btn_container.pack(side="left", padx=40)

            # Label above the button with extra vertical padding
            btn_label = tk.Label(btn_container, text=text, font=self.constants.heading, bg=self.constants.background_color, fg=self.constants.text_color)
            btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

            # Canvas for circular button, based on calculated button diameter
            canvas = tk.Canvas(btn_container, width=button_diameter, height=button_diameter, highlightthickness=0, bg=self.constants.background_color)
            canvas.pack()

            # Draw circular button shape with calculated diameter
            button_circle = canvas.create_oval(
                5, 5, button_diameter - 5, button_diameter - 5, fill=self.constants.text_color
            )

            # Place the resized image in the center of the button
            canvas.create_image(button_diameter // 2, button_diameter // 2, image=image)

            # Button action using a lambda
            canvas.bind("<Button-1>", lambda e: command())

        # Create the circular buttons with labels above and resized images in the center
        create_circular_button(button_frame, "Information", lambda: controller.show_frame("Info_page"), self.info_image)
        create_circular_button(button_frame, "Tävla", lambda: controller.show_frame("Competition_page"), self.competition_image)
        create_circular_button(button_frame, "Skapa Mönster", lambda: controller.show_frame("Pattern_page"), self.pattern_image)

        # Center Home_page frame and allow expansion to center contents
        self.pack(expand=True, fill="both")
