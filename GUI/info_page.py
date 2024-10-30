import tkinter as tk
import constants

class Info_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_page = 0
        
        self.configure(bg=constants.background_color)

        # Placeholder list for pages (create individual frames or widgets for each page if needed)
        self.pages = [tk.Label(self, text=f"Page {i + 1}", font=constants.heading) for i in range(5)]

        # Configure grid layout to center content both vertically and horizontally
        self.grid_rowconfigure(0, weight=0)  # Spacer row at the top
        self.grid_rowconfigure(1, weight=9)  # Main content row
        self.grid_rowconfigure(2, weight=1)  # Dots and buttons row

        self.grid_columnconfigure(0, weight=0)  # Spacer column on the left
        self.grid_columnconfigure(1, weight=1)  # Main content column
        self.grid_columnconfigure(2, weight=0)  # Spacer column on the right

        # Dots canvas for page indicators at the bottom, spanning all columns
        self.dots = tk.Canvas(self, height=30)
        self.dots.grid(row=2, column=1, pady=30, sticky="n")  # Center the dots canvas in its cell

        # Navigation buttons aligned with dots row
        self.btn_prev = tk.Button(self, text="<< Prev", command=self.prev_page)
        self.btn_prev.grid(row=2, column=1, padx=500, pady=30, sticky="nw")  # Centered in the left cell

        self.btn_next = tk.Button(self, text="Next >>", command=self.next_page)
        self.btn_next.grid(row=2, column=1, padx=500, pady=30, sticky="ne")  # Centered in the right cell
        
        self.lower_left_button = tk.Button(self, text="Tillbaka", command=lambda: controller.show_frame("Home_page"))
        self.lower_left_button.grid(row=2, column=1, padx=10, pady=10, sticky="sw")  # Lower-left corner

        # Show the first page initially
        self.show_page(0)

        # Fix for initial rendering of dots
        self.after(100, self.update_dots)

    def show_page(self, page_index):
        """Show page at given index by bringing it to the front."""
        # Only bring the selected page to the front without hiding other pages
        page = self.pages[page_index]
        page.grid(row=1, column=1, sticky="nsew")  # Ensure it's placed correctly
        page.lift()  # Bring the selected page to the front

        self.current_page = page_index
        self.update_dots()

    def update_dots(self):
        """Update the dots to show current page and make them clickable."""
        self.dots.delete("all")
        dot_radius = 5
        dot_spacing = 20
        center_x = (self.dots.winfo_width() / 2) - (len(self.pages) * dot_spacing / 2)  # Calculate center position
        
        for i in range(len(self.pages)):
            x = center_x + i * dot_spacing
            color = "black" if i == self.current_page else "gray"
            dot = self.dots.create_oval(x, 10, x + 2 * dot_radius, 10 + 2 * dot_radius, fill=color)

            # Bind click event to each dot, passing the page index as a lambda argument
            self.dots.tag_bind(dot, "<Button-1>", lambda event, index=i: self.show_page(index))

    def prev_page(self):
        """Navigate to previous page if possible."""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def next_page(self):
        """Navigate to next page if available."""
        if self.current_page < len(self.pages) - 1:
            self.show_page(self.current_page + 1)
