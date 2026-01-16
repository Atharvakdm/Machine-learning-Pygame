import cv2
import mediapipe as mp
import time

#code for inverted camera

cap = cv2.VideoCapture(0) # setting up the camera

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=5) #check what parameters are required: min_detection, min_tracking

while True:
    success, img = cap.read() #getting the frame
    #flipping the camera
    img = cv2.flip(img, 1)
    #converting the color of the environment to RGB in real-time
    imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #cvtcolor refers to convert color, and we are converting it to RGB
    # processing the frames
    results = hands.process(imgRBG)
    print(results.multi_hand_landmarks) #multi_land_handmarks checks if the hand is detected or not

    cv2.imshow('camera-frame', img)
    cv2.waitKey(1)
