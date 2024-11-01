import tkinter as tk
import constants

class Challenge_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)

        # Screen dimensions
        screen_width = self.winfo_screenwidth()  # 1440
        screen_height = self.winfo_screenheight()  # 900

        # Configure grid layout to center content both vertically and horizontally
        self.grid_rowconfigure(0, weight=1)  # Spacer row at the top
        self.grid_rowconfigure(1, weight=2)  # Main content row
        self.grid_rowconfigure(2, weight=3)  # Dots and buttons row

        self.grid_columnconfigure(0, weight=1)  # Spacer column on the left
        self.grid_columnconfigure(1, weight=2)  # Main content column
        self.grid_columnconfigure(2, weight=9)  # Spacer column on the right

        # Home button
        button = tk.Button(self, text="Back to Home Page",
                           command=lambda: controller.show_frame("Home_page"))
        button.grid(row=0, column=0)  # Place button in the first row

        # Frame to hold right-side text
        text_frame = tk.Frame(self, bg=constants.background_color)
        text_frame.grid(row=0, column=3)  # Place text frame in the second row

        # Adding text
        text_label = tk.Label(text_frame, text="Utmana mig i att balansera bollen!", 
                              font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        text_label.pack(pady=10)  # Adjust the padding as needed

        additional_text = tk.Label(text_frame, text="Jag rullar bollen till olika", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)

        additional_text = tk.Label(text_frame, text="ställen på bordet, sedan får du ", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)

        additional_text = tk.Label(text_frame, text="använd spakarna för att röra", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)

        additional_text = tk.Label(text_frame, text="roboten till samma ställen.", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)

        # BUTTON
        button_diameter = int(screen_width * 0.15)

        # Frame to hold buttons
        button_frame = tk.Frame(self, bg=constants.background_color)
        button_frame.grid(row=2, column=10, sticky="se")  # Place button frame in the third row

        def create_circular_button(frame, text, command):
            btn_label = tk.Label(frame, text=text, font=constants.heading, bg=constants.background_color, fg=constants.text_color)
            btn_label.pack(pady=(0, 10))  # Adds 10 pixels of space below the label

            # Canvas for circular button, based on calculated button diameter
            canvas = tk.Canvas(frame, width=button_diameter, height=button_diameter, highlightthickness=0, bg=constants.background_color)
            canvas.pack()

            # Draw circular button shape with calculated diameter
            button_circle = canvas.create_oval(
                1, 1, button_diameter, button_diameter, fill="#B9D9EB"
            )

            # Button action using a lambda
            canvas.bind("<Button-1>", lambda e: command())

        # Create the circular buttons with labels above
        create_circular_button(button_frame, "Starta här!", lambda: start_challenge())

        def start_challenge():
            print("Utmaning påbörjad!")     

        # VIDEO SQUARE
        vid_frame = tk.Frame(self, bg=constants.background_color)
        vid_frame.grid(row=1, column=0, rowspan=3, sticky="nw", padx=10, pady=10)  # Place video frame to the right

        square_canvas = tk.Canvas(vid_frame, width=800, height=600, bg=constants.background_color)
        square_canvas.pack()