import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
user_input = int(input("Enter 1/0 to start/quit the program: "))
if user_input == 1:
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # We store hand data here: {'Left': [[id, x, y]...], 'Right': [[id, x, y]...]}
        all_hands_data = {}

        if results.multi_hand_landmarks:
            # results.multi_handedness tells us if it's the Left or Right hand
            for hand_idx, hand_info in enumerate(results.multi_handedness):
                hand_label = hand_info.classification[0].label  # "Left" or "Right"
                hand_lms = results.multi_hand_landmarks[hand_idx]

                lmList = []
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([cx, cy])

                all_hands_data[hand_label] = lmList
                mpDraw.draw_landmarks(img, hand_lms, mpHands.HAND_CONNECTIONS)

            # --- INTER-HAND DETECTION ---
            # Check if both hands are in the frame
            if "Left" in all_hands_data and "Right" in all_hands_data:
                # Index tip for Left hand
                l_index_x, l_index_y = all_hands_data["Left"][4]
                l1_index_x, l1_index_y = all_hands_data["Left"][8]
                l2_index_x, l2_index_y = all_hands_data["Right"][12]
                l3_index_x, l3_index_y = all_hands_data["Right"][16]
                l4_index_x, l4_index_y = all_hands_data["Left"][20]
                # Index tip for Right hand
                r_index_x, r_index_y = all_hands_data["Right"][4]
                r1_index_x, r1_index_y = all_hands_data["Right"][8]
                r2_index_x, r2_index_y = all_hands_data["Right"][12]
                r3_index_x, r3_index_y = all_hands_data["Right"][16]
                r4_index_x, r4_index_y = all_hands_data["Right"][20]

                # Calculate distance between the two index fingers
                dist_thumb = math.hypot(r_index_x - l_index_x, r_index_y - l_index_y) # DISTANCE BETWEEN THE THUMB 1 AND THUMB 2
                dist_thumb_index = math.hypot(r1_index_x - l_index_x, r1_index_y - l_index_y)# max distance
                dist_thumb_middle = math.hypot(r2_index_x - l_index_x, r2_index_y - l_index_y)
                dist_thumb_ring = math.hypot(r3_index_x - l_index_x, r3_index_y - l_index_y)
                dist_thumb_pinky = math.hypot(r4_index_x - l_index_x, r4_index_y - l_index_y)
                dist_index = math.hypot(r1_index_x - l1_index_x, r1_index_y - l1_index_y)# min distance
                dist_middle = math.hypot(r2_index_x - l2_index_x, r2_index_y - l2_index_y)
                dist_ring = math.hypot(r3_index_x - r3_index_x, r3_index_y - r3_index_y)
                dist_pinky = math.hypot(r4_index_x - r4_index_x, r4_index_y - r4_index_y)

                if (dist_thumb < 30) and (dist_index < 30) and (dist_ring < 30) and (dist_pinky < 30) and (dist_middle < 30) and (dist_thumb_index >= 30) and (dist_thumb_middle >= 30) and (dist_thumb_ring >= 30) and (dist_thumb_pinky >= 30):
                    cv2.putText(img, "You have the best heart!", (150, 50),
                                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                    # Draw a spark or line between them
                    cv2.line(img, (l_index_x, l_index_y), (r_index_x, r_index_y), (255, 255, 255), 5)
                    cv2.line(img, (l1_index_x, l1_index_y), (r1_index_x, r1_index_y), (255, 0, 0), 5)
                    cv2.line(img, (l2_index_x, l2_index_y), (r2_index_x, r2_index_y), (0, 255, 0), 5)
                    cv2.line(img, (l3_index_x, l3_index_y), (r3_index_x, r3_index_y), (0, 0, 255), 5)
                    cv2.line(img, (l4_index_x, l4_index_y), (r4_index_x, r4_index_y), (0, 0, 255), 5)

        cv2.imshow("Make a heart with your fingers :D", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    cv2.destroyAllWindows()
