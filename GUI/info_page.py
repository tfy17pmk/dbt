import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import constants
import button

class Info_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_page = 0

        self.configure(bg=constants.background_color)

        # Load the arrow icon and create rotated version for left button
        original_arrow = Image.open(constants.RIGHT_ARROW).resize((20, 20))
        self.right_arrow_icon = ImageTk.PhotoImage(original_arrow)
        self.left_arrow_icon = ImageTk.PhotoImage(original_arrow.rotate(180))

        # Load images for each page (eyes, arm, and brain images)
        eyes_image_original = Image.open(constants.EYES).resize((300, 300))
        self.eyes_image_icon = ImageTk.PhotoImage(eyes_image_original)

        arm_image_original = Image.open(constants.ARM).resize((250, 250))
        self.arm_image_icon = ImageTk.PhotoImage(arm_image_original)

        brain_image_original = Image.open(constants.BRAIN).resize((250, 250))
        self.brain_image_icon = ImageTk.PhotoImage(brain_image_original)

        # Load the light icon for the dynamic button
        self.light_icon = ImageTk.PhotoImage(Image.open(constants.LIGHT_BULB).resize((40, 40)))

        button_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0)
        button_frame.grid(row=2, column=1, sticky="sw")

        # Placeholder for each page's unique text and actions
        self.page_texts = constants.info_text

        def send_light_data(light):
            print("turning on light")
            print(light)
            
        self.page_actions = [
            lambda: print("Action for Page 1"), 
            lambda: send_light_data(1),
            lambda: send_light_data(2),
            lambda: send_light_data(3)
        ]

        # Configure grid layout to center content
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=9)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Prevents dynamic resizing when widgets are shown/hidden
        self.grid_propagate(False)

        # Dots canvas for page indicators
        self.dots = tk.Canvas(self, height=30, bg=constants.background_color, highlightthickness=0)
        self.dots.grid(row=2, column=1, pady=30, sticky="n")

        # Create canvases for navigation buttons
        self.btn_prev_canvas = tk.Canvas(self, width=40, height=40, bg=constants.background_color, highlightthickness=0)
        self.btn_prev_canvas.grid(row=2, column=1, sticky="nw", padx=(500, 0), pady=30)
        
        self.btn_next_canvas = tk.Canvas(self, width=40, height=40, bg=constants.background_color, highlightthickness=0)
        self.btn_next_canvas.grid(row=2, column=1, sticky="ne", padx=(0, 500), pady=30)

        # Draw circular buttons with arrow icons, and store IDs
        self.left_arrow_id = self.create_circle_button(self.btn_prev_canvas, 20, 20, 18, self.left_arrow_icon, self.prev_page)
        self.right_arrow_id = self.create_circle_button(self.btn_next_canvas, 20, 20, 18, self.right_arrow_icon, self.next_page)

        # Text widget for page content with tagged fonts
        self.page_content_text = tk.Text(
            self, 
            wrap="word", 
            font=constants.body_text, 
            bg=constants.background_color, 
            relief="flat", 
            height=15, 
            width=70, 
            highlightthickness=0,
            pady=100,
            padx=100
        )
        self.page_content_text.grid(row=1, column=1, sticky="ne")
        self.page_content_text.tag_configure("heading", font=constants.heading, foreground=constants.text_color)
        self.page_content_text.tag_configure("body", font=constants.body_text, foreground=constants.text_color)
        self.page_content_text.config(state="disabled")

        # Frame to hold the button (keeps layout stable)
        self.dynamic_button_frame = tk.Frame(self, bg=constants.background_color)
        self.dynamic_button_frame.grid(row=1, column=1, pady=200, padx=300, sticky="se")

        # Placeholder spacer label to maintain consistent layout when button is hidden
        self.spacer_label = tk.Label(self.dynamic_button_frame, text="", height=2, bg=constants.background_color)
        self.spacer_label.grid(row=0, column=0)

        # Define a custom style for the rounded button
        style = ttk.Style()
        style.configure("RoundedButton.TButton", 
                        foreground=constants.text_color,   # Text color
                        background=constants.background_color,    # Background color
                        borderwidth=0, 
                        focuscolor=style.configure(".")["background"])  # Match focus color to background
        
        style.map("RoundedButton.TButton",
                  background=[("active", constants.background_color)])  # Hover color

        # Use RoundedButton for the dynamic button with light bulb icon
        self.dynamic_button = button.RoundedButton(
            master=self.dynamic_button_frame,
            text="",  # No text since we're using an icon
            radius=25,
            width=70,
            height=70,
            btnbackground=constants.text_color,  # Button background
            btnforeground=constants.background_color,  # Icon/text color
            image=self.light_icon,  # Set the light bulb icon
            clicked=lambda: self.page_actions[self.current_page]()  # Action based on page
        )
        self.dynamic_button.grid(row=0, column=0)

        # Lower-left corner button to go back
        self.back_button = button.RoundedButton(
            master = button_frame, 
            text="Bakåt", 
            radius=25, 
            width=200, 
            height=70, 
            btnbackground=constants.text_color, 
            btnforeground=constants.background_color, 
            clicked=lambda: controller.show_frame("Home_page")
        )
        self.back_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

        # Canvas to display images on relevant pages
        self.image_canvas = tk.Canvas(self, width=400, height=300, bg=constants.background_color, highlightthickness=0)
        self.image_canvas.grid(row=1, column=1, padx=50, sticky="nw")
        self.image_canvas.grid_remove()  # Initially hidden

        # Display the first page initially
        self.show_page(0)

        # Fix for initial rendering of dots
        self.after(100, self.update_dots)

    def create_circle_button(self, canvas, x, y, radius, icon, command):
        """Draw a circular button with an icon inside it on the canvas and bind it to a command."""
        circle_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=constants.text_color, outline="")
        image_id = canvas.create_image(x, y, image=icon)
        
        # Bind click events to both the circle and image
        canvas.tag_bind(circle_id, "<Button-1>", lambda event: command())
        canvas.tag_bind(image_id, "<Button-1>", lambda event: command())
        
        return circle_id, image_id

    def show_page(self, page_index):
        """Show page at given index by updating content text, dynamic button, and arrow visibility."""
        self.current_page = page_index

        # Clear and update the Text widget for the current page
        self.page_content_text.config(state="normal")
        self.page_content_text.delete("1.0", tk.END)

        # Set text alignment based on the current page
        self.page_content_text.tag_configure("left", justify="left")
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["heading"] + "\n", ("heading", "left"))
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["body"], ("body", "left"))
        self.page_content_text.grid(sticky="ne")
        
        self.page_content_text.config(state="disabled")

        # Show or hide the appropriate image based on the current page
        self.image_canvas.delete("all")  # Clear any existing image first
        if page_index == 1:
            self.image_canvas.create_image(125, 125, image=self.eyes_image_icon)
            self.image_canvas.grid()  # Show the canvas
        elif page_index == 2:
            self.image_canvas.create_image(125, 170, image=self.arm_image_icon)
            self.image_canvas.grid()  # Show the canvas
        elif page_index == len(self.page_texts) - 1:
            self.image_canvas.create_image(125, 170, image=self.brain_image_icon)
            self.image_canvas.grid()  # Show the canvas
        else:
            self.image_canvas.grid_remove()  # Hide the canvas if no image is needed

        # Update dynamic button visibility based on the current page
        if page_index == 0:
            self.dynamic_button.grid_remove()  # Hide by removing from frame (keeps layout stable)
        else:
            self.dynamic_button.grid()  # Show by adding back to frame

        # Update arrow visibility based on the current page
        self.update_arrow_visibility()

        # Update the dots to show the current page
        self.update_dots()

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
            color = constants.text_color if i == self.current_page else constants.background_color
            dot = self.dots.create_oval(x, 10, x + 2 * dot_radius, 10 + 2 * dot_radius, fill=color)
            self.dots.tag_bind(dot, "<Button-1>", lambda event, index=i: self.show_page(index))

    def prev_page(self):
        """Navigate to previous page if possible."""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def next_page(self):
        """Navigate to next page if available."""
        if self.current_page < len(self.page_texts) - 1:
            self.show_page(self.current_page + 1)
