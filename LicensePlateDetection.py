import cv2
import numpy as np
import pytesseract
import datetime

# Path to Tesseract executable (change this to your local path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load YOLOv4
net = cv2.dnn.readNetFromDarknet('path/to/yolov4.cfg', 'path/to/yolov4.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Function to perform license plate detection and OCR
def detect_and_ocr(frame):
    height, width, _ = frame.shape

    # YOLOv4 input preprocessing
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Get names of output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Forward pass through network
    outputs = net.forward(output_layers)

    # Processing detections
    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:  # Assuming class 0 is for license plates
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-max suppression to remove redundant overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    plates_info = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, w, h = box

        # Crop the detected plate region
        plate_roi = frame[y:y+h, x:x+w]

        # Perform OCR on the cropped plate region
        gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        plate_text = pytesseract.image_to_string(gray, config='--psm 6').strip()

        # Detect vehicle color
        vehicle_color = detect_vehicle_color(frame, x, y, w, h)

        # Draw rectangle and label on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f'License Plate: {plate_text}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f'Color: {vehicle_color}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Store information for saving to file
        plates_info.append(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} | {plate_text} | {vehicle_color}')

    return frame, plates_info

# Function to detect vehicle color
def detect_vehicle_color(frame, x, y, w, h):
    # Extract the region of interest (ROI) for color detection
    roi = frame[y:y+h, x:x+w]

    # Convert BGR to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Define color ranges for common vehicle colors in HSV
    color_ranges = {
        'black': ([0, 0, 0], [180, 255, 30]),
        'white': ([0, 0, 200], [180, 30, 255]),
        'gray': ([0, 0, 100], [180, 30, 200]),
        'red': ([0, 100, 100], [10, 255, 255]),
        'blue': ([90, 100, 100], [120, 255, 255]),
        'green': ([30, 100, 100], [80, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
    }

    # Detect color
    vehicle_color = 'unknown'
    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)
        if cv2.countNonZero(mask) > 100:  # Adjust this threshold based on lighting conditions
            vehicle_color = color_name
            break

    return vehicle_color

# Function to save detected license plates to a file
def save_to_file(plates_info):
    filename = f"detected_plates_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(filename, 'a') as file:
        for info in plates_info:
            file.write(info + '\n')

    print(f"Detected license plates saved to {filename}")

# Main function to process video feed
def process_video_feed(video_source):
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform license plate detection and OCR
        processed_frame, plates_info = detect_and_ocr(frame)

        # Display the processed frame with license plate information
        cv2.imshow('License Plate Detection', processed_frame)

        # Save detected license plates to a file
        if plates_info:
            save_to_file(plates_info)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Entry point
if __name__ == '__main__':
    # Specify the video source (0 for webcam, or provide a path to a video file)
    video_source = 0  # Change this to your video source (e.g., 'video.mp4')

    # Start capturing and processing the video feed
    process_video_feed(video_source)
