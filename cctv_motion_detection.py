import cv2
from datetime import datetime

# Function to detect movement and save frames to a video file
def detect_and_save_movement():
    # Capture video from the camera
    cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to a video file

    # Initialize variables
    first_frame = None
    motion_detected = False
    motion_start_time = None
    motion_frames = []

    while True:
        # Read frame-by-frame
        ret, frame = cap.read()

        # If frame is not received, continue
        if not ret:
            continue

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur the grayscale image to remove noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Store the first frame
        if first_frame is None:
            first_frame = gray
            continue

        # Compute absolute difference between current frame and the first frame
        frame_delta = cv2.absdiff(first_frame, gray)

        # Apply thresholding to the delta image
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours of the thresholded image
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check each contour
        for contour in contours:
            # Ignore small contours
            if cv2.contourArea(contour) < 1000:
                continue

            # Motion detected
            motion_detected = True

            # Save the current frame and surrounding frames
            if motion_start_time is None:
                motion_start_time = datetime.now().strftime('%Y%m%d%H%M%S')

            # Append the frame and its grayscale version
            motion_frames.append((frame.copy(), gray.copy()))

        # Display the frame
        cv2.imshow('CCTV Feed', frame)

        # Update first frame for the next iteration
        first_frame = gray

        # Save detected frames to a video file if motion was detected
        if motion_detected:
            save_motion_frames(motion_frames, motion_start_time)
            motion_frames = []  # Clear the frames list
            motion_detected = False  # Reset motion detection flag

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close windows
    cap.release()
    cv2.destroyAllWindows()

def save_motion_frames(frames, start_time):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'motion_detected_{start_time}.avi', fourcc, 20.0, (640, 480))

    # Write each frame to the video file
    for color_frame, gray_frame in frames:
        out.write(color_frame)

    # Release the VideoWriter object
    out.release()

# Call the function to detect movement and save frames to a video file
detect_and_save_movement()
