import cv2 as cv
import numpy as np
import time

class FindBall:
    def __init__(self):
        
        self.videoCapture = cv.VideoCapture(0)
        self.videoCapture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        self.videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        self.videoCapture.set(cv.CAP_PROP_FPS, 90)
        self.crop_x1 = 190
        self.crop_y1 = 120
        self.crop_x2 = 490
        self.crop_y2 = 395

        print(self.videoCapture.get(cv.CAP_PROP_FPS))

        # Initial time for FPS calculation
        self.prev_frame_time = 0

    def get_frame(self):
        # Read the frame from the video source
        ret, frame = self.videoCapture.read()
        if not ret:
            print("none frame")
            return None
        return frame

    def crop_frame(self, frame):
        cropped_frame = frame[self.crop_y1:self.crop_y2, self.crop_x1:self.crop_x2]
        return cropped_frame

    
    def get_ball(self, frame):
        grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grayFrame = cv.equalizeHist(grayFrame)
        edges = cv.Canny(grayFrame, 50, 150)

        contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Loop over contours and filter for circular shapes
        for contour in contours:
            # Approximate the contour to a circle
            ((x, y), radius) = cv.minEnclosingCircle(contour)
            
            # Calculate area and perimeter to filter non-circular shapes
            area = cv.contourArea(contour)
            perimeter = cv.arcLength(contour, True)

            # Check if the contour is approximately circular
            if area > 0 and perimeter > 0:
                circularity = 4 * np.pi * (area / (perimeter ** 2))
                if 0.75 < circularity <= 1.3 and radius > 3:  # Adjust threshold as needed
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv.circle(frame, center, radius, (0, 255, 0), 2)  # Green circle around detected ball
                    cv.circle(frame, center, 3, (0, 0, 255), -1)  # Red dot at the center
                    return int(x), int(y)
        return -1, -1, 0
    
    def show_frame(self, frame):
        # Capture the current time
        new_frame_time = time.time()
        # Calculate FPS
        fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time

        # Convert the FPS to an integer and display it on the frame
        fps_text = f"FPS: {int(fps)}"
        cv.putText(frame, fps_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv.imshow("Circles with FPS", frame)
        if cv.waitKey(1) == ord('q'):
            return True
        return False

    def clean_up_cam(self):
        # Release resources
        self.videoCapture.release()
        cv.destroyAllWindows()

# Usage example
if __name__ == "__main__":
    camera = FindBall()
    while True:
        # Read the frame from the video source
        frame = camera.get_frame()
        cropped_frame = camera.crop_frame(frame)
        if cropped_frame is not None:
            xy_coordinates = camera.get_ball(cropped_frame)
            if xy_coordinates[0] != -1:
                print(f"Coordinates: x: {xy_coordinates[0]}, y: {xy_coordinates[1]}")
            camera.show_frame(cropped_frame)
        else:
            camera.clean_up_cam()
            break

        # Break on 'q' key press
        if cv.waitKey(1) & 0xFF == ord("q"):
            camera.clean_up_cam()
            break