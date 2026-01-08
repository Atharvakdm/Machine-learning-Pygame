import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Create a blank canvas
canvas = np.zeros((480, 640, 3), np.uint8)
px, py = 0, 0  # Previous coordinates

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Fix the inversion!
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            if len(lmList) != 0:
                # We use Point 8 (Index Finger Tip)
                x1, y1 = lmList[8][1], lmList[8][2]

                # If this is the first frame, set previous = current
                if px == 0 and py == 0:
                    px, py = x1, y1

                # DRAWING LOGIC:
                # Draw a line on the CANVAS from previous (px, py) to current (x1, y1)
                cv2.line(canvas, (px, py), (x1, y1), (255, 0, 255), 5)

                # Update previous coordinates for the next frame
                px, py = x1, y1
    else:
        # If no hand is detected, reset previous points so we don't
        # get a giant line jumping across the screen when the hand reappears
        px, py = 0, 0

    # COMBINE: Add the canvas onto the webcam image
    # Basically, anywhere the canvas isn't black, show the canvas color
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    cv2.imshow("Virtual Painter", img)

    # Press 'c' to clear the canvas
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('c'):
        canvas = np.zeros((480, 640, 3), np.uint8)

cap.release()
cv2.destroyAllWindows()
