from tkinter import *
import tkinter as tk
from .home_page import Home_page
from .info_page import Info_page
from .competition_page import Competition_page
from .pattern_page import Pattern_page
from .freeplay_page import Freeplay_page
from .challenge_page import Challenge_page
from .patterns import Patterns


# Main Application Class
class App(tk.Tk):
    """Initialize the application."""
    def __init__(self, resources):
        super().__init__()
        self.title("BallBot")
        self.resources = resources

        self.patterns = Patterns()

        #  Reset timer when there is any action on the touch screen
        self.bind_all("<Motion>", self.reset_timer)

        # Replace this shared resources with the resources from main.py
        self.send_frames_to_challenge = resources.send_frames_to_challenge
        self.gui_challange_frame_queue = resources.gui_challange_frame_queue
        self.ball_coords_queue = resources.ball_coords_gui_queue
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
                frame = Page(parent=container, controller=self, resources=self.resources)
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
        self.current_page = page_name

        #if page_name != "Home_page":
        self.start_timer()

        if page_name == "Challenge_page":
            self.resources.send_frames_to_challenge.value = True

        frame.tkraise()

    def join_threads(self):
        """Join all threads in the frames."""
        for frame in self.frames.values():
            if hasattr(frame, 'join_threads'):
                frame.join_threads()

    def start_timer(self):
        """Start timer for going back to home page due to inactivity."""
        # Ensure only one timer is active at a time
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(10000, self.reset_to_idle_state)  # Store the task ID

    def reset_timer(self, event=None):
        """Reset timer for going back to home page if there is activity."""
        if hasattr(self, 'timer_id'):  # Cancel the existing timer
            self.after_cancel(self.timer_id)
        self.start_timer()  # Restart the timer

    def reset_to_idle_state(self):
        """Reset applikation to idle state and let Robot run a specific pattern."""

        # Show Home Page
        if hasattr(self, 'current_page'):
            if self.current_page != "Home_page":
                self.show_frame("Home_page")
        
        # Run pattern



    