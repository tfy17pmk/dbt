import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from webcamera_test import Camera
import constants
from class_challenges import Challenges

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)
        self.page_texts = constants.challenge_text
        self.camera = Camera()
            
        frame = self.camera.get_frame()
        frame = self.camera.crop_frame(frame)

        self.cam_width = frame.shape[0]
        self.cam_height = frame.shape[1]

        # Frame for the video feed
        self.cam_frame = tk.Frame(self, bg=constants.background_color)
        self.cam_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="w", padx=50, pady=50)  # Place below text widget in grid
        self.cam_canvas = tk.Canvas(self.cam_frame, width=self.cam_width*2, height=self.cam_height*2, highlightthickness=1, bg=constants_test.background_color)
        self.cam_canvas.pack()

        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=constants.body_text,
            bg=constants.background_color, 
            fg=constants.text_color,
            relief="flat", 
            height=20, 
            width=75, 
            highlightthickness=0,
        )

        # Configure text tags for heading and body text styles. Add it to column 1
        self.page_content_text.tag_configure("heading", font=constants.heading, foreground=constants_test.text_color)
        self.page_content_text.tag_configure("body", font=constants.body_text, foreground=constants_test.text_color)

        # Clear any existing text and insert text from challenge_text
        self.page_content_text.delete("1.0", tk.END)
        self.page_content_text.insert(tk.END, self.page_texts[0]["heading"] + "\n", ("heading", "center"))
        self.page_content_text.insert(tk.END, self.page_texts[0]["body"] + "\n", ("body", "center"))
        self.page_content_text.grid(row=0, column=2, sticky="ne")

        self.create_circular_button(self, "Next", self.on_button_click, 100, 2, 2)
        
        self.result_frame = tk.Frame(self, bg=constants.background_color)
        self.result_frame.grid(row=1, column=2, sticky="nsew")
        T = tk.Text(self.result_frame, height = 5, width = 52)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        self.challenge_isRunning = False
        self.challenge_isFinished = False

        self.delay = 1
        self.update_camera()

    def create_circular_button(self, frame, text, command, diameter, row, column):
        # Frame for each button_test and its label
        btn_frame = tk.Frame(frame, bg=constants.background_color)
        btn_frame.grid(row=row, column=column, sticky="nsew", ipadx=10, ipady=10)  # Place below text widget in grid

        # Label above the button_test with extra vertical padding
        btn_label = tk.Label(btn_frame, 
                             text=text, 
                             font=constants.heading, 
                             bg=constants.background_color, 
                             fg=constants.text_color)
        btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label


        # Canvas for circular button_test, based on calculated button_test diameter
        canvas = tk.Canvas(btn_frame, 
                           width=diameter, 
                           height=diameter, 
                           highlightthickness=1, 
                           bg=constants.background_color)
        canvas.pack(side="left")

        # Draw circular button_test shape with calculated diameter
        button_circle = canvas.create_oval(
            0, 0, diameter, diameter, fill="#B9D9EB"
        )

        # Button action using a lambda
        canvas.bind("<Button-1>", lambda e: command())

    def on_button_click(self):
        # Define the action for the button_test click
        print('Utmaning startad!')
        self.challenge = Challenges()
        self.challenge.start_challenge()
        self.challenge_isRunning = True

    def update_camera(self):
        frame = self.camera.get_frame()
        frame = self.camera.crop_frame(frame)
        if frame is not None:
            if self.challenge_isRunning:
                x, y, area = self.camera.get_ball(frame)
                self.challenge_isFinished, result_time = self.challenge.create_dots(frame, x, y)
                if self.challenge_isFinished:
                    btn_label = tk.Label(self.result_frame, 
                             text="Du klarade det!\nDin tid var " + str(result_time) + " sekunder", 
                             font=constants.body_text, 
                             bg=constants.background_color, 
                             fg=constants.text_color)
                    btn_label.pack(side="bottom")

                    self.challenge_isRunning = False
                    self.challenge_isFinished = False
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            resized_frame = cv.resize(frame, (self.cam_height*2, self.cam_width*2))
            photo = ImageTk.PhotoImage(image = Image.fromarray(resized_frame))
            self.cam_canvas.create_image(0, 0, image = photo, anchor = tk.NW)

            label = tk.Label(image=photo)
            label.image = photo # keep a reference!
        else:
            print("no frame")

        self.after(self.delay, self.update_camera)

    def __del__(self):
        if self.camera.cam.isOpened():
            self.camera.cam.release()

    