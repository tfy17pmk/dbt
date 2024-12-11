import tkinter as tk
import GUI.constants

class RoundedButton(tk.Canvas):
    """Rounded button class with text and image support."""

    def __init__(self, master=None, text: str = "", image=None, radius=25, btnforeground="#000000",
                 btnbackground=GUI.constants.background_color, clicked=None, *args, **kwargs):
        """Initialize the rounded button."""
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"], border=0, highlightthickness=0)
        self.btnbackground = btnbackground
        self.clicked = clicked
        self.radius = radius
        self.image = image
        self.constants = GUI.constants

        # Create the rounded rectangle background
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)

        # Create the text and image if provided
        self.text_id = self.create_text(0, 0, text=text, tags="button", fill=btnforeground,
                                        font=(self.constants.heading, 25), justify="center")
        if self.image:
            self.image_id = self.create_image(0, 0, image=self.image, tags="button")

        # Bind events for button click effects
        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)

        # Adjust button dimensions based on text and/or image size
        self.adjust_button_size()

    def adjust_button_size(self):
        """Adjust the button size based on text and/or image size."""
        text_rect = self.bbox(self.text_id)
        width = max(int(self["width"]), text_rect[2] - text_rect[0] + 20)
        height = max(int(self["height"]), text_rect[3] - text_rect[1] + 20)

        # Update button size if necessary
        if width > int(self["width"]):
            self["width"] = width
        if height > int(self["height"]):
            self["height"] = height
            
    def update_text(self, new_text):
        """Update the button's text dynamically."""
        self.itemconfig(self.text_id, text=new_text)
        self.adjust_button_size()

    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs):
        """Create a rounded rectangle."""
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1,
                  x2, y1 + radius, x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2,
                  x2 - radius, y2, x2 - radius, y2, x1 + radius, y2, x1 + radius, y2, x1, y2,
                  x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)
        else:
            self.coords(self.rect, points)

    def resize(self, event):
        """Resize the button when the canvas size changes."""
        text_bbox = self.bbox(self.text_id)

        # Ensure the radius does not exceed button dimensions
        radius = min(self.radius, event.width, event.height)

        # Calculate required width and height for the button
        width = max(event.width, text_bbox[2] - text_bbox[0] + 30)
        height = max(event.height, text_bbox[3] - text_bbox[1] + 30)

        # Update the rounded rectangle with the new size and radius
        self.round_rectangle(5, 5, width - 5, height - 5, radius, update=True)
        bbox = self.bbox(self.rect)

        # Calculate center positions for the button
        x_center = (bbox[2] + bbox[0]) / 2
        y_center = (bbox[3] + bbox[1]) / 2

        # Center the text and image based on availability
        if self.image and self.text_id:
            # Center both image and text in the middle, no offset
            self.coords(self.image_id, x_center, y_center)
            self.coords(self.text_id, x_center, y_center + 10)
        elif self.image:
            # Center the image directly if no text is present
            self.coords(self.image_id, x_center, y_center)
        else:
            # Center the text directly if no image is present
            self.coords(self.text_id, x_center, y_center)

    def border(self, event):
        """Handle button border changes on press and release."""
        if event.type == "4":
            self.itemconfig(self.rect)
            if self.clicked:
                self.clicked()
        else:
            self.itemconfig(self.rect, fill=self.btnbackground)
