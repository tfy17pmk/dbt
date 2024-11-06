import cv2 as cv
import numpy as np
import time

class Camera:
	def __init__(self):
		# Open webcam and check that it is opened
		self.cam = cv.VideoCapture(0)  # 0 for laptop webcam, 1 for external webcam

        # Set the resolution to 640x480
		self.cam.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
		self.cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
		self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
		self.cam.set(cv.CAP_PROP_FPS, 90)
		self.cam.set(cv.CAP_PROP_AUTOFOCUS, 0)
		self.crop_x1 = 190
		self.crop_y1 = 120
		self.crop_x2 = 490
		self.crop_y2 = 395
		if not self.cam.isOpened():
			print("Error: Cannot open camera. Exiting.")
			exit()

        # Initialize color thresholds (orange and white)
		self.lower_orange = np.array([5, 100, 100]) 
		self.upper_orange = np.array([15, 255, 255])
		self.lower_white = np.array([0, 0, 200])
		self.upper_white = np.array([180, 25, 255])

        # For calculating FPS
		self.last_time = time.time()
		self.frame_count = 0

	def get_frame(self):
		return_value, frame = self.cam.read()
		if not return_value:
			print("Error: Can't receive frame. Exiting.")
			return None
		return frame
    
	def crop_frame(self, frame):
		cropped_frame = frame[self.crop_y1:self.crop_y2, self.crop_x1:self.crop_x2]
		return cropped_frame

	def get_masked_frame(self):
		return_value, frame = self.cam.read()
		frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		# Create binary masks for orange and white balls
		mask_orange = cv.inRange(frame_hsv, self.lower_orange, self.upper_orange)
		mask_white = cv.inRange(frame_hsv, self.lower_white, self.upper_white)

		# Combine masks
		mask = cv.bitwise_or(mask_orange, mask_white)

		# Morphological operations to improve mask
		kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
		mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)  # Remove small blobs
		mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) # Close gaps in detected objects

		if not return_value:
			print("Error: Can't receive mask_frame. Exiting.")
			return None
		return mask


	def show_frame(self, frame):
			# Calculate FPS
		self.frame_count += 1
		current_time = time.time()
		total_time = current_time - self.last_time
		fps = int(self.frame_count/total_time)
		self.frame_count = 0
		self.last_time = current_time

		# Overlay FPS on the frame
		cv.putText(frame, f'FPS: {fps}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

		cv.imshow("Display window", frame)
		if cv.waitKey(1) == ord('q'):
			return True
		return False

	def get_ball(self, frame):
		# Convert frame to HSV
		frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		# Create binary masks for orange and white balls
		mask_orange = cv.inRange(frame_hsv, self.lower_orange, self.upper_orange)
		mask_white = cv.inRange(frame_hsv, self.lower_white, self.upper_white)

		# Combine masks
		mask = cv.bitwise_or(mask_orange, mask_white)

		# Apply Gaussian blur to reduce noise
		mask = cv.GaussianBlur(mask, (5, 5), 0)

		# Morphological operations to improve mask
		kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
		mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)  # Remove small blobs
		mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) # Close gaps in detected objects

		# Find contours
		contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

		if contours:
			# Filter contours by area and circularity to identify round objects
			for contour in contours:
				area = cv.contourArea(contour)
				perimeter = cv.arcLength(contour, True)

				# Skip small areas to reduce noise
				if area > 200 and perimeter > 0:
					# Calculate circularity
					circularity = 4 * np.pi * area / (perimeter * perimeter)
					if 0.7 < circularity <= 1.0:  # Can try to adjust
						# Find the smallest enclosing circle, draw a circle around detected object
						(x, y), radius = cv.minEnclosingCircle(contour)
						cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

                        # Change coordinate system
						height, width, _ = frame.shape
						x -= (width / 2) - 3
						y -= (height / 2) -2
						y = -y
						return int(x), int(y), int(area)

		return -1, -1, 0

	def clean_up_cam(self):
		self.cam.release()
		cv.destroyAllWindows()
		


# Usage example
"""if __name__ == "__main__":
    camera = Camera()
    while True:
        frame = camera.get_frame()
        if frame is not None:
            ball_coordinates = camera.get_ball(frame)
            if ball_coordinates[0] != -1:
                print(f"Ball detected at coordinates: {ball_coordinates[:2]}, Area: {ball_coordinates[2]}")
            camera.show_frame(frame)
        else:
            break

    camera.clean_up_cam()"""