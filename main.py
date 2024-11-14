from multiprocessing import Process, Queue, Event
from Image_processing.webcamera import Camera
from PID.pid import PID_control
from communication.communication import Commmunication
from test_code.find_ball import FindBall
from PID.class_PID import PID
import sys
import time

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
    #pid_controller = PID_control(k_pid)
    pid_controller = PID(k_pid, 1, 1)
    #goal_position = (0, 0)  # Desired position (update when we know coordinates for tables middle point)

    last_received_time = time.perf_counter()
    height = 15
    state1 = 1
    state2 = 0
    state3 = 1
    homing = False

    while not stop_event.is_set():
        if not queue_in.empty():
            current_position = queue_in.get()
            last_received_time = time.perf_counter()  # Update the time with each new data

            #control_x, control_y = pid_controller.get_angles(goal_position, current_position)
            control_x, control_y = pid_controller.compute(goal_position, current_position)
            
            #print(queue_in.size())
            print(f"Control angles: X: {control_x}, Y: {control_y}")
            # Send angles to ESP here
            esp_com.send_data(-control_x, control_y, height, state1, state2, state3, homing)
            esp_com.receive_response()

        # Check if 3 seconds have passed since the last update
        if time.perf_counter() - last_received_time > 3:
            pid_controller.reset()  # Reset the PID controllers
            esp_com.send_data(0, 0, height, state1, state2, state3, homing)
            last_received_time = time.perf_counter()  # Reset timer to avoid continuous reset



if __name__ == "__main__":
    #k_pid = [0.0004, 0.000002, 0.007, 0.1]
    #k_pid = [0.00065, 0, 0.005, 0.1]
    #k_pid = [0.0005, 0, 0.0005, 0.1]
    #k_pid = [0.00055, 0, 0.0005, 0.1] # working with adv pid
    #k_pid = [0.00055, 0.0004, 0.0005, 0.1] # working with new pid
    k_pid = [0.00055, 0.0007, 0.0007]

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
