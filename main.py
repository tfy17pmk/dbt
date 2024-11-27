from multiprocessing import Process, Queue, Event, Value
from Image_processing.webcamera import Camera
from PID.pid import PID_control
from communication.communication import Commmunication
from PID.class_PID import PID
from GUI.GUI import App
import cv2 as cv
import sys
import time
import signal

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

def capture_and_detect(queue, gui_queue, send_frames_to_gui, gui_challange_frame_queue, 
                       send_frames_to_challenge, ball_coords_gui_queue, goal_position, 
                       stop_event):
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
                    put_value_in_shared_queue(ball_coordinates, queue, 1)

                # If in info-page, send frame to GUI
                if send_frames_to_gui.value:
                    #print("Sending frame to GUI")
                    put_value_in_shared_queue(cropped_frame, gui_queue, 2)
                else:
                    if not gui_queue.empty():
                        empty_queue(gui_queue)  # Clear the queue if not empty

                # In in challenge page, send frames
                if send_frames_to_challenge.value:
                    put_value_in_shared_queue(cropped_frame, gui_challange_frame_queue, 3)
                    put_value_in_shared_queue(ball_coordinates, ball_coords_gui_queue, 4)
                else:
                    if not gui_challange_frame_queue.empty():
                        empty_queue(gui_challange_frame_queue)

                #camera.show_frame(cropped_frame, goal_position)  # Display frame if needed
            else:
                break
    finally:
        camera.clean_up_cam()
        pass

def pid_control(queue_in, k_pid, esp_com, goal_position_queue, joystick_control_queue, stop_event):
    """Receive ball coordinates from the queue, compute control angles, and send commands."""
    
    pid_controller = PID(k_pid, 1, 1)

    last_received_time = time.perf_counter()
    height = 15
    state1 = 1
    state2 = 0
    state3 = 1
    homing = False
    local_goal_pos = (0, 0)
    local_joystick_control = False
    controlling = local_joystick_control
    last_tuple = (0 ,0)

    while not stop_event.is_set():
        if not joystick_control_queue.empty():
            local_joystick_control = joystick_control_queue.get_nowait()
    
        if isinstance(local_joystick_control, bool):
            controlling = False
        elif isinstance(local_joystick_control, tuple) and (last_tuple is not local_joystick_control):
            last_tuple = local_joystick_control
            esp_com.send_data(local_joystick_control[0], local_joystick_control[1], height, state1, state2, state3, homing)
            controlling = True

        if not queue_in.empty():
            current_position = queue_in.get_nowait()
            last_received_time = time.perf_counter()  # Update the time with each new data
            if not goal_position_queue.empty():
                local_goal_pos = goal_position_queue.get_nowait()

            control_x, control_y = pid_controller.compute(local_goal_pos, current_position)

            
            if not controlling:
                esp_com.send_data(-control_x, control_y, height, state1, state2, state3, homing)

        # Check if 3 seconds have passed since the last update
        if (time.perf_counter() - last_received_time > 3) and not controlling:
            pid_controller.reset()  # Reset the PID controllers
            esp_com.send_data(0, 0, height, state1, state2, state3, homing)
            last_received_time = time.perf_counter()  # Reset timer to avoid continuous reset

def handle_keyboard_interrupt(signum, frame):
    """Handle keyboard interrupt by setting the stop event."""
    print("Keyboard interrupt received. Exiting...")
    stop_event.set()  # Signal processes to stop

if __name__ == "__main__":
    
    k_pid = [0.0008, 0.0000669, 0.0006505, 0.00098, 0.00019, 0.00067]

    joystick_control_queue = Queue(maxsize=5)
    goal_position_queue = Queue(maxsize=5)
    ball_coords_queue = Queue(maxsize=5)
    ball_coords_gui_queue = Queue(maxsize=5)
    gui_frame_queue = Queue(maxsize=10)
    gui_challange_frame_queue = Queue(maxsize=10)
    stop_event = Event()
    send_frames_to_gui = Value('b', False)
    send_frames_to_challenge = Value('b', False)
    esp_com = Commmunication()

    # Create processes
    capture_process = Process(target=capture_and_detect, args=(ball_coords_queue, gui_frame_queue, send_frames_to_gui, gui_challange_frame_queue, 
                                                               send_frames_to_challenge, ball_coords_gui_queue, goal_position_queue, 
                                                                stop_event), daemon=True)
    
    pid_process = Process(target=pid_control, args=(ball_coords_queue, k_pid, esp_com, goal_position_queue, joystick_control_queue,stop_event), daemon=True)

    # Start processes
    capture_process.start()
    pid_process.start()

    # Register signal handler for KeyboardInterrupt
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)

    try:
        app = App(send_frames_to_gui=send_frames_to_gui, gui_frame_queue=gui_frame_queue, send_frames_to_challenge=send_frames_to_challenge, 
                  gui_challange_frame_queue=gui_challange_frame_queue, ball_coords_queue=ball_coords_gui_queue, goal_pos_queue=goal_position_queue,
                  joystick_control_queue=joystick_control_queue)
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        stop_event.set()
    finally:
        # Stop processes
        stop_event.set()
        capture_process.join(timeout=5)
        pid_process.join(timeout=5)
       
        # Force terminate if still alive
        if capture_process.is_alive():
            capture_process.terminate()
        if pid_process.is_alive():
            pid_process.terminate()
        
        # Exit GUI
        #app.join_threads()
        #sleep(1)
        #app.destroy()