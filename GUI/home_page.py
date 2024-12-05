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
        self.circular_buttons_object = []
        self.circular_buttons_id = []
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Convert the resized image to a PhotoImage

        # Create a Canvas to hold the background image
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, highlightthickness=0, bd=0)
        self.canvas.config(bg=self.constants.background_color)
        self.canvas.pack(fill="both", expand=True)


        # Scale button size relative to screen size
        button_diameter = int(screen_width * 0.25)

        # Load and resize images for each button
        # Replace 'path_to_image1.png' with the path to your actual image files
        self.info_image = Image.open(self.constants.INFO_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.competition_image = Image.open(self.constants.JOYSTICK).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        self.pattern_image = Image.open(self.constants.PATTERN_IMAGE).resize((button_diameter // 2, button_diameter // 2), Image.LANCZOS)
        
        # Convert images to PhotoImage for tkinter compatibility
        self.info_image = ImageTk.PhotoImage(self.info_image)
        self.competition_image = ImageTk.PhotoImage(self.competition_image)
        self.pattern_image = ImageTk.PhotoImage(self.pattern_image)

        def create_circular_button(canvas, text, command, image, canvas_x, canvas_y):

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
            label_canvas.config(bg=self.constants.background_color)
            label_canvas.pack()

            # Place the label background and overlay text
            text_id = label_canvas.create_text(
                button_diameter // 2, int(button_diameter * 0.15),
                text=text,
                font=self.constants.heading,
                fill=self.constants.text_color
            )
            self.circular_buttons_id.append(text_id)

            # Canvas for the button
            button_canvas = tk.Canvas(
                btn_container,
                width=button_diameter,
                height=button_diameter,
                highlightthickness=0,
                bd=0
            )
            button_canvas.pack()
            button_canvas.config(bg=self.constants.background_color)

            # Draw the button circle
            button_canvas.create_oval(
                5, 5, button_diameter - 5, button_diameter - 5,
                outline=self.constants.text_color,
                fill=self.constants.text_color,
                width=2,
                tags="button_clickable"
            )

            # Place the button icon
            button_canvas.create_image(
                button_diameter // 2, 
                button_diameter // 2, 
                image=image, 
                tags="button_clickable"
            )

            # Bind the button action
            button_canvas.tag_bind("button_clickable", "<Button-1>", lambda e: command())

            # Add the button container to the main canvas
            canvas.create_window(canvas_x, canvas_y, window=btn_container, anchor="center")
            return label_canvas

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
        self.circular_buttons_object.append(create_circular_button(
            self.canvas,
            "Information",
            lambda: controller.show_frame("Info_page"),
            self.info_image,
            canvas_x=start_x + button_diameter // 2,
            canvas_y=center_y
        ))

        self.circular_buttons_object.append(create_circular_button(
            self.canvas,
            "Balansera Själv",
            lambda: controller.show_frame("Freeplay_page"),
            self.competition_image,
            canvas_x=start_x + button_diameter + button_spacing + button_diameter // 2,
            canvas_y=center_y
        ))

        self.circular_buttons_object.append(create_circular_button(
            self.canvas,
            "Skapa Mönster",
            lambda: controller.show_frame("Pattern_page"),
            self.pattern_image,
            canvas_x=start_x + 2 * (button_diameter + button_spacing) + button_diameter // 2,
            canvas_y=center_y
        ))
        
        
        # Load and resize images for the language options
        self.sv_icon = ImageTk.PhotoImage(Image.open(self.constants.SV).resize((50, 50), Image.LANCZOS))
        self.en_icon = ImageTk.PhotoImage(Image.open(self.constants.EN).resize((50, 50), Image.LANCZOS))

        # Add Swedish language canvas image
        sv_image = self.canvas.create_image(
            60,  # Adjust to place near the right edge
            screen_height - 70,  # Adjust to place near the bottom edge
            image=self.sv_icon,
            anchor="center"
        )

        # Bind click event to the Swedish image
        self.canvas.tag_bind(sv_image, "<Button-1>", lambda event: switch_language("sv"))

        # Add English language canvas image
        en_image = self.canvas.create_image(
            130,  # Adjust to place left of the Swedish image
            screen_height - 70,  # Align with the Swedish image
            image=self.en_icon,
            anchor="center"
        )

        # Bind click event to the English image
        self.canvas.tag_bind(en_image, "<Button-1>", lambda event: switch_language("en"))
        
        # Add highlight circles for the flags
        self.sv_highlight = self.canvas.create_oval(
            35,  # Adjust based on flag position
            screen_height - 95,  # Adjust based on flag position
            85,  # Adjust based on flag size
            screen_height - 45,  # Adjust based on flag size
            outline=self.constants.text_color,  # Highlight color
            width=2,
            state="hidden"  # Initially hidden
        )

        self.en_highlight = self.canvas.create_oval(
            105,  # Adjust based on flag position
            screen_height - 95,  # Adjust based on flag position
            155,  # Adjust based on flag size
            screen_height - 45,  # Adjust based on flag size
            outline=self.constants.text_color,  # Highlight color
            width=2,
            state="hidden"  # Initially hidden
        )
        
        # Uppdates the higlited language
        if self.controller.set_language == "sv":
            self.canvas.itemconfig(self.sv_highlight, state="normal")  # Show Swedish highlight
            self.canvas.itemconfig(self.en_highlight, state="hidden")  # Hide English highlight
        elif self.controller.set_language == "en":
            self.canvas.itemconfig(self.en_highlight, state="normal")  # Show English highlight
            self.canvas.itemconfig(self.sv_highlight, state="hidden")  # Hide Swedish highlight
        


        # Add a function to handle language switching
        def switch_language(lang_code):
            self.controller.set_language = lang_code  # Assuming the controller has a method to set the language
            self.controller.update_text()
            
            if self.controller.set_language == "sv":
                self.canvas.itemconfig(self.sv_highlight, state="normal")  # Show Swedish highlight
                self.canvas.itemconfig(self.en_highlight, state="hidden")  # Hide English highlight
            elif self.controller.set_language == "en":
                self.canvas.itemconfig(self.en_highlight, state="normal")  # Show English highlight
                self.canvas.itemconfig(self.sv_highlight, state="hidden")  # Hide Swedish highlight
               
             
    def update_labels(self, texts):    
        
        tmp = self.circular_buttons_object[1]
        id = self.circular_buttons_id[1]
        tmp.itemconfig(id, text=texts["control"])    

        tmp = self.circular_buttons_object[2]
        id = self.circular_buttons_id[2]
        tmp.itemconfig(id, text=texts["create_pattern"])

