import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import constants

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
            height=10, 
            width=50, 
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
        self.dynamic_button_frame.grid(row=1, column=1, pady=(200, 0), sticky="s")

        # Placeholder spacer label to maintain consistent layout when button is hidden
        self.spacer_label = tk.Label(self.dynamic_button_frame, text="", height=2, bg=constants.background_color)
        self.spacer_label.grid(row=0, column=0)

        # Dynamic action button
        self.dynamic_button = ttk.Button(self.dynamic_button_frame, text="Dynamic Action")
        self.dynamic_button.grid(row=0, column=0)  # Button initially in frame

        # Lower-left corner button to go back
        self.lower_left_button = ttk.Button(self, text="Tillbaka", command=lambda: controller.show_frame("Home_page"), style="Flat.TButton")
        self.lower_left_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

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
        
        # Insert heading and body text with tags
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["heading"] + "\n", "heading")
        self.page_content_text.insert(tk.END, self.page_texts[page_index]["body"], "body")
        self.page_content_text.config(state="disabled")

        # Update dynamic button visibility based on the current page
        if page_index == 0:
            self.dynamic_button.grid_remove()  # Hide by removing from frame (keeps layout stable)
        else:
            self.dynamic_button.grid()  # Show by adding back to frame

        # Update dynamic button action for the current page
        self.dynamic_button.config(command=self.page_actions[page_index])

        # Update arrow visibility based on the current page
        self.update_arrow_visibility()

        # Update the dots to show the current page
        self.update_dots()

    def update_arrow_visibility(self):
        """Hide left arrow on the first page and right arrow on the last page."""
        # Hide the left arrow if on the first page, else show it
        if self.current_page == 0:
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[0], state="hidden")
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[1], state="hidden")
        else:
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[0], state="normal")
            self.btn_prev_canvas.itemconfigure(self.left_arrow_id[1], state="normal")

        # Hide the right arrow if on the last page, else show it
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
