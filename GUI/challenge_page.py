import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
import GUI.button as button
import GUI.constants as constants
from GUI.class_challenges import Challenges
from math import atan2, cos, sin, sqrt
from multiprocessing import Lock
import threading

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller, send_frames, gui_frame_queue, ball_coords_queue):
        super().__init__(parent)
        self.controller = controller
        self.gui_frame_queue = gui_frame_queue #
        self.ball_coords_queue = ball_coords_queue #
        self.send_frames = send_frames
        self.stop_event = threading.Event() #
        self.thread_started = False

        self.configure(bg=constants.background_color)
        self.page_texts = constants.challenge_text
        self.button_diameter = 200
            
        # Output frame size
        self.current_frame = None
        self.frame_height, self.frame_width = 285, 320
        self.cam_width = self.frame_width*3
        self.cam_height = self.frame_height*3

        # Frame for the video feed
        self.cam_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0)
        self.cam_frame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="new", padx=(50,0), pady=(50,0))  # Place below text widget in grid
        self.cam_canvas = tk.Canvas(self.cam_frame, width=self.cam_width, height=self.cam_height, highlightthickness=0, bg=constants.background_color)
        self.cam_canvas.pack()

        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=constants.body_text,
            bg=constants.background_color, 
            fg=constants.text_color,
            relief="flat", 
            height=8, 
            width=40, 
            highlightthickness=0,
            padx=0,
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
        self.btn_frame.grid(row=1, column=2, sticky="new", ipadx=0, ipady=50)

        # Label above the button_test with extra vertical padding
        self.btn_frame_label = tk.Label(self.btn_frame, 
                             text="Starta utmaning!", 
                             font=constants.heading, 
                             bg=constants.background_color, 
                             fg=constants.text_color,
                             anchor="center")
        self.btn_frame_label.pack()  # Adds 10 pixels of space below the label

        self.btn_container = tk.Frame(self.btn_frame, bg=constants.background_color)
        self.btn_container.pack(side="left")

        self.create_button(self.btn_container, "Lätt")
        self.create_button(self.btn_container, "Medel")
        self.create_button(self.btn_container, "Svår")

        self.result_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0)
        self.result_frame.grid(row=2, column=2, sticky="new", ipadx=0, ipady=0)
        self.result_canvas = tk.Canvas(self.result_frame, bg=constants.background_color, height=2, width=50, highlightthickness=0)

        # Go back frame
        back_btn_frame = tk.Frame(self, 
                                  bg=constants.background_color, 
                                  highlightthickness=0, 
                                  borderwidth=0)
        back_btn_frame.grid(row=3, column=0, sticky="sw")

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
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

        # Joystick area
        joystick_frame = tk.Frame(self, bg=constants.background_color)
        joystick_frame.grid(row=3, column=2, sticky="nesw", pady=(0, 10))

        # Create a canvas for the joystick
        joystick_size = 150
        self.joystick_center = joystick_size // 2
        self.joystick_canvas = tk.Canvas(joystick_frame, width=joystick_size, height=joystick_size, bg=constants.background_color, highlightthickness=0)
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
        self.btn_canvas.pack(side="left", padx=50)

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
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        self.result_canvas = tk.Canvas(self.result_frame, bg=constants.background_color, height=2, width=35, highlightthickness=0)
        self.challenge = Challenges(self.frame_height, self.frame_width)
        self.challenge.start_challenge(nivå)
        self.challenge_isRunning = True

    def update_camera(self):
        if self.send_frames.value and not self.thread_started:
            self.start_thread()
            self.thread_started = True
        
        elif self.send_frames.value and self.thread_started:
            if self.current_frame is not None:
                if self.challenge_isRunning:
                    x, y, _ = self.current_coords
                    self.challenge_isFinished, result_time = self.challenge.create_dots(self.current_frame, x, y)
                    if self.challenge_isFinished:
                        btn_label = tk.Label(self.result_frame, 
                                text="Du klarade det!\nDin tid var " + str(round(result_time, 2)) + " sekunder", 
                                font=constants.body_text, 
                                bg=constants.background_color, 
                                fg=constants.text_color)
                        btn_label.pack(side="bottom")

                        self.challenge_isRunning = False
                        self.challenge_isFinished = False

                self.current_frame = cv.cvtColor(self.current_frame, cv.COLOR_BGR2RGB)
                resized_frame = cv.resize(self.current_frame, (self.cam_height, self.cam_width))
                photo = ImageTk.PhotoImage(image = Image.fromarray(resized_frame))
                self.cam_canvas.create_image(0, 0, image = photo, anchor = tk.NW)

                label = tk.Label(image=photo)
                label.image = photo # keep a reference!
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

        # Print the joystick's position relative to the center
        print(f"Joystick position: x={dx:.2f}, y={dy:.2f}")

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

    def start_thread(self):
        """Start a separate thread to fetch frames from the queue."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.fetch)
        self.thread.start()

    def join_threads(self):
        """Join the frame fetching thread."""
        self.stop_event.set()
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
        self.join_threads()
        self.send_frames.value = False
        self.controller.show_frame("Competition_page")