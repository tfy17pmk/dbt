import tkinter as tk
import constants
import button


# Competition page
class Competition_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Setup grid pattern with equal weight for each row and column
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)

        # Scale button size relative to screen size (e.g., 10% of the screen width)
        button_diameter = int(screen_width * 0.25)

        # Frame to hold buttons and text in a single row, centered
        button_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0)
        button_frame.grid(row=1, column=1, rowspan=1, columnspan=1, padx=30, sticky="nsew")  # Center button frame in the middle of Home_page

        back_btn_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0)
        back_btn_frame.grid(row=2, column=0, sticky="sw")

        # Custom function to create circular buttons with labels and images
        def create_circular_button(frame, text, command):
            # Frame for each button and its label
            btn_container = tk.Frame(frame, bg=constants.background_color)
            btn_container.pack(side="left", padx=40)

            # Label above the button with extra vertical padding
            btn_label = tk.Label(btn_container, text=text, font=constants.heading, bg=constants.background_color, fg=constants.text_color)
            btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

            # Canvas for circular button, based on calculated button diameter
            canvas = tk.Canvas(btn_container, width=button_diameter, height=button_diameter, highlightthickness=0, bg=constants.background_color)
            canvas.pack()

            # Draw circular button shape with calculated diameter
            button_circle = canvas.create_oval(
                5, 5, button_diameter - 5, button_diameter - 5, fill="#B9D9EB"
            )

            # Button action using a lambda
            canvas.bind("<Button-1>", lambda e: command())

        # Create the circular buttons with labels above and resized images in the center
        create_circular_button(button_frame, "Utmaning", lambda: controller.show_frame("Challenge_page"))
        create_circular_button(button_frame, "Balansera själv", lambda: controller.show_frame("Freeplay_page"))

        # Lower-left corner button to go back
        self.back_button = button.RoundedButton(
            master = back_btn_frame, 
            text="Bakåt", 
            radius=20, 
            width=200, 
            height=70, 
            btnbackground=constants.text_color, 
            btnforeground=constants.background_color, 
            clicked=lambda: controller.show_frame("Home_page")
        )
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")
     
