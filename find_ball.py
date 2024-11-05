import cv2 as cv
import numpy as np
import time

videoCapture = cv.VideoCapture(0)
videoCapture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('H', '2', '6', '4'))
videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
videoCapture.set(cv.CAP_PROP_FPS, 90)
print(videoCapture.get(cv.CAP_PROP_FPS))

# Initial time for FPS calculation
prev_frame_time = 0

while True:
    # Capture the current time
    new_frame_time = time.time()

    # Read the frame from the video source
    ret, frame = videoCapture.read()
    if not ret:
        break

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
            if 0.85 < circularity <= 1.15 and radius > 10:  # Adjust threshold as needed
                center = (int(x), int(y))
                radius = int(radius)
                cv.circle(frame, center, radius, (0, 255, 0), 2)  # Green circle around detected ball
                cv.circle(frame, center, 3, (0, 0, 255), -1)  # Red dot at the center

    # Calculate FPS
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Convert the FPS to an integer and display it on the frame
    fps_text = f"FPS: {int(fps)}"
    cv.putText(frame, fps_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv.imshow("Circles with FPS", frame)

    # Break on 'q' key press
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
videoCapture.release()
cv.destroyAllWindows()
