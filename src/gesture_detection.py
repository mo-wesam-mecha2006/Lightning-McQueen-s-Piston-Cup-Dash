import cv2
from ultralytics import YOLO

# Load trained YOLO model
model = YOLO("models/best.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Real-time detection
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Run YOLO detection
    results = model(frame, conf=0.5)

    # Draw detections
    annotated_frame = results[0].plot()

    # Display result
    cv2.imshow("YOLO Hand Gesture Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()