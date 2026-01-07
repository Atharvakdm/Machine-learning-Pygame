import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
#Loading image
overlay_img = cv2.imread("monkey-think.jpg")
# Resize it so it's not huge (e.g., 100x100 pixels)
overlay_img = cv2.resize(overlay_img, (100, 100))
img_h, img_w, _ = overlay_img.shape

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Default color: Green (BGR format)
    drawColor = (0, 255, 0)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # We need to get the pixel coordinates for points 4 and 8
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                #id is the id number to identify each finger, while lm is the landmark which refers to the finger. lm contains x,y and z.
                h, w, c = img.shape
                #img.shape gets the size of your webcam video.
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                # appending the id, x and the y coordinate of the finger in real-time to the list.

            if len(lmList) != 0:
                # Coordinate of Thumb tip (4) and Index tip (8)
                # coordinates:
                # pinky finger (20), ring finger (16), Middle finger is (12)
                x1, y1 = lmList[4][1], lmList[4][2] # thumb
                x2, y2 = lmList[8][1], lmList[8][2] # index
                x3, y3 = lmList[12][1], lmList[12][2] # middle
                x4, y4 = lmList[16][1], lmList[16][2] # ring
                x5, y5 = lmList[4][1], lmList[4][2] # pinky
                # Calculate the distance
                distance1 = math.hypot(x2 - x1, y2 - y1) #pointing finger
                distance2 = math.hypot(x3 - x2, y3 - y2) #close fingers
                distance3 = math.hypot(x4 - x3, y4 - y3)
                distance4 = math.hypot(x5 - x4, y5 - y4)
                #checking if each of the distances between the fingers is close enough to the thumb finger. like an eye.
                # If distance is less than 30 pixels, change color to Pink!
                if (distance2 < 70) and (distance3 < 70) and (distance4 < 70):
                    drawColor = (255, 0, 255)
                    # --- NEW: Overlay the image near your hand ---
                    # We define the region where we want to put the meme
                    y_offset = y1 - 120
                    x_offset = x1 - 50
                    # Pink in BGR
                    # 1. THE TEXT COMMAND
                    # Parameters: (image, text, position, font, scale, color, thickness)
                    cv2.putText(img, "!", (x1, y1 - 40),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 4)
                    if y_offset > 0 and x_offset > 0:
                        img[y_offset:y_offset + img_h, x_offset:x_offset + img_w] = overlay_img
                else:
                    drawColor = (0, 255, 0) # Green in BGR
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS,
                                 mpDraw.DrawingSpec(color=drawColor, thickness=2, circle_radius=2),
                                 mpDraw.DrawingSpec(color=drawColor, thickness=2))

    cv2.imshow("Monkey!", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
