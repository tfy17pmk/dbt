import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from webcamera_test import Camera
import button
import constants
from class_challenges import Challenges

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)
        self.page_texts = constants.challenge_text
        self.camera = Camera()
        self.button_diameter = 200
            
        # Output frame size
        frame = self.camera.get_frame()
        frame = self.camera.crop_frame(frame)
        frame_height, frame_width, _ = frame.shape
        self.cam_width = frame_width*3
        self.cam_height = frame_height*3

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
                                clicked=lambda: controller.show_frame("Competition_page")
        )
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

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
        frame = self.camera.get_frame()
        frame = self.camera.crop_frame(frame)
        self.challenge = Challenges(frame)
        self.challenge.start_challenge(nivå)
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
                             text="Du klarade det!\nDin tid var " + str(round(result_time, 2)) + " sekunder", 
                             font=constants.body_text, 
                             bg=constants.background_color, 
                             fg=constants.text_color)
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

    