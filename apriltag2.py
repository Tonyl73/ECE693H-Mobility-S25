import cv2
import numpy as np
from pupil_apriltags import Detector
import math
import time

def rotation_matrix_to_euler_angles(R):
    sy = math.sqrt(R[0, 0]**2 + R[1, 0]**2)
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])  # Roll
        y = math.atan2(-R[2, 0], sy)      # Pitch
        z = math.atan2(R[1, 0], R[0, 0])  # Yaw
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.degrees([x, y, z])  # Convert to degrees

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

detector = Detector(families="tag36h11")
last_print_time = time.time()

cv2.namedWindow('AprilTag Detection', cv2.WINDOW_NORMAL)  # Force window creation

while True:
    #make sure camera feed is being captured
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray, estimate_tag_pose=True, camera_params=(600, 600, 320, 240), tag_size=0.065)
    current_time = time.time()

    detection_info = []  #empty array to store multiple april tag detections

    #this stuff is just kinda part of the april tags library
    for detection in detections:
        corners = detection.corners.astype(int)
        center_x, center_y = np.mean(corners, axis=0).astype(int)

        if detection.pose_R is not None:
            euler_angles = rotation_matrix_to_euler_angles(np.array(detection.pose_R))
            
            #store all detected tags into array from before
            detection_info.append(
                f"Tag ID: {detection.tag_id}, X: {center_x}, Y: {center_y}, "
                f"Yaw: {euler_angles[2]:.2f}, Pitch: {euler_angles[1]:.2f}, Roll: {euler_angles[0]:.2f}"
            )

            #draw orientation info on the frame
            cv2.putText(frame, f"Yaw: {euler_angles[2]:.1f}", (center_x, center_y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Pitch: {euler_angles[1]:.1f}", (center_x, center_y + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(frame, f"Roll: {euler_angles[0]:.1f}", (center_x, center_y + 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        #draw lines around detected tag
        cv2.polylines(frame, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

        #display the tag id
        cv2.putText(frame, f"ID {detection.tag_id}", (center_x, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #print the information every x seconds
    x = 0.5
    if current_time - last_print_time >= x and detection_info:
        print("\nDetected AprilTags:")
        for tag in detection_info:
            print(tag)
        last_print_time = current_time  # Reset timer
    
    cv2.imshow('AprilTag Detection', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
