import tkinter as tk
import constants
import button

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)
        self.page_texts = constants.challenge_text

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Left padding
        self.grid_columnconfigure(1, weight=1) 


        vid_frame = tk.Frame(self, bg=constants.background_color)
        vid_frame.grid(row=1, rowspan=2, column=0, sticky="s", ipadx=100, ipady=100)  # Place below text widget in grid
        canvas = tk.Canvas(vid_frame, width=640, height=480, highlightthickness=1, bg=constants.background_color)
        canvas.pack()


        # Text widget for page content with tagged fonts
        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=constants.body_text,  # Default font for body text
            bg=constants.background_color, 
            fg=constants.text_color,  # Default text color
            relief="flat", 
            height=20, 
            width=75, 
            highlightthickness=0,
        )

        # Configure text tags for heading and body text styles. Add it to column 1
        self.page_content_text.tag_configure("heading", font=constants.heading, foreground=constants.text_color)
        self.page_content_text.tag_configure("body", font=constants.body_text, foreground=constants.text_color)
        self.page_content_text.grid(row=1, column=1)

        # Clear any existing text and insert text from challenge_text
        self.page_content_text.delete("1.0", tk.END)
        self.page_content_text.insert(tk.END, self.page_texts[0]["heading"] + "\n", ("heading", "center"))
        self.page_content_text.grid(sticky="ne")

        # Go back framne
        back_btn_frame = tk.Frame(self, 
                                  bg=constants.background_color, 
                                  highlightthickness=0, 
                                  borderwidth=0)
        back_btn_frame.grid(row=2, column=0, sticky="sw")

        self.create_circular_button(self, "Next", self.on_button_click)

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
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")


    def create_circular_button(self, frame, text, command):
        # Diameter of the button
        button_diameter = 100

        # Frame for each button and its label
        btn_container = tk.Frame(frame, bg=constants.background_color)
        btn_container.grid(row=2, column=1, sticky="e")  # Place below text widget in grid

        # Label above the button with extra vertical padding
        btn_label = tk.Label(btn_container, 
                             text="Starta här!", 
                             font=constants.heading, 
                             bg=constants.background_color, 
                             fg=constants.text_color)
        btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

        # Canvas for circular button, based on calculated button diameter
        canvas = tk.Canvas(btn_container, 
                           width=600+button_diameter, 
                           height=200+button_diameter, 
                           highlightthickness=0, 
                           bg=constants.background_color)
        canvas.pack(side="top")

        # Draw circular button shape with calculated diameter
        button_circle = canvas.create_oval(
            250, 0, 350+button_diameter, 100+button_diameter, fill="#B9D9EB"
        )

        # Button action using a lambda
        canvas.bind("<Button-1>", lambda e: command())

    def on_button_click(self):
        # Define the action for the button click
        print()

    