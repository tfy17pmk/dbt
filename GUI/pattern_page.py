import tkinter as tk
import constants
import button

# Page 3: Page Two
class Pattern_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=constants.background_color)

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        button_width = int(screen_width * 0.05)
        button_height = int(screen_height * 0.05)

        # Setup grid pattern with equal weight for each row and column
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)


        # Button frame for holding buttons, now added to layout
        button_frame = tk.Frame(self, bg=constants.background_color, highlightthickness=0, borderwidth=0)
        button_frame.config(borderwidth=0, )
        button_frame.grid(row=1, column=3, sticky="nsew", rowspan=2, pady=20)  # Set grid position for button_frame

        # Pattern Page title
        label = tk.Label(self, text="Skapa ett mönster", font=(constants.heading, 24), fg=constants.text_color, bg=constants.background_color)
        label.grid(row=0, column=1, columnspan=2, pady=20)  # Set label position with grid, centered across columns

        # Canvas for creating patterns
        self.canvas = tk.Canvas(self, width=600, height=600, bg=constants.text_color, highlightthickness=0)
        self.canvas.grid(row=1, column=1, columnspan=2, pady=0)
        '''
        # Function to create a rounded rectangle on canvas
        def create_rounded_rectangle(canvas, x, y, width, height, radius=25, fill="#ffffff", outline="black", update=True):
            points = [x+radius, y,
                        x+radius, y,
                        width-radius, y,
                        width-radius, y,
                        width, y,
                        width, y+radius,
                        width, y+radius,
                        width, y-radius,
                        width, y-radius,
                        width, y,
                        width-radius, height,
                        width-radius, height,
                        x+radius, height,
                        x+radius, height,
                        x, height,
                        x, height-radius,
                        x, height-radius,
                        x, y+radius,
                        x, y+radius,
                        x, y]
                        
            return canvas.create_polygon(points, smooth=True, fill=fill)


        # Function to create a rectangular button
        def create_rectangular_button(frame, text, command, button_width, button_height):
            # Container for each button
            btn_container = tk.Frame(frame, bg=constants.background_color)
            btn_container.pack(padx=5, pady=5)

            
            # Canvas for button appearance
            canvas = tk.Canvas(btn_container, width=button_width, height=button_height, highlightthickness=0, bg=constants.background_color)
            canvas.pack()

            create_rounded_rectangle(canvas, 0, 0, button_width, button_height, radius=10, fill=constants.text_color, outline="black")
            
            # Bind action to canvas
            #canvas.bind("<Button-1>", lambda e: command())
            return btn_container

        def place_button(text, command, r, c, px, py):
            button = create_rectangular_button(button_frame, text, command, button_width, button_height)
            button.grid(row=r, column=c, sticky="nsew", padx=px, pady=py)

        # Button actions
        def draw_square_button():
            print("Drawing square pattern...")
            self.canvas.create_rectangle(50, 50, 150, 150, outline="black")

        def draw_circle():
            print("Drawing circle pattern...")
            self.canvas.create_oval(50, 50, 150, 150, outline="black")

        def undo():
            print("Undoing pattern...")
            self.canvas.delete("all")

        # Place the rectangle button using `place_button`
        place_button('Rectangle', draw_square_button, 1, 4, 10, 5)
        '''
        but_rec = button.RoundedButton(master = button_frame, text="Rectangle", radius=25, width=200, height=70, 
                                   btnbackground=constants.text_color, btnforeground=constants.background_color, clicked=None)
        but_circ = button.RoundedButton(master = button_frame, text="Circle", radius=25, width=200, height=70, 
                                   btnbackground=constants.text_color, btnforeground=constants.background_color, clicked=None)
        but_tri = button.RoundedButton(master = button_frame, text="Triangle", radius=25, width=200, height=70, 
                                   btnbackground=constants.text_color, btnforeground=constants.background_color, clicked=None)
        but_star = button.RoundedButton(master = button_frame, text="Star", radius=25, width=200, height=70, 
                                   btnbackground=constants.text_color, btnforeground=constants.background_color, clicked=None)
        but_rec.grid(row=2, column=4, sticky="nsew")
        but_circ.grid(row=3, column=4, sticky="nsew", pady=30)
        but_tri.grid(row=4, column=4, sticky="nsew", pady=30)
        but_star.grid(row=5, column=4, sticky="nsew", pady=30)