from tkinter import *
import tkinter as tk
from .home_page import Home_page
from .info_page import Info_page
from .pattern_page import Pattern_page
from .freeplay_page import Freeplay_page
from .idle_pattern import IdlePatterns
from . import constants

# Main Application Class
class App(tk.Tk):
    """Main application class for BallBot GUI."""

    def __init__(self, resources):
        """Initialize the application."""
        super().__init__()
        self.title("BallBot")
        self.resources = resources
        self.set_language = "sv"
        self.pattern = True # True = run pattern when idle
        self.time_before_idle = 1800000
        self.IdlePattern = IdlePatterns(self.resources)
        self.translations = constants.translation

        #  Reset timer when there is any action on the touch screen
        self.bind_all("<Motion>", self.reset_timer)

        # Replace this shared resources with the resources from main.py
        self.ball_coords_queue = resources.ball_coords_queue
        self.goal_pos_queue = resources.goal_position_queue
        self.joystick_control_queue = resources.joystick_control_queue

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
        for Page in (Home_page, Info_page, Pattern_page, Freeplay_page):
            page_name = Page.__name__
            
            if Page is Info_page:
                frame = Page(parent=container, controller=self, resources=self.resources)
            elif Page is Pattern_page:
                frame = Page(parent=container, controller=self, goal_pos_queue=self.goal_pos_queue)
            elif Page is Freeplay_page:
                frame = Page(parent=container, controller=self, resources=self.resources)
            else:
                frame = Page(parent=container, controller=self)

            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page
        self.show_home_page()

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]

        if page_name in ["Home_page", "Info_page"]:
            if self.pattern:  # Start the pattern if it is enabled
                self.IdlePattern.run_pattern()
        else:
            self.IdlePattern.reset_data()  # Stop the pattern for other pages

        if page_name != "Home_page":
            self.start_timer()

        frame.tkraise()


    def join_threads(self):
        """Join all threads in the frames."""
        for frame in self.frames.values():
            if hasattr(frame, 'join_threads'):
                frame.join_threads()
        self.IdlePattern.reset_data()
        

    def start_timer(self):
        """Start timer for going back to home page due to inactivity."""
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(self.time_before_idle, self.show_home_page)

    def reset_timer(self, event=None):
        """Reset timer for going back to home page if there is activity."""
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        self.start_timer()  

    def show_home_page(self):
        """Show home page and reset language to Swedish."""
        self.set_language = "sv"
        self.update_text()
        for frame in self.frames.values():
            if hasattr(frame, "go_back"):
                frame.go_back()
                  
        if self.pattern:
            self.IdlePattern.run_pattern()
        
    def update_text(self):
        """Update all frames with new text based on the current language."""
        for frame in self.frames.values():
            if hasattr(frame, "update_labels"):
                frame.update_labels(self.translations[self.set_language])



    
