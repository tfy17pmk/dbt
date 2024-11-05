from webcamera import Camera as class_camera
from pid import PID_control as class_PID
import time
import numpy as np

# PID-variabler
K_PID = [0, 0, 0, 0]
camera = class_camera.Camera()
pid = class_PID.PID_control(K_PID)

# Startvärden för koordinater och area
x = -1
y = -1
area = -1
goal = [0, 0]

# Starttider för FPS-beräkning
img_start_time = time.time()
rob_start_time = time.time()

def update_position():
    """Uppdaterar positionen för bollen genom att läsa en bild från kameran."""
    global x, y, area, img_start_time, rob_start_time
    image = camera.get_frame()
    if image is None:
        print("Kunde inte fånga bild. Avslutar.")
        return None  # Returnera None om bilden inte är tillgänglig

    # Uppdatera bildhämtning FPS
    img_frame_count += 1
    if img_frame_count == 100:
        img_end_time = time.time()
        img_elapsed_time = img_end_time - img_start_time
        img_fps = 100 / img_elapsed_time
        img_start_time = img_end_time
        img_frame_count = 0
        print(f"Bildhämtning FPS: {img_fps:.2f}")

    # Detektera bollen och uppdatera koordinater
    x, y, area = camera.get_ball(image)

    # Uppdatera objektigenkännings-FPS
    rob_frame_count += 1
    if rob_frame_count == 100:
        rob_end_time = time.time()
        rob_elapsed_time = rob_end_time - rob_start_time
        rob_fps = 100 / rob_elapsed_time
        rob_start_time = rob_end_time
        rob_frame_count = 0
        print(f"Objektigenkänning FPS: {rob_fps:.2f}")

    return x, y  # Returnera positionerna


def calculate_angles(goal, current):
    """Beräknar styrvinklarna theta och phi baserat på målet och den aktuella positionen."""
    theta, phi = pid.get_angles(goal, current)
    return theta, phi


try:
    # Huvudloop
    while True:
        # Uppdatera bollens position
        position = update_position()
        
        if position is None:
            break  # Avsluta loopen om det inte finns någon position att uppdatera

        # Beräkna styrvinklar baserat på mål och aktuell position
        current = [x, y]
        theta, phi = calculate_angles(goal, current)
        
        # Skicka vidare theta och phi till nästa funktion
        # Exempelvis: send_to_actuator(theta, phi)
        print(f"Styrvinklar: theta={theta:.2f}, phi={phi:.2f}")

finally:
    # Rensa kameran
    camera.clean_up_cam()
