from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import GUI.constants
import GUI.button
from multiprocessing import Lock
import threading

class Info_page(tk.Frame):
    """Class for the Info page of the GUI."""

    def __init__(self, parent, controller, resources):
        """Initialize the Info page."""
        super().__init__(parent)
        self.controller = controller
        self.current_page = 0
        self.constants = GUI.constants
        self.button = GUI.button

        self.resources = resources
        self.current_frame = None
        self.stop_event = threading.Event()

        self.configure(bg=self.constants.background_color)

        # Frame to hold 'back' button
        button_frame = tk.Frame(self, bg=self.constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0)
        button_frame.grid(row=2, column=1, sticky="sw")

        # Load the arrow icon and create rotated version for left button
        original_arrow = Image.open(self.constants.RIGHT_ARROW).resize((40, 40))
        self.right_arrow_icon = ImageTk.PhotoImage(original_arrow)
        self.left_arrow_icon = ImageTk.PhotoImage(original_arrow.rotate(180))
        
        first_page = Image.open(self.constants.FIRSTPAGE).resize((400, 720))
        self.first_page = ImageTk.PhotoImage(first_page)
        
        arm_image_original = Image.open(self.constants.ARM).resize((750, 500))
        self.arm_image_icon = ImageTk.PhotoImage(arm_image_original)

        brain_image_original = Image.open(self.constants.BRAIN).resize((250, 250))
        self.brain_image_icon = ImageTk.PhotoImage(brain_image_original)
        
        # Placeholder for each page's unique text and actions
        self.page_texts = self.constants.translation["sv"]["text_info"]

        # Configure grid layout to center content
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=9)
        self.grid_columnconfigure(2, weight=0)

        # Prevents dynamic resizing when widgets are shown/hidden
        self.grid_propagate(False)
        
        # Dots canvas for page indicators
        self.dots = tk.Canvas(self, height=40, bg=self.constants.background_color, highlightthickness=0)
        self.dots.grid(row=2, column=1, pady=10, padx=(420,0), sticky="n")
        
        # Create canvases for navigation buttons
        self.btn_prev_canvas = tk.Canvas(self, width=80, height=80, bg=self.constants.background_color, highlightthickness=0)
        self.btn_prev_canvas.grid(row=2, column=1, sticky="nw", padx=(730,0), pady=0)
        
        self.btn_next_canvas = tk.Canvas(self, width=80, height=80, bg=self.constants.background_color, highlightthickness=0)
        self.btn_next_canvas.grid(row=2, column=1, sticky="ne", padx=(0,320), pady=0)

        # Draw circular buttons with arrow icons, and store IDs 
        self.left_arrow_id = self.create_circle_button(self.btn_prev_canvas, 40, 40, 30, self.left_arrow_icon, self.prev_page)
        self.right_arrow_id = self.create_circle_button(self.btn_next_canvas, 40, 40, 30, self.right_arrow_icon, self.next_page)

        # Text widget for page content with tagged fonts
        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=self.constants.body_text,  # Default font
            bg=self.constants.background_color, 
            relief="flat", 
            height=70, 
            width=70, 
            highlightthickness=0,
            pady=0,
            padx=100
        )
        
        self.page_content_text.grid(row=0, column=1, padx=(200,0), pady=(75,0), sticky="n")
        self.page_content_text.tag_configure("heading", font=self.constants.heading, foreground=self.constants.text_color, spacing3=0)
        self.page_content_text.tag_configure("subheading", font=self.constants.sub_heading, foreground=self.constants.text_color)
        self.page_content_text.tag_configure("body", font=self.constants.body_text, foreground=self.constants.text_color)
        self.page_content_text.tag_configure("lightButtonText", font=self.constants.sub_heading, foreground=self.constants.text_color)
        self.page_content_text.config(state="disabled")

        # Disable selection bindings
        self.page_content_text.bind("<Button-1>", lambda e: "break")     # Disable left-click selection
        self.page_content_text.bind("<B1-Motion>", lambda e: "break")    # Disable mouse drag selection
        self.page_content_text.bind("<Shift-Left>", lambda e: "break")   # Disable Shift+Left selection
        self.page_content_text.bind("<Shift-Right>", lambda e: "break")  # Disable Shift+Right selection
        self.page_content_text.bind("<Shift-Up>", lambda e: "break")     # Disable Shift+Up selection
        self.page_content_text.bind("<Shift-Down>", lambda e: "break")   # Disable Shift+Down selection
        self.page_content_text.bind("<Control-a>", lambda e: "break")    # Disable Ctrl+A selection (Select All)

        # Define a custom style for the rounded button
        style = ttk.Style()
        style.configure("RoundedButton.TButton", 
                        foreground=self.constants.text_color,
                        background=self.constants.background_color,
                        borderwidth=0, 
                        focuscolor=style.configure(".")["background"])
        
        style.map("RoundedButton.TButton",
                  background=[("active", self.constants.background_color)])

        # Lower-left corner button to go back
        self.back_button = self.button.RoundedButton(
            master = button_frame, 
            text=self.constants.translation[self.controller.set_language]["back"], 
            radius=25, 
            width=200, 
            height=70, 
            btnbackground=self.constants.text_color, 
            btnforeground=self.constants.background_color, 
            clicked=self.go_back
        )
        self.back_button.grid(row=1, column=0, padx=(0,200), pady=10, sticky="n")

        # Canvas to display images on relevant pages
        self.image_canvas = tk.Canvas(self, width=500, height=1000, bg=self.constants.background_color, highlightthickness=0)
        self.image_canvas.grid(row=0, column=2, pady=(50,0), sticky="n")
        self.image_canvas.grid_remove()  # Initially hidden

        # Display the first page initially
        self.show_page(0)
        self.update_dots()
        # Fix for initial rendering of dots
        self.after(100, self.update_dots)

    def create_circle_button(self, canvas, x, y, radius, icon, command):
        """Draw a circular button with an icon inside it on the canvas and bind it to a command."""
        circle_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.constants.text_color, outline="")
        image_id = canvas.create_image(x, y, image=icon)
        
        # Bind click events to both the circle and image
        canvas.tag_bind(circle_id, "<Button-1>", lambda event: command())
        canvas.tag_bind(image_id, "<Button-1>", lambda event: command())
        
        return circle_id, image_id

    def show_page(self, page_index):
        """Show page at given index by updating content text, dynamic button, and arrow visibility."""
        self.current_page = page_index

        # Adjust the width of the Text widget for the second page
        if page_index == 1:
            self.page_content_text.config(width=70)  # Set to a smaller width on the second page
        else:
            self.page_content_text.config(width=70)  # Default width for other pages

        # Clear and update the Text widget for the current page
        self.page_content_text.config(state="normal")
        self.page_content_text.delete("1.0", tk.END)

        # Insert heading, subheading, and body with respective tags
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["heading"] + "\n", "heading")
        self.page_content_text.insert(tk.END, self.page_texts[page_index].get("subheading", "") + "\n", "subheading")
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["body"], "body")
        self.page_content_text.config(state="disabled")

        # Show or hide the appropriate image based on the current page
        self.image_canvas.delete("all")  # Clear any existing image first
        self.image_canvas.config(bg=self.constants.background_color)  # Ensure the background color remains consistent

        # Display the correct image and handle camera frame for each page
        
        if page_index == 0:
            self.image_canvas.grid()  # Make sure the image canvas is visible
            self.image_canvas.create_image(195, 480, image=self.first_page)
            self.image_canvas.grid()

        if page_index == 1:
            self.resources.send_frames_to_gui.value = True # Set flag for backend to send frames to GUI
            self.image_canvas.grid()  # Make sure the image canvas is visible

            # Create and display camera_frame below the image, only on the second page
            if not hasattr(self, "camera_frame"):
                self.camera_frame = tk.Label(self)
            self.camera_frame.grid(row=0, column=2, padx=(0,100), sticky="")
            self.start_frame_thread()  # Start the frame fetching thread
        else:
            self.resources.send_frames_to_gui.value = False # Set flag to stop sending frames to GUI
            self.current_frame = None  # Clear the current frame

            # Hide camera_frame on pages other than the second
            if hasattr(self, "camera_frame"):
                self.camera_frame.grid_remove()

            # Show the ARM image for the third page
            if page_index == 2:
                self.image_canvas.create_image(195, 280, image=self.arm_image_icon)
                self.image_canvas.grid()

            # Show the BRAIN image for the last page
            elif page_index == len(self.page_texts) - 1:
                self.image_canvas.create_image(200, 300, image=self.brain_image_icon)
                self.image_canvas.grid()

        # Update arrow visibility based on the current page
        self.update_arrow_visibility()

        # Update the dots to show the current page
        self.update_dots()

    def start_frame_thread(self):
        """Start a separate thread to fetch frames from the queue."""
        self.stop_event.clear()
        if not hasattr(self, 'frame_thread'):
            self.frame_thread = threading.Thread(target=self.fetch_frames)
            self.frame_thread.start()

    def join_threads(self):
        """Join the frame fetching thread."""
        self.stop_event.set()
        if hasattr(self, 'frame_thread') and self.frame_thread.is_alive():
            self.frame_thread.join()

    def fetch_frames(self):
        """Fetch frames from the queue in a separate thread."""
        while not self.stop_event.is_set():
            try:
                if not self.resources.gui_frame_queue.empty():
                    frame = self.resources.gui_frame_queue.get_nowait()
                    self.current_frame = ImageTk.PhotoImage(Image.fromarray(frame))

                    # Update the camera_frame with the latest frame directly
                    self.camera_frame.config(image=self.current_frame)
                    self.camera_frame.image = self.current_frame
            except Exception as e:
                pass

    def update_arrow_visibility(self):
        """Hide left arrow on the first page and right arrow on the last page."""
        if self.current_page == 0:
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[0], state="hidden")
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[1], state="hidden")
        else:
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[0], state="normal")
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[1], state="normal")

        if self.current_page == len(self.page_texts) - 1:
            self.btn_next_canvas.itemconfigure(self.right_arrow_id[0], state="hidden")
            self.btn_next_canvas.itemconfigure(self.right_arrow_id[1], state="hidden")
        else:
            self.btn_next_canvas.itemconfigure(self.right_arrow_id[0], state="normal")
            self.btn_next_canvas.itemconfigure(self.right_arrow_id[1], state="normal")

    def update_dots(self):
        """Update the dots to show current page and make them clickable."""
        self.dots.delete("all")
        dot_radius = 5
        dot_spacing = 20
        center_x = (self.dots.winfo_width() / 2) - (len(self.page_texts) * dot_spacing / 2)
        
        for i in range(len(self.page_texts)):
            x = center_x + i * dot_spacing
            color = self.constants.text_color if i == self.current_page else self.constants.background_color
            dot = self.dots.create_oval(x, 10, x + 2 * dot_radius, 10 + 2 * dot_radius, fill=color, outline=self.constants.text_color)
            self.dots.tag_bind(dot, "<Button-1>", lambda event, index=i: self.show_page(index))
        # Force the dots to render the first time the page is visited
        self.update_idletasks()

    def prev_page(self):
        """Navigate to previous page if possible."""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def next_page(self):
        """Navigate to next page if available."""
        if self.current_page < len(self.page_texts) - 1:
            self.show_page(self.current_page + 1)
    
    def go_back(self):
        """Go back to the home page and reset to the first info page."""
        self.current_page = 0
        self.show_page(0)  # Show the first page when returning
        self.controller.show_frame("Home_page")
            
    def update_labels(self, texts):
        """Update labels with new text based on the current language."""   
        self.back_button.update_text(texts["back"])
        self.page_texts = texts["text_info"]
        self.show_page(self.current_page)