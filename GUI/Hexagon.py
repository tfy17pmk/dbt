import tkinter as tk
import math

class HexagonShape:
    def __init__(self, canvas, fill="#ffffff", outline="#ffffff"):
        self.canvas = canvas
        self.points = []  # Hexagonens hörnpunkter
        self.fill = fill
        self.outline = outline
        
        # Bind för att rita hexagonen när storleken ändras
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind för att hantera klick på hexagonen
        self.canvas.bind("<Button-1>", self.on_click)

        # Rita hexagon för första gången
        self.create_hexagon()

    def create_hexagon(self):
        # Rensa canvas innan vi ritar om
        self.canvas.delete("all")
        
        # Hitta mitten och radien för hexagonen
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2.05  # Anpassa radien så hexagonen får plats

        # Beräkna hexagonens hörnpunkter
        self.points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            self.points.append((x, y))

        # Skapa hexagonen på canvas
        self.canvas.create_polygon(self.points, outline=self.outline, fill=self.fill, width=2)

    def on_resize(self, event):
        # Skala om hexagonen när fönstret ändrar storlek
        self.create_hexagon()

    def on_click(self, event):
        # Kontrollera om klicket är inom hexagonen
        if self.is_point_inside_hexagon(event.x, event.y):
            print(f"Klick inuti hexagonen vid koordinat: ({event.x}, {event.y})")
        else:
            print("Klick utanför hexagonen")

    def is_point_inside_hexagon(self, x, y):
        # Punkt-inom-polygon-test (Ray-casting algoritm)
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
