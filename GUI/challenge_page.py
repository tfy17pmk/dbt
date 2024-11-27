import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import GUI.button as button
import GUI.constants as constants
from GUI.class_challenges import Challenges
from math import atan2, cos, sin, sqrt
from multiprocessing import Lock
import threading
import time

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller, resources):
        super().__init__(parent)
        self.controller = controller
        self.gui_frame_queue = resources.gui_challange_frame_queue
        self.ball_coords_queue = resources.ball_coords_gui_queue
        self.send_frames = resources.send_frames_to_challenge
        self.goal_pos_queue = resources.goal_position_queue
        self.joystick_control_queue = resources.joystick_control_queue
        self.isJoystick = False
        self.start_time = None
        self.robot_time = None
        self.user_time = None
        self.stop_event = threading.Event()
        self.thread_started = False

        self.configure(bg=constants.background_color)
        self.page_texts = constants.challenge_text
        self.button_diameter = 200
            
        # Output frame size
        self.current_frame = None
        self.frame_height, self.frame_width = 285, 320
        self.cam_width = int(self.frame_width*2.5)
        self.cam_height = int(self.frame_height*2.5)

        # Frame for the video feed
        self.cam_frame = tk.Label(self) #
        self.cam_frame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="new", padx=(30,20), pady=(30,0))  # Place below text widget in grid

        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=constants.body_text,
            bg=constants.background_color, 
            fg=constants.text_color,
            relief="flat", 
            height=6, 
            width=20, 
            highlightthickness=0,
            padx=20,
            pady=50
        )

        # Configure text tags for heading and body text styles. Add it to column 1
        self.page_content_text.tag_configure("heading", font=constants.heading, foreground=constants.text_color, justify="center")
        self.page_content_text.tag_configure("body", font=constants.body_text, foreground=constants.text_color, justify="center")

        # Clear any existing text and insert text from challenge_text
        self.page_content_text.delete("1.0", tk.END)
        self.page_content_text.insert(tk.END, self.page_texts[0]["heading"] + "\n", ("heading", "center"))
        self.page_content_text.insert(tk.END, self.page_texts[0]["body"] + "\n", ("body", "center"))
        self.page_content_text.grid(row=0, column=2, sticky="new")

        self.btn_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0)
        self.btn_frame.grid(row=1, column=2, sticky="new", ipadx=0, ipady=0)

        # Label above the button_test with extra vertical padding
        self.btn_frame_label = tk.Label(self.btn_frame, 
                             text="Starta utmaning!", 
                             font=constants.heading, 
                             bg=constants.background_color, 
                             fg=constants.text_color,
                             anchor="center")
        self.btn_frame_label.pack(pady=(0,30))  # Adds 10 pixels of space below the label

        self.btn_container = tk.Frame(self.btn_frame, bg=constants.background_color)
        self.btn_container.pack(side="left")

        # Create challenge buttons
        self.create_button(self.btn_container, "Lätt")
        self.create_button(self.btn_container, "Medel")
        self.create_button(self.btn_container, "Svår")

        # Create frame to display results
        self.result_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0)
        self.result_frame.grid(row=2, column=2, sticky="new", ipadx=0, ipady=0)
        self.result_canvas = tk.Canvas(self.result_frame, bg=constants.background_color, height=4, width=50, highlightthickness=0)
        self.result_text_variable = tk.StringVar()
        self.result_text_variable.set("")
        self.result_label = tk.Label(self.result_frame, 
                                textvariable=self.result_text_variable, 
                                font=constants.heading, 
                                bg=constants.background_color, 
                                fg=constants.text_color)
        self.result_label.pack(side="bottom")

        # Go back frame
        back_btn_frame = tk.Frame(self, 
                                  bg=constants.background_color, 
                                  highlightthickness=0, 
                                  borderwidth=0)
        back_btn_frame.grid(row=3, column=0, sticky="w")

        # Lower-left corner button to go back
        self.back_button = button.RoundedButton(
                                master = back_btn_frame, 
                                text="Bakåt", 
                                radius=20, 
                                width=200, 
                                height=70, 
                                btnbackground=constants.text_color, 
                                btnforeground=constants.background_color, 
                                clicked=lambda: self.back()
        )
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

        # Joystick area
        joystick_frame = tk.Frame(self, bg=constants.background_color)
        joystick_frame.grid(row=3, column=2, sticky="new", pady=(0, 10))

        # Create a canvas for the joystick
        joystick_size = 300
        self.joystick_center = joystick_size // 2
        self.joystick_canvas = tk.Canvas(joystick_frame, width=joystick_size, height=joystick_size, bg=constants.background_color, highlightthickness=0)
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
        self.maxnormal = 0.15

        # Draw the joystick handle
        self.handle_radius = 50
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

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.challenge_isRunning = False
        self.challenge_isFinished = False

        self.delay = 1
        self.update_camera()

    def create_button(self, btn_frame, text):
        # Canvas for circular button_test, based on calculated button_test diameter
        self.btn_canvas = tk.Canvas(btn_frame, 
                           width=self.button_diameter, 
                           height=self.button_diameter, 
                           highlightthickness=0, 
                           bg=constants.background_color)
        self.btn_canvas.pack(side="left", padx=90)

        # Draw circular button_test shape with calculated diameter
        button_circle = self.btn_canvas.create_oval(
            0, 0, self.button_diameter, self.button_diameter, fill="#B9D9EB"
        )

        text_id = self.btn_canvas.create_text(self.button_diameter/2, self.button_diameter/2, 
                                                    text=text, tags="button", fill=constants.background_color,
                                                    font=(constants.heading, 25), justify="center")

        # Button action using a lambda
        self.btn_canvas.bind("<Button-1>", lambda e: self.on_button_click(text))

    def on_button_click(self, nivå):
        # Define the action for the button_test click
        self.result_text_variable.set("Tävlingen startar!\nRoboten börjar!")
        self.isJoystick = False
        self.joystick_control_queue.put_nowait(False)
        time.sleep(1)

        self.challenge = Challenges(self.frame_height, self.frame_width, self.goal_pos_queue)
        self.challenge.start_challenge(nivå)
        self.start_time = time.time()
        self.challenge_isRunning = True

    def update_camera(self):
        if self.send_frames.value and not self.thread_started:
            self.start_thread()
            self.thread_started = True
        
        elif self.send_frames.value and self.thread_started:
            if self.current_frame is not None:
                if self.challenge_isRunning:
                    x, y, _ = self.current_coords
                    robotIsFinished, self.challenge_isFinished, current_time = self.challenge.compete(self.current_frame, x, y)
                    if self.challenge_isFinished:
                        self.user_time = current_time - self.start_time
                        self.goal_pos_queue.put((0, 0), timeout=0.01)
                        self.result_label.config(font=constants.body_text)
                        self.result_text_variable.set("Du klarade det!\n Robotens tid var " + str(round(self.robot_time,2)) + " sekunder\nDin tid var " + str(round(self.user_time, 2)) + " sekunder")

                        self.challenge_isRunning = False
                        self.challenge_isFinished = False
                        self.isJoystick = False
                    elif robotIsFinished:
                        self.robot_time = current_time - self.start_time

                        self.result_label.config(font=constants.heading)
                        #for i in range(3):
                        #    self.result_text_variable.set(f"Din tur!\n {str(3-i)}")
                        #    time.sleep(1)
                        #    print("Hi")
                        time.sleep(1.5)
                        self.result_text_variable.set("Din tur!\n Kör!")
                        
                        self.isJoystick = True
                        self.start_time = time.time()

                # Resize and display frame
                flipped_frame = cv.flip(self.current_frame,-1)
                resized_frame = cv.resize(flipped_frame, (self.cam_height, self.cam_width))
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(resized_frame))
                self.cam_frame.config(image=self.photo) #
                self.cam_frame.image = self.photo #
            else:
                print("no frame")

        self.after(self.delay, self.update_camera)

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

        if self.isJoystick:
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

        if self.isJoystick:
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

    def start_thread(self):
        """Start a separate thread to fetch frames from the queue."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.fetch)
        self.thread.start()

    def join_threads(self):
        """Join the frame fetching thread."""
        self.stop_event.set()
        if hasattr(self, 'thread') and self.frame_thread.is_alive():
            self.thread.join()
            self.thread_started = False

    def fetch(self):
        """Fetch frames from the queue in a separate thread."""
        while not self.stop_event.is_set():
            try:
                if not self.gui_frame_queue.empty():
                    self.current_frame = self.gui_frame_queue.get_nowait()
                if not self.ball_coords_queue.empty():
                    self.current_coords = self.ball_coords_queue.get_nowait()
            except Exception as e:
                pass

    def back(self):
        while not self.goal_pos_queue.empty():
            self.goal_pos_queue.get_nowait()
        self.goal_pos_queue.put((0, 0), timeout=0.01)
        self.joystick_control_queue.put_nowait(False)
        
        # Remove result text
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.result_canvas = tk.Canvas(self.result_frame, bg=constants.background_color, height=2, width=35, highlightthickness=0)
        # End challenge
        self.challenge_isRunning = False
        self.challenge_isFinished = False
        # Kill thread
        self.join_threads()
        self.send_frames.value = False
        # Show previous page
        self.controller.show_frame("Competition_page")