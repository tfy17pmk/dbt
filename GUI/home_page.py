from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import GUI.constants

# Page 1: Home Page
class Home_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.cropped_images = []

        # Load the background image
        bg_image = Image.open(GUI.constants.BG)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the scaling factor to fit the screen without distortion
        img_width, img_height = bg_image.size
        scale = max(screen_width / img_width, screen_height / img_height)

        # Resize the image to fit the screen while maintaining aspect ratio
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        bg_image = bg_image.resize((new_width, new_height), Image.LANCZOS)

        # Convert the resized image to a PhotoImage
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Create a Canvas to hold the background image
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        # Place the background image on the canvas and center it
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Scale button size relative to screen size
        button_diameter = int(screen_width * 0.25)

        # Load and resize images for each button
        # Replace 'path_to_image1.png' with the path to your actual image files
        self.info_image = Image.open(self.constants.INFO_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.competition_image = Image.open(self.constants.COMPETITION_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.pattern_image = Image.open(self.constants.PATTERN_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        
        # Convert images to PhotoImage for tkinter compatibility
        self.info_image = ImageTk.PhotoImage(self.info_image)
        self.competition_image = ImageTk.PhotoImage(self.competition_image)
        self.pattern_image = ImageTk.PhotoImage(self.pattern_image)

        def create_circular_button(canvas, text, command, image, canvas_x, canvas_y):
            # Calculate cropping area based on button position on the canvas
            crop_x = canvas_x - button_diameter // 2
            crop_y = canvas_y - button_diameter // 2

            # Ensure cropping coordinates are within bounds of the background image
            crop_x = max(0, crop_x)
            crop_y = max(0, crop_y)
            crop_y += 72
            crop_x_end = min(crop_x + button_diameter, bg_image.size[0])
            crop_y_end = min(crop_y + button_diameter, bg_image.size[1])

            # Crop the background image dynamically to use as the button's background
            cropped_bg = bg_image.crop((crop_x, crop_y, crop_x_end, crop_y_end))
            cropped_bg = cropped_bg.resize((button_diameter, button_diameter), Image.LANCZOS)
            cropped_bg_image = ImageTk.PhotoImage(cropped_bg)

            # Save reference to prevent garbage collection
            self.cropped_images.append(cropped_bg_image)

            # Create the button container (transparent)
            btn_container = tk.Frame(canvas, bd=0)
            btn_container.pack()

            # Canvas for the label
            label_canvas = tk.Canvas(
                btn_container,
                width=button_diameter,
                height=int(button_diameter * 0.3),  # Adjust label height
                highlightthickness=0,
                bd=0
            )
            label_canvas.pack()

            # Crop and apply the background for the label
            label_crop_y = crop_y - int(button_diameter * 0.3)
            label_crop_y = max(0, label_crop_y)
            label_cropped_bg = bg_image.crop((
                crop_x,
                label_crop_y,
                crop_x + button_diameter,
                label_crop_y + int(button_diameter * 0.3)
            ))
            label_cropped_bg = label_cropped_bg.resize((button_diameter, int(button_diameter * 0.3)), Image.LANCZOS)
            label_cropped_image = ImageTk.PhotoImage(label_cropped_bg)

            # Save reference to prevent garbage collection
            self.cropped_images.append(label_cropped_image)

            # Place the cropped label background and overlay text
            label_canvas.create_image(0, 0, image=label_cropped_image, anchor="nw")
            label_canvas.create_text(
                button_diameter // 2, int(button_diameter * 0.15),
                text=text,
                font=self.constants.heading,
                fill=self.constants.text_color
            )

            # Canvas for the button
            button_canvas = tk.Canvas(
                btn_container,
                width=button_diameter,
                height=button_diameter,
                highlightthickness=0,
                bd=0
            )
            button_canvas.pack()

            # Place the cropped background as the button's background
            button_canvas.create_image(0, 0, image=cropped_bg_image, anchor="nw")

            # Draw the button circle
            button_canvas.create_oval(
                5, 5, button_diameter - 5, button_diameter - 5,
                outline=self.constants.text_color,
                fill=self.constants.text_color,
                width=2
            )

            # Place the button icon
            button_canvas.create_image(button_diameter // 2, button_diameter // 2, image=image)

            # Bind the button action
            button_canvas.bind("<Button-1>", lambda e: command())

            # Add the button container to the main canvas
            canvas.create_window(canvas_x, canvas_y, window=btn_container, anchor="center")

        # Example button creation
        # Button properties
        button_diameter = int(screen_width * 0.25)  # Adjust button size as needed
        button_spacing = int(screen_width * 0.05)  # Space between buttons
        total_buttons = 3  # Number of buttons

        # Calculate the total width of the buttons row
        total_width = (button_diameter * total_buttons) + (button_spacing * (total_buttons - 1))

        # Calculate the starting X position to center the row
        start_x = (screen_width - total_width) // 2
        center_y = screen_height // 2

        # Create buttons dynamically, centering them
        create_circular_button(
            self.canvas,
            "Information",
            lambda: controller.show_frame("Info_page"),
            self.info_image,
            canvas_x=start_x + button_diameter // 2,
            canvas_y=center_y
        )

        create_circular_button(
            self.canvas,
            "Tävla",
            lambda: controller.show_frame("Competition_page"),
            self.competition_image,
            canvas_x=start_x + button_diameter + button_spacing + button_diameter // 2,
            canvas_y=center_y
        )

        create_circular_button(
            self.canvas,
            "Skapa Mönster",
            lambda: controller.show_frame("Pattern_page"),
            self.pattern_image,
            canvas_x=start_x + 2 * (button_diameter + button_spacing) + button_diameter // 2,
            canvas_y=center_y
        )