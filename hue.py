import numpy as np
import cv2

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lower_purple = np.array([90, 50, 50])
        upper_purple = np.array([170, 255, 255])
        mask = cv2.inRange(hsv, lower_purple, upper_purple)

        ret, thresh = cv2.threshold(v, 180, 255, cv2.THRESH_BINARY)

        final_mask = cv2.bitwise_and(mask, thresh)

        cv2.imshow("Hue channel", h)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
