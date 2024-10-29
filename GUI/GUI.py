import tkinter as tk
from home_page import Home_page
from info_page import Info_page
from competition_page import Competition_page
from pattern_page import Pattern_page

# Main Application Class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page Application")
        
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
        for Page in (Home_page, Info_page, Pattern_page, Competition_page):
            page_name = Page.__name__
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
