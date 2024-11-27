from tkinter import *
import tkinter as tk
from .home_page import Home_page
from .info_page import Info_page
from .competition_page import Competition_page
from .pattern_page import Pattern_page
from .freeplay_page import Freeplay_page
from .challenge_page import Challenge_page


# Main Application Class
class App(tk.Tk):
    """Initialize the application."""
    def __init__(self, resources):
        super().__init__()
        self.title("BallBot")
        self.resources = resources

        # Replace this shared resources with the resources from main.py
        self.send_frames_to_challenge = resources.send_frames_to_challenge
        self.gui_challange_frame_queue = resources.gui_challange_frame_queue
        self.ball_coords_queue = resources.ball_coords_queue
        self.goal_pos_queue = resources.goal_position_queue
        self.joystick_control_queue = resources.joystick_control_queue
        #--------------------------------------------------------------

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
        for Page in (Home_page, Info_page, Pattern_page, Challenge_page, Competition_page, Freeplay_page):
            page_name = Page.__name__
            
            if Page is Info_page:
                frame = Page(parent=container, controller=self, resources=self.resources)
            elif Page is Challenge_page:
                frame = Page(parent=container, controller=self, send_frames=self.send_frames_to_challenge, gui_frame_queue=self.gui_challange_frame_queue, ball_coords_queue=self.ball_coords_queue, goal_pos_queue=self.goal_pos_queue, joystick_control_queue=self.joystick_control_queue)
            elif Page is Pattern_page:
                frame = Page(parent=container, controller=self, goal_pos_queue=self.goal_pos_queue)
            elif Page is Freeplay_page:
                frame = Page(parent=container, controller=self, joystick_control_queue=self.joystick_control_queue)
            else:
                frame = Page(parent=container, controller=self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page
        self.show_frame("Home_page")


    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]

        #if page_name == "Challenge_page":
            #self.resources.send_frames_to_challenge.value = True

        frame.tkraise()

    def join_threads(self):
        """Join all threads in the frames."""
        for frame in self.frames.values():
            if hasattr(frame, 'join_threads'):
                frame.join_threads()

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()
