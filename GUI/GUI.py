import tkinter as tk
from .home_page import Home_page
from .info_page import Info_page
from .competition_page import Competition_page
from .pattern_page import Pattern_page
from .freeplay_page import Freeplay_page
from .challenge_page import Challenge_page

# Main Application Class
class App(tk.Tk):
    def __init__(self, update_send_frames_to_gui_callback, gui_frame_queue):
        super().__init__()
        self.title("BallBot")
        self.update_send_frames_to_gui_callback = update_send_frames_to_gui_callback
        self.gui_frame_queue = gui_frame_queue

        # Start in full-screen mode
        self.attributes("-fullscreen", True)

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        # Make the container resizable and center its content
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold the pages
        self.frames = {}

        # Initialize each page
        for Page in (Home_page, Info_page, Pattern_page, Competition_page, Challenge_page, Freeplay_page):
            page_name = Page.__name__
            
            if Page is Info_page:
                frame = Page(parent=container, controller=self, update_send_frames_to_gui_callback=self.update_send_frames_to_gui_callback, gui_frame_queue=self.gui_frame_queue)
            else:
                frame = Page(parent=container, controller=self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page
        self.show_frame("Home_page")

    # Method to show a frame for the given page name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
