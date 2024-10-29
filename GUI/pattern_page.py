import tkinter as tk

# Page 3: Page Two
class Pattern_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is the pattern page")
        label.pack(pady=10)
        
        button = tk.Button(self, text="Back to Home Page",
                           command=lambda: controller.show_frame("Home_page"))
        button.pack()
