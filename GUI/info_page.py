import tkinter as tk

# Page 2: Page One
class Info_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is the info page")
        label.pack(pady=10)
        
        button = tk.Button(self, text="Back to the home Page",
                           command=lambda: controller.show_frame("Home_page"))
        button.pack()