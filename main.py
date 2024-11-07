from multiprocessing import Process, Queue, Event
from webcamera import Camera
from pid import PID_control
from communication import Commmunication
from find_ball import FindBall
import time
import sys

def capture_and_detect(queue, goal_position, stop_event):
    """Capture frames and detect ball coordinates, placing them in the queue."""
    camera = Camera()
    try:
        while not stop_event.is_set():
            frame = camera.get_frame()
            cropped_frame = camera.crop_frame(frame)
            if cropped_frame is not None:
                ball_coordinates = camera.get_ball(cropped_frame)
                if ball_coordinates != (-1, -1, 0):  # Valid detection
                    if not queue.full():
                        try:
                            queue.put(ball_coordinates, timeout=0.01)
                            print(ball_coordinates)
                        except e:
                            print(f"Queue error: {e}")
                    else:
                        print("Queue is full!")
                '''else:
                    if not queue.full():
                        try:
                            queue.put((0, 0, 0), timeout=0.01)
                            print("no ball detected")
                        except e:
                            print(f"Queue error: {e}")
                    else:
                        print("Queue is full!")'''

                camera.show_frame(cropped_frame, goal_position)  # Display frame if needed
            else:
                break
    finally:
        camera.clean_up_cam()

def capture_and_detect2(queue, stop_event):
    """Capture frames and detect ball coordinates, placing them in the queue."""
    camera = FindBall()
    try:
        while not stop_event.is_set():
            frame = camera.get_frame()
            cropped_frame = camera.crop_frame(frame)
            if cropped_frame is not None:
                ball_coordinates = camera.get_ball(cropped_frame)# * 0.0014
                if ball_coordinates != [-1, -1, 0]:  # Valid detection
                    if not queue.full():
                        try:
                            queue.put(ball_coordinates, timeout=0.01)
                        except e:
                            print(f"Queue error: {e}")
                camera.show_frame(cropped_frame)  # Display frame if needed
            else:
                break
    finally:
        camera.clean_up_cam()
        
def pid_control(queue_in, k_pid, esp_com, goal_position, stop_event):
    """Receive ball coordinates from the queue, compute control angles, and send commands."""
    pid_controller = PID_control(k_pid)
    goal_position = (0, 0)  # Desired position (update when we know coordinates for tables middle point)

    while not stop_event.is_set():
        if not queue_in.empty():
            current_position = queue_in.get()
            control_x, control_y = pid_controller.get_angles(goal_position, current_position)
            height = 13
            state1 = 1
            state2 = 0
            state3 = 1
            homing = False
            #print(queue_in.size())
            print(f"Control angles: X: {control_x}, Y: {control_y}")
            # Send angles to ESP here
            esp_com.send_data(-control_x, control_y, height, state1, state2, state3, homing)


if __name__ == "__main__":
    #k_pid = [0.0004, 0.000002, 0.007, 0.1]
    #k_pid = [0.00065, 0, 0.005, 0.1]
    #k_pid = [0.0005, 0, 0.0005, 0.1]
    k_pid = [0.00055, 0, 0.0005, 0.1]
    goal_position = (0,0)
    ball_coords_queue = Queue(maxsize=5)
    stop_event = Event()
    esp_com = Commmunication()

    # Create processes
    capture_process = Process(target=capture_and_detect, args=(ball_coords_queue, goal_position, stop_event), daemon=True)
    pid_process = Process(target=pid_control, args=(ball_coords_queue, k_pid, esp_com, goal_position, stop_event), daemon=True)

    # Start processes
    capture_process.start()
    pid_process.start()

    try:
        # Main loop
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
