from multiprocessing import Process, Event, Array
from Image_processing.webcamera import Camera
from PID.pid import PID_control
from communication.communication import Commmunication
import sys

def capture_and_detect(array, stop_event):
    """Capture frames and detect ball coordinates, placing them in the queue."""
    camera = Camera()
    try:
        while not stop_event.is_set():
            frame = camera.get_frame()
            cropped_frame = camera.crop_frame(frame)
            if cropped_frame is not None:
                ball_coordinates = camera.get_ball(cropped_frame)
                if ball_coordinates != (-1, -1, 0):  # Valid detection
                    with array.get_lock():
                        array[0] = ball_coordinates[0]
                        array[1] = ball_coordinates[1]
                        print(f"Updated coordinates: x: {array[0]}, y: {array[1]}")
                camera.show_frame(cropped_frame)  # Display frame if needed
            else:
                break
    finally:
        camera.clean_up_cam()
        
def pid_control(array, k_pid, esp_com, stop_event):
    """Receive ball coordinates from the queue, compute control angles, and send commands."""
    pid_controller = PID_control(k_pid)
    goal_position = (0, 0)  # Desired position (update when we know coordinates for tables middle point)

    while not stop_event.is_set():
        current_position = (array[0], array[1])
        control_x, control_y = pid_controller.get_angles(goal_position, current_position)
        height = 15
        state1 = 1
        state2 = 0
        state3 = 1
        homing = False
        print(f"Control angles: X: {control_x}, Y: {control_y}")
        # Send angles to ESP here
        esp_com.send_data(-control_x, -control_y, height, state1, state2, state3, homing)


if __name__ == "__main__":
    #k_pid = [0.0004, 0.000002, 0.007, 0.1]
    k_pid = [0.002, 0.0, 0, 0.2]
    ball_coords = Array('i', [0, 0])
    stop_event = Event()
    esp_com = Commmunication()

    # Create processes
    capture_process = Process(target=capture_and_detect, args=(ball_coords, stop_event), daemon=True)
    pid_process = Process(target=pid_control, args=(ball_coords, k_pid, esp_com, stop_event), daemon=True)

    # Start processes
    capture_process.start()
    pid_process.start()

    # Main loop
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
        stop_event.set()  # Signal processes to stop
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        stop_event.set()
    finally:
        # Ensure all processes are terminated
        capture_process.join(timeout=1)
        pid_process.join(timeout=1)

        # Force terminate if still alive
        if capture_process.is_alive():
            capture_process.terminate()
        if pid_process.is_alive():
            pid_process.terminate()
