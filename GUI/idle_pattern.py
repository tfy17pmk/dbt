import math
import threading
import time
from multiprocessing import Queue

class IdlePatterns:
    def __init__(self, resources):
        self.goal_position_queue = resources.goal_position_queue
        self.data_queue = Queue(maxsize=500)
        self.stop_event = threading.Event()
        self.prev_goal_pos = (0, 0)
        self.next_pattern = "triangle"
        self.pattern_delay = 3
        self.square_coords = [(-60, -63), (60, -63), (60, 63), (-60, 63), (-60, -63), (0, 0)]
        self.triangle_coords = [(0, -63), (-60, 63), (60, 63), (0, -63), (0, 0)]
        self.hexagon_coords = [(100, 0), (46, 90), (-46, 90), (-100, 0), (-46, -90), (46, -90), (100, 0), (0, 0)]


    def run_pattern(self):
        # initialize first idle pattern
        [self.data_queue.put((x,y)) for x, y in self.triangle_coords]
        # start thread
        self.start_thread()

    def start_thread(self):
        self.stop_event.clear()
        if not hasattr(self, 'thread'):
            self.thread = threading.Thread(target=self.send_data)
            self.thread.start()

    def join_threads(self):
        self.stop_event.set()
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
            del self.thread  # Remove the thread attribute
            while not self.data_queue.empty():
                self.data_queue.get_nowait()
            while not self.goal_position_queue.empty():
                self.goal_position_queue.get_nowait()
            self.send_goal_pos(0, 0)


    def reset_data(self, event=None):
        
        self.next_pattern = "square"
        self.join_threads()

    def custom_sleep(self):
        """
        Sleep for `duration` seconds, but allow interruption by `stop_event`.
        """
        start_time = time.time()
        while time.time() - start_time < self.pattern_delay:
            if self.stop_event.is_set():
                break  # Exit early if the stop event is set
            time.sleep(0.1)  # Sleep in small increments


    def send_data(self):
        while not self.stop_event.is_set():
            try:
                if not self.data_queue.empty():
                    coordinates = self.data_queue.get_nowait()
                    
                    dist = math.sqrt((self.prev_goal_pos[0] - coordinates[0]) ** 2 + (self.prev_goal_pos[1] - coordinates[1]) ** 2)
                    delay = abs((dist/80))
                    self.send_goal_pos(coordinates[0], coordinates[1])
                    self.prev_goal_pos = coordinates
                    time.sleep(delay)
                elif self.data_queue.empty() and self.next_pattern == "triangle":
                    [self.data_queue.put((x,y)) for x, y in self.triangle_coords]
                    self.next_pattern = "square"
                    self.custom_sleep()
                elif self.data_queue.empty() and self.next_pattern == "square":
                    [self.data_queue.put((x,y)) for x, y in self.square_coords]
                    self.next_pattern = "hexagon"
                    self.custom_sleep()
                elif self.data_queue.empty() and self.next_pattern == "hexagon":
                    [self.data_queue.put((x,y)) for x, y in self.hexagon_coords]
                    self.next_pattern = "triangle"
                    self.custom_sleep()
                
            except Exception as e:
                pass


    def send_goal_pos(self, x, y):
        if not self.goal_position_queue.full():
            try:
                self.goal_position_queue.put((x, y), timeout=0.01)
            except Exception as e:
                print(f"Queue error: {e}")
        else:
            print(f"Queue goal pos is full!")