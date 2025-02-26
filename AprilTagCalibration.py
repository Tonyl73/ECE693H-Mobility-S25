import cv2
import numpy as np
from apriltag import apriltag

# Initialize the camera feed (0 refers to the default camera)
cap = cv2.VideoCapture(0)

# Initialize the AprilTag detector
detector = apriltag("tag36h11")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Convert the frame to grayscale (as AprilTag detection works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags in the frame
    detections = detector.detect(gray)

    # Draw the detected tags on the frame
    for detection in detections:
        # Get the corners of the detected tag from 'lb-rb-rt-lt'
        corners = np.array(detection['lb-rb-rt-lt'], dtype=int)

        # Draw lines around the detected tag
        cv2.polylines(frame, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

        # Optionally: display the tag ID in the center of the tag
        tag_id = detection['id']
        center = tuple(np.mean(corners, axis=0).astype(int))
        cv2.putText(frame, str(tag_id), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the resulting frame with detected AprilTags
    cv2.imshow('AprilTag Detection', frame)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
