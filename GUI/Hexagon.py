import tkinter as tk
import math

class HexagonShape:
    def __init__(self, canvas, fill="#ffffff", outline="#ffffff"):
        self.canvas = canvas
        self.points = []  # Hexagonens hörnpunkter
        self.fill = fill
        self.outline = outline
        
        # Bind to draw the hexagon in the case of window resize
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind to handle clicking on the hexagon
        self.canvas.bind("<Button-1>", self.on_click)

        # Create initial hexagon
        self.create_hexagon()

    def create_hexagon(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Find center and radius
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = width // 2.05  # Making sure hexagon fits on the canvas

        # Finding the corner positions of the hexagon
        self.points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            self.points.append((x, y))

        # Fill the canvas with the hexagon
        self.canvas.create_polygon(self.points, outline=self.outline, fill=self.fill, width=2)

    def on_resize(self, event):
        # Rescale the hexagon in case of window size changing
        self.create_hexagon()

    def on_click(self, event):
        # Check if the click is within the borders
        if self.is_point_inside_hexagon(event.x, event.y):
            print(f"Klick inuti hexagonen vid koordinat: ({event.x}, {event.y})")
        else:
            print("Klick utanför hexagonen")

    def is_point_inside_hexagon(self, x, y):
        # Point-within-polygon-test (Ray-casting algorithm)
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0]
        for i in range(n + 1):
            p2x, p2y = self.points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
