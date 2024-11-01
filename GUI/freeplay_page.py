import tkinter as tk
import constants


class Freeplay_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)


        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Home button
        button = tk.Button(self, text="Back to Home Page",
                           command=lambda: controller.show_frame("Home_page"))
        button.pack()
        
        # Frame to hold text, centered
        text_frame = tk.Frame(self, bg=constants.background_color)
        text_frame.pack(anchor="center", expand=True)

        # Adding text to the text frame
        text_label = tk.Label(text_frame, text="Välkommen till balanssidan!", font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        text_label.pack(pady=10)  # Adjust the padding as needed

        # Optionally, you can add more text or other widgets to the text_frame here
        additional_text = tk.Label(text_frame, text="Här kan du testa balansera roboten själv,", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)
        additional_text = tk.Label(text_frame, text="använd spakarna för att röra roboten i rätt riktning.", 
                                    font=constants.heading, bg=constants.background_color, fg=constants.text_color)
        additional_text.pack(pady=5)

             
