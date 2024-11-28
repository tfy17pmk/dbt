import tkinter as tk
import GUI.constants
import GUI.button
from math import atan2, cos, sin, sqrt
import time



class Freeplay_page(tk.Frame):
    def __init__(self, parent, controller, joystick_control_queue):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.button = GUI.button
        self.configure(bg=self.constants.background_color)
        self.joystick_control_queue = joystick_control_queue
        self.last_time = time.time()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Setup grid pattern with equal weight for each row and column
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=0)
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
        text_frame.grid(row=0, column=1, pady=(0,0), sticky="")

        # Adding text to the text frame
        text_label = tk.Label(text_frame, 
                              text="Välkommen till balanssidan!\n", 
                              font=self.constants.heading, 
                              bg=self.constants.background_color, 
                              fg=self.constants.text_color)
        text_label.grid(row=0, column=0, sticky="nsew")

        additional_text = tk.Label(text_frame, 
                                   text="Här kan du testa balansera bollen själv,\nanvänd spaken för att röra roboten.\nSpaken hittar du nere i högra hörnet.", 
                                    font=self.constants.sub_heading, 
                                    bg=self.constants.background_color, 
                                    fg=self.constants.text_color)
        additional_text.grid(row=1, column=0, sticky="nsew")

        # Joystick area
        joystick_frame = tk.Frame(self, bg=self.constants.background_color)
        joystick_frame.grid(row=2, column=2, sticky="e", padx=20)

        # Create a canvas for the joystick
        joystick_size = 300
        self.joystick_center = joystick_size // 2
        self.joystick_canvas = tk.Canvas(joystick_frame, width=joystick_size, height=joystick_size, bg=self.constants.background_color, highlightthickness=0)
        self.joystick_canvas.pack()

        # Draw joystick area 
        self.area_radius = 120
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
        self.handle_radius = 40
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
            clicked=self.go_back
        )
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

        self.maxnormal = 0.15
    

    def move_handle(self, event):
        # Calculate the distance and angle from the center
        dx = (event.x - self.joystick_center)
        dy = (event.y - self.joystick_center)
        distance = sqrt(dx**2 + dy**2)

        # Limit the movement within joystick bounds
        if distance > self.joystick_center - self.handle_radius:
            # Restrict position to the edge of the larger circle
            angle = atan2(dy, dx)
            dx = cos(angle) * (self.joystick_center - self.handle_radius)
            dy = sin(angle) * (self.joystick_center - self.handle_radius)
            '''dx_mapped = float(dx * (0.15 / (self.joystick_center - self.handle_radius)))
            dy_mapped = float(dy * (0.15 / (self.joystick_center - self.handle_radius)))'''


        # Move the handle
        self.joystick_canvas.coords(
            self.handle,
            self.joystick_center + dx - self.handle_radius,
            self.joystick_center + dy - self.handle_radius,
            self.joystick_center + dx + self.handle_radius,
            self.joystick_center + dy + self.handle_radius
        )

        dx = dx * (self.maxnormal / (self.joystick_center - self.handle_radius))
        dy = dy * (self.maxnormal / (self.joystick_center - self.handle_radius))

        self.send_joystick_control(dx, dy)


    def reset_handle(self, event):
        # Reset the handle to the center
        self.joystick_canvas.coords(
            self.handle,
            self.joystick_center - self.handle_radius,
            self.joystick_center - self.handle_radius,
            self.joystick_center + self.handle_radius,
            self.joystick_center + self.handle_radius
        )
        self.send_joystick_control(0.14, 0.14)
        self.send_joystick_control(0.14, 0.14)
        self.send_joystick_control(0.14, 0.14)
        self.send_joystick_control(0.14, 0.14)
        self.send_joystick_control(0.14, 0.14)
        self.send_joystick_control(0, 0)
        self.send_joystick_control(0, 0)
        self.send_joystick_control(0, 0)
        self.send_joystick_control(0, 0)
        self.send_joystick_control(0, 0)


    def send_joystick_control(self, dx, dy):
        if not self.joystick_control_queue.full():
            try:
                #if time.time() - self.last_time > 0.1:
                    self.joystick_control_queue.put_nowait((dx, dy))
                    #self.last_time = time.time()
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            print(f"Queue joystick control is full!")

    def go_back(self):
        self.controller.show_frame("Competition_page")
        self.joystick_control_queue.put_nowait(False)
