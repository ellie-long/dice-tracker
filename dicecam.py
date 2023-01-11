import cv2

# Load the templates for each number
templates = []
for i in range(1,20):
    template = cv2.imread(f"template_{i}.jpg", cv2.IMREAD_GRAYSCALE)
    templates.append(template)

# Open a connection to the webcam
cap = cv2.VideoCapture(2)

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to make the numbers more visible
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over the contours and find the contour with the best match to the templates
    best_match = None
    best_match_val = float("inf")
    for contour in contours:
        for i, template in enumerate(templates):
            match = cv2.matchShapes(template, contour, cv2.CONTOURS_MATCH_I1, 0.0)
            if match < best_match_val:
                best_match = i+1
                best_match_val = match

    # If a match was found, draw the number on the frame
    if best_match is not None:
        x,y,w,h = cv2.boundingRect(contours[best_match])
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, str(best_match), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    # Display the frame
    cv2.imshow("Dice recognition", frame)

    # Exit if the user presses 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
