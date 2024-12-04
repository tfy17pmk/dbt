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
        self.square_coords = [(-68, -71), (68, -71), (68, 71), (-68, 71), (-68, -71)]
        self.triangle_coords = [(0, -71), (-68, 71), (68, 71), (0, -71)]
        self.hexagon_coords = [(108, 0), (54, 98), (-54, 98), (-108, 0), (-54, -98), (54, -98), (108, 0)]


    def run_pattern(self):
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

    def reset_data(self):
        while not self.data_queue.empty():
            self.data_queue.get_nowait()
        
        self.mapped_points = []
        self.send_goal_pos(0, 0)
        self.join_threads()

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