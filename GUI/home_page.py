import tkinter as tk

# Page 1: Home Page
class Home_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Centered label at the top
        label = tk.Label(self, text="This is the Home Page", font=("Arial", 16))
        label.pack(pady=20)

        # Frame to hold buttons in a single row, centered
        button_frame = tk.Frame(self)
        button_frame.pack(expand=True)  # Center button frame in the middle of the Home_page frame

        # Buttons in a row, centered within button_frame
        button1 = tk.Button(button_frame, text="Go to the Info Page",
                            command=lambda: controller.show_frame("Info_page"))
        button1.pack(side="left", padx=10)

        button2 = tk.Button(button_frame, text="Go to the Competition Page",
                            command=lambda: controller.show_frame("Competition_page"))
        button2.pack(side="left", padx=10)

        button3 = tk.Button(button_frame, text="Go to the Pattern Page",
                            command=lambda: controller.show_frame("Pattern_page"))
        button3.pack(side="left", padx=10)

        # Use expand and fill options to center the entire Home_page frame
        self.pack(expand=True, fill="both")

