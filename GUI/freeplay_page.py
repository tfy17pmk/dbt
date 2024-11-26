import tkinter as tk
import GUI.constants
import GUI.button
from math import atan2, cos, sin, sqrt


class Freeplay_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.button = GUI.button
        self.configure(bg=self.constants.background_color)
        

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
        
        # Frame to hold text, centered
        text_frame = tk.Frame(self, 
                              bg=self.constants.background_color, 
                              highlightthickness=0, 
                              height=screen_height*0.3, 
                              width=screen_width*0.75)
        text_frame.grid(row=1, column=1, rowspan=1, columnspan=1, pady=300, sticky="nsew")

        # Adding text to the text frame
        text_label = tk.Label(text_frame, 
                              text="Välkommen till balanssidan!", 
                              font=self.constants.heading, 
                              bg=self.constants.background_color, 
                              fg=self.constants.text_color)
        text_label.grid(row=0, column=0, sticky="nsew")

        additional_text = tk.Label(text_frame, 
                                   text="Här kan du testa balansera bollen själv,\nanvänd spakarna för att röra roboten i rätt riktning.", 
                                    font=self.constants.heading, 
                                    bg=self.constants.background_color, 
                                    fg=self.constants.text_color)
        additional_text.grid(row=1, column=0, sticky="nsew")

        # Joystick area
        joystick_frame = tk.Frame(self, bg=self.constants.background_color)
        joystick_frame.grid(row=2, column=2, sticky="e", padx=20)

        # Create a canvas for the joystick
        joystick_size = 150
        self.joystick_center = joystick_size // 2
        self.joystick_canvas = tk.Canvas(joystick_frame, width=joystick_size, height=joystick_size, bg=self.constants.background_color, highlightthickness=0)
        self.joystick_canvas.pack()

        # Draw joystick area 
        self.area_radius = 60
        self.joystick_area = self.joystick_canvas.create_oval(
            self.joystick_center - self.area_radius, 
            self.joystick_center - self.area_radius,
            self.joystick_center + self.area_radius, 
            self.joystick_center + self.area_radius,
            fill="#C8C8C8",
            outline="#C8C8C8"
        )

        # Initialize mapping range joystick
        self.new_min_joystick = -0.15
        self.old_min_joystick = -45
        self.new_max_joystick = 0.15
        self.old_max_joystick = 45

        # Draw the joystick handle
        self.handle_radius = 30
        self.handle = self.joystick_canvas.create_oval(
            self.joystick_center - self.handle_radius, 
            self.joystick_center - self.handle_radius,
            self.joystick_center + self.handle_radius, 
            self.joystick_center + self.handle_radius,
            fill="white",
            outline="white"
        )

        # Bind mouse events for joystick control
        self.joystick_canvas.bind("<B1-Motion>", self.move_handle)
        self.joystick_canvas.bind("<ButtonRelease-1>", self.reset_handle)

        # Back button frame
        back_btn_frame = tk.Frame(self, 
                                  bg=self.constants.background_color, 
                                  highlightthickness=0, 
                                  borderwidth=0)
        back_btn_frame.grid(row=2, column=0, sticky="sw")

        # Lower-left corner button to go back
        self.back_button = self.button.RoundedButton(
            master = back_btn_frame, 
            text="Bakåt", 
            radius=20, 
            width=200, 
            height=70, 
            btnbackground=self.constants.text_color, 
            btnforeground=self.constants.background_color, 
            clicked=lambda: controller.show_frame("Competition_page")
        )
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

    def map_joystick(self, value, event):
        target = self.new_min_joystick + (value - self.old_min_joystick) * (self.new_max_joystick - self.new_min_joystick) / (self.old_max_joystick - self.old_min_joystick)
        return target

    def move_handle(self, event):
        # Calculate the distance and angle from the center
        dx = event.x - self.joystick_center
        dy = event.y - self.joystick_center
        distance = sqrt(dx**2 + dy**2)

        # Limit the movement within joystick bounds
        if distance > self.joystick_center - self.handle_radius:
            # Restrict position to the edge of the larger circle
            angle = atan2(dy, dx)
            dx = cos(angle) * (self.joystick_center - self.handle_radius)
            dy = sin(angle) * (self.joystick_center - self.handle_radius)
            dx_mapped = dx * (0.15 / (self.joystick_center - self.handle_radius))
            dy_mapped = dy * (0.15 / (self.joystick_center - self.handle_radius))

        # Move the handle
        self.joystick_canvas.coords(
            self.handle,
            self.joystick_center + dx - self.handle_radius,
            self.joystick_center + dy - self.handle_radius,
            self.joystick_center + dx + self.handle_radius,
            self.joystick_center + dy + self.handle_radius
        )

        # Print the joystick's position relative to the center
        print(f"Joystick position: x={dx_mapped:.2f}, y={dy_mapped:.2f}")

    def reset_handle(self, event):
        # Reset the handle to the center
        self.joystick_canvas.coords(
            self.handle,
            self.joystick_center - self.handle_radius,
            self.joystick_center - self.handle_radius,
            self.joystick_center + self.handle_radius,
            self.joystick_center + self.handle_radius
        )
        print("Joystick position: x=0, y=0")  # Print center position when reset
