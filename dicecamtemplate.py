import cv2

scale_factor = 10.0
last_x, last_y, last_w, last_h = None, None, None, None

def close_windows_on_esc(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.destroyAllWindows()

cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", close_windows_on_esc)

# Open the webcam
cap = cv2.VideoCapture(2)

# Capture background image
ret, bg_frame = cap.read()
bg_gray = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the frame to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)


    # Apply thresholding to the frameqqqq
    # ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)


    # Find contours in the thresholded frame
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x,y,w,h = 0, 0, 0, 0
    if len(contours) > 0:
        # Sort the contours by area, so that the largest contour will be selected
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Select the largest contour
        die_contour = contours[0]

        # Get the bounding box of the die contour
        x, y, w, h = cv2.boundingRect(die_contour)

        # check if the position and size are close to the last frame
        if last_x and abs(x-last_x) < 20 and abs(y-last_y) < 20 and abs(w-last_w) < 20 and abs(h-last_h) < 20:
            # Expand the ROI by the scale factor
            x = int(x - (w * (scale_factor - 1) / 2))
            y = int(y - (h * (scale_factor - 1) / 2))
            w = int(w * scale_factor)
            h = int(h * scale_factor)
            # Make sure that the bounding box is inside the frame
            x, y, w, h = (x, y, w, h) if x>0 and y>0 and w>0 and h>0 else (0, 0, 0, 0)
            # Crop the frame to the expanded ROI
            roi = frame[y:y+h, x:x+w]
            if x > 0 and y > 0 and w > 0 and h > 0:
                cv2.imshow("ROI", roi)
            last_x, last_y, last_w, last_h = x, y, w, h
    # Draw the bounding box around the die
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Show the webcam frame
    cv2.imshow("Webcam", frame)

    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
cap.release()

# Close all windows
cv2.destroyAllWindows()
