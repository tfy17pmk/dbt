import tkinter as tk
import config

# Page 3: Page Two
class Competition_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=config.background_color)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Home button
        button = tk.Button(self, text="Back to Home Page",
                           command=lambda: controller.show_frame("Home_page"))
        button.pack()

        # Scale button size relative to screen size (e.g., 10% of the screen width)
        button_diameter = int(screen_width * 0.25)

        # Frame to hold buttons and text in a single row, centered
        button_frame = tk.Frame(self, bg=config.background_color)
        button_frame.pack(anchor="center", expand=True)  # Center button frame in the middle of Home_page

        # Custom function to create circular buttons with labels and images
        def create_circular_button(frame, text, command):
            # Frame for each button and its label
            btn_container = tk.Frame(frame, bg=config.background_color)
            btn_container.pack(side="left", padx=40)

            # Label above the button with extra vertical padding
            btn_label = tk.Label(btn_container, text=text, font=config.heading, bg=config.background_color, fg=config.text_color)
            btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

            # Canvas for circular button, based on calculated button diameter
            canvas = tk.Canvas(btn_container, width=button_diameter, height=button_diameter, highlightthickness=0, bg=config.background_color)
            canvas.pack()

            # Draw circular button shape with calculated diameter
            button_circle = canvas.create_oval(
                5, 5, button_diameter - 5, button_diameter - 5, fill="#B9D9EB"
            )

            # Button action using a lambda
            canvas.bind("<Button-1>", lambda e: command())

        # Create the circular buttons with labels above and resized images in the center
        create_circular_button(button_frame, "Tävla", lambda: controller.show_frame("Info_page"))
        create_circular_button(button_frame, "Balansera själv", lambda: controller.show_frame("Competition_page"))
     
