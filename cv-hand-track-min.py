import cv2
import mediapipe as mp
import time

#code for inverted camera

cap = cv2.VideoCapture(0) # setting up the camera

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=5) #check what parameters are required: min_detection, min_tracking
mpDraw = mp.solutions.drawing_utils

prev_time = 0
current_time = 0

while True:
    success, img = cap.read() #getting the frame
    #flipping the camera
    img = cv2.flip(img, 1)
    #converting the color of the environment to RGB in real-time
    imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #cvtcolor refers to convert color, and we are converting it to RGB
    # processing the frames
    results = hands.process(imgRBG)
    print(results.multi_hand_landmarks) #multi_land_handmarks checks if the hand is detected or not
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: #checking each hand in the result
            for id, lm in enumerate(handLms.landmark): #giving an index number (0, 1, ....n) to each hand landmark
                # print(id, lm)
                h, w, c = img.shape #height, width and channel of determining the pixel size.
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # if id == 0 or id == 4 or id == 7 or id == 8:
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #drawing the dots and connections

    current_time = time.time() # that's how you access the real current time
    fps = 1/(current_time - prev_time)
    prev_time = current_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

    cv2.imshow('camera-frame', img)
    cv2.waitKey(1)
