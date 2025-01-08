from multiprocessing import Process, Queue, Event, Value
from Image_processing.webcamera import Camera
from communication.communication import Commmunication
from PID.class_pid import PID
from GUI.gui import App
import cv2 as cv
import sys
import time
import signal

class SharedResources:
    """Class to hold shared resources between processes."""
    def __init__(self):
        # Shared queues
        self.goal_position_queue = Queue(maxsize=5)
        self.ball_coords_queue = Queue(maxsize=5)
        self.gui_frame_queue = Queue(maxsize=10)
        self.joystick_control_queue = Queue(maxsize=20)
        # Shared variables
        self.send_frames_to_gui = Value('b', False)
        self.send_frames_to_challenge = Value('b', False)
        self.esp_com = Commmunication()

def put_value_in_shared_queue(value, shared_queue, variant):
    """Put a value in the shared queue if it is not full."""
    if not shared_queue.full():
        try:
            shared_queue.put(value, timeout=0.01)
        except Exception as e:
            print(f"Queue error: {e}")
    else:
        print(f"Queue {variant} is full!")

def empty_queue(queue):
    """Empty all items from the queue."""
    while not queue.empty():
        queue.get()

def capture_and_detect(resources, stop_event):
    """Capture frames and detect ball coordinates, placing them in the queue."""
    camera = Camera()
    try:
        while not stop_event.is_set():
            frame = camera.get_frame()
            cropped_frame = camera.crop_frame(frame)
            cropped_frame = cv.cvtColor(cropped_frame, cv.COLOR_BGR2RGB)

            # Detect ball coordinates and put them in the queue
            if cropped_frame is not None:
                ball_coordinates = camera.get_ball(cropped_frame)
                if ball_coordinates != (-1, -1, 0):  # Valid detection
                    put_value_in_shared_queue(ball_coordinates, resources.ball_coords_queue, 1)

                # If in info-page, send frame to GUI
                if resources.send_frames_to_gui.value:
                    rotated_frame = cv.rotate(cropped_frame, cv.ROTATE_180)
                    put_value_in_shared_queue(rotated_frame, resources.gui_frame_queue, 2)
                else:
                    # Clear the queue if not empty
                    if not resources.gui_frame_queue.empty():
                        empty_queue(resources.gui_frame_queue)  

    except KeyboardInterrupt:
        print("Capture process interrupting. Exiting.")
    finally:
        camera.clean_up_cam()

def pid_control(resources, k_pid, stop_event):
    """Receive ball coordinates from the queue, compute control angles, and send commands."""
    pid_controller = PID(k_pid, 1, 1)

    last_received_time = time.perf_counter()
    height = 15
    state1 = 1
    state2 = 0
    state3 = 1
    homing = False
    local_goal_pos = (0, 0)
    local_joystick_control = None
    controlling = local_joystick_control
    last_tuple = (0 ,0)
    reset = False

    try:
        while not stop_event.is_set():
            # Check for joystick control input
            if not resources.joystick_control_queue.empty():
                local_joystick_control = resources.joystick_control_queue.get_nowait()

            # check data type of joystick input
            if isinstance(local_joystick_control, bool):
                controlling = False
                local_joystick_control = None
                pid_controller.reset()

            elif isinstance(local_joystick_control, tuple) and (last_tuple is not local_joystick_control):
                last_tuple = local_joystick_control
                resources.esp_com.send_data(local_joystick_control[0], local_joystick_control[1], height, state1, state2, state3, homing)
                controlling = True


            # Check for ball coordinates
            if not resources.ball_coords_queue.empty():
                current_position = resources.ball_coords_queue.get_nowait()
                last_received_time = time.perf_counter()  # Update the time with each new data
                reset = False

                # Check for goal position
                if not resources.goal_position_queue.empty():
                    local_goal_pos = resources.goal_position_queue.get_nowait()


                # Send control angles to ESP if not in joystick control mode
                if not controlling:
                    # Compute control angles
                    if isinstance(local_goal_pos[0], int) and isinstance(local_goal_pos[0], int):
                        control_x, control_y = pid_controller.compute(local_goal_pos, current_position)
                    resources.esp_com.send_data(-control_x, control_y, height, state1, state2, state3, homing)

            # Check if 3 seconds have passed since the last update, reset in that case
            if (time.perf_counter() - last_received_time > 3) and not controlling and not reset:
                pid_controller.reset()  # Reset the PID controllers
                # BAD CODE! speeds up return to initial position
                for i in range(10):
                    resources.esp_com.send_data(0.14, 0.14, height, state1, state2, state3, homing)
                    resources.esp_com.send_data(0, 0, height, state1, state2, state3, homing)


                last_received_time = time.perf_counter()  # Reset timer to avoid continuous reset
                reset = True
    
    except KeyboardInterrupt:
        print("PID control process interrupted. Exiting.")
    finally:
        pass

def handle_keyboard_interrupt(signum, frame, stop_event):
    """Handle keyboard interrupt by setting the stop event."""
    print("Keyboard interrupt received. Exiting...")
    stop_event.set()

def shutdown_processes(capture_process, pid_process, stop_event):
    """Shutdown processes."""
    stop_event.set()
    print("Shutting down processes.")
    # Allow processes to finish gracefully within timeout
    capture_process.join(timeout=5)
    pid_process.join(timeout=5)

    # Force terminate if still alive
    if capture_process.is_alive():
        capture_process.terminate()
    if pid_process.is_alive():
        pid_process.terminate()

def shutdown_gui(app):
    """Shutdown the GUI application."""
    if app is not None:
        print("Destroing application.")
        app.destroy()

def check_for_stop(app, stop_event):
    """Periodically check if the stop event is set and quit the app if it is."""
    if stop_event.is_set():
        print("Stop event is set. Quiting appplication.")
        app.join_threads()
        app.quit()
    else:
        app.after(100, check_for_stop, app, stop_event)

if __name__ == "__main__":
    
    k_pid = [0.0008, 0.0000669, 0.0006505, 0.00098, 0.00019, 0.00067]

    resources = SharedResources()
    stop_event = Event()

    # Create processes
    capture_process = Process(target=capture_and_detect, args=(resources, stop_event), daemon=True)
    pid_process = Process(target=pid_control, args=(resources, k_pid, stop_event), daemon=True)

    # Start processes
    capture_process.start()
    pid_process.start()

    # Register signal handler for KeyboardInterrupt
    signal.signal(signal.SIGINT, lambda signum, frame: handle_keyboard_interrupt(signum, frame, stop_event))

    try:
        app = App(resources=resources)

        # Start the periodic check of the stop event
        app.after(100, check_for_stop, app, stop_event)

        app.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        stop_event.set()

    finally:
        # Stop processes
        shutdown_processes(capture_process, pid_process, stop_event)
        # Exit GUI
        shutdown_gui(app)