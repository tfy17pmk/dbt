import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from webcamera_test import Camera
import GUI.button
import GUI.constants
from GUI.class_challenges import Challenges

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.button = GUI.button
        self.constants = GUI.constants
        self.configure(bg=self.constants.background_color)
        self.page_texts = self.constants.challenge_text
        self.camera = Camera()
        
            
        # Output frame size
        self.cam_width = 600
        self.cam_height = 600

        # Frame for the video feed
        self.cam_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=1)
        self.cam_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="new", padx=(30,50), pady=(20,0))  # Place below text widget in grid
        self.cam_canvas = tk.Canvas(self.cam_frame, width=self.cam_width, height=self.cam_height, highlightthickness=1, bg=self.constants.background_color)
        self.cam_canvas.pack()

        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=self.constants.body_text,
            bg=self.constants.background_color, 
            fg=self.constants.text_color,
            relief="flat", 
            height=8, 
            width=35, 
            highlightthickness=1,
            padx=10,
            pady=20
        )

        # Configure text tags for heading and body text styles. Add it to column 1
        self.page_content_text.tag_configure("heading", font=self.constants.heading, foreground=self.constants.text_color)
        self.page_content_text.tag_configure("body", font=self.constants.body_text, foreground=self.constants.text_color)

        # Clear any existing text and insert text from challenge_text
        self.page_content_text.delete("1.0", tk.END)
        self.page_content_text.insert(tk.END, self.page_texts[0]["heading"] + "\n", ("heading", "center"))
        self.page_content_text.insert(tk.END, self.page_texts[0]["body"] + "\n", ("body", "center"))
        self.page_content_text.grid(row=0, column=2, sticky="new")

        self.btn_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=1)
        self.btn_frame.grid(row=1, column=2, sticky="new", ipadx=10, ipady=10)

        # Label above the button_test with extra vertical padding
        self.btn_label = tk.Label(self.btn_frame, 
                             text="Starta utmaning!", 
                             font=self.constants.heading, 
                             bg=self.constants.background_color, 
                             fg=self.constants.text_color,
                             anchor="center")
        self.btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

        # Canvas for circular button_test, based on calculated button_test diameter
        self.btn_canvas = tk.Canvas(self.btn_frame, 
                           width=100, 
                           height=100, 
                           highlightthickness=1, 
                           bg=self.constants.background_color)
        self.btn_canvas.pack(side="top")

        # Draw circular button_test shape with calculated diameter
        button_circle = self.btn_canvas.create_oval(
            0, 0, 100, 100, fill="#B9D9EB"
        )

        # Button action using a lambda
        self.btn_canvas.bind("<Button-1>", lambda e: self.on_button_click())

        self.result_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=1)
        self.result_frame.grid(row=2, column=2, sticky="new")
        self.result_canvas = tk.Canvas(self.result_frame, bg=self.constants.background_color, height=2, width=35, highlightthickness=1)

                # Go back frame
        back_btn_frame = tk.Frame(self, 
                                  bg=self.constants.background_color, 
                                  highlightthickness=1, 
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
        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.challenge_isRunning = False
        self.challenge_isFinished = False

        self.delay = 1
        self.update_camera()

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
                             font=self.constants.body_text, 
                             bg=self.constants.background_color, 
                             fg=self.constants.text_color)
                    btn_label.pack(side="bottom")

                    self.challenge_isRunning = False
                    self.challenge_isFinished = False
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            resized_frame = cv.resize(frame, (self.cam_height, self.cam_width))
            photo = ImageTk.PhotoImage(image = Image.fromarray(resized_frame))
            self.cam_canvas.create_image(0, 0, image = photo, anchor = tk.NW)

            label = tk.Label(image=photo)
            label.image = photo # keep a reference!
        else:
            print("no frame")

        self.after(self.delay, self.update_camera)

    # Releases camera, remove when integrating w main
    def __del__(self):
        if self.camera.cam.isOpened():
            self.camera.cam.release()

    