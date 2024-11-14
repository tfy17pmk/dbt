import tkinter as tk
import GUI.constants
import GUI.button


class Freeplay_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.constants = GUI.constants
        self.button = GUI.button
        self.configure(bg=self.constants.background_color)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Setup grid pattern with equal weight for each row and column
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=1)
        
        # Frame to hold text, centered
        text_frame = tk.Frame(self, 
                              bg=self.constants.background_color, 
                              highlightthickness=0, 
                              height=screen_height*0.3, 
                              width=screen_width*0.75)
        text_frame.grid(row=1, column=1, rowspan=1, columnspan=1, pady=300, sticky="nsew")

        # Adding text to the text frame
        text_label = tk.Label(text_frame, 
                              text="Välkommen till balanssidan!", 
                              font=self.constants.heading, 
                              bg=self.constants.background_color, 
                              fg=self.constants.text_color)
        text_label.grid(row=0, column=0, sticky="nsew")

        additional_text = tk.Label(text_frame, 
                                   text="Här kan du testa balansera bollen själv,\nanvänd spakarna för att röra roboten i rätt riktning.", 
                                    font=self.constants.heading, 
                                    bg=self.constants.background_color, 
                                    fg=self.constants.text_color)
        additional_text.grid(row=1, column=0, sticky="nsew")


        # Go back framne
        back_btn_frame = tk.Frame(self, 
                                  bg=self.constants.background_color, 
                                  highlightthickness=0, 
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
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

             
