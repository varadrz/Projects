import cv2
import numpy as np
import time

def hello(x):
    pass

cap = cv2.VideoCapture(0)

# Capture in HD but display in small size
cap.set(3, 1280)
cap.set(4, 720)
time.sleep(2)

cv2.namedWindow("bars")
cv2.createTrackbar("upper_hue", "bars", 110, 180, hello)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, hello)
cv2.createTrackbar("upper_value", "bars", 255, 255, hello)
cv2.createTrackbar("lower_hue", "bars", 68, 180, hello)
cv2.createTrackbar("lower_saturation", "bars", 55, 255, hello)
cv2.createTrackbar("lower_value", "bars", 54, 255, hello)

print("Capturing background... Step out of frame")
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

print("Adjust sliders until only your green towel is detected.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)

    # Work on HD frame, then shrink only for display
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    u_h = cv2.getTrackbarPos("upper_hue", "bars")
    u_s = cv2.getTrackbarPos("upper_saturation", "bars")
    u_v = cv2.getTrackbarPos("upper_value", "bars")
    l_h = cv2.getTrackbarPos("lower_hue", "bars")
    l_s = cv2.getTrackbarPos("lower_saturation", "bars")
    l_v = cv2.getTrackbarPos("lower_value", "bars")

    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask[:frame.shape[0]//3, :] = 0

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    inverse_mask = cv2.bitwise_not(mask)
    res1 = cv2.bitwise_and(frame, frame, mask=inverse_mask)
    res2 = cv2.bitwise_and(background, background, mask=mask)
    final = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Resize only for display (keeps processing quality high)
    display_final = cv2.resize(final, (640, 360))
    display_mask = cv2.resize(mask, (640, 360))

    cv2.imshow("Mask", display_mask)
    cv2.imshow("Invisibility Cloak", display_final)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
