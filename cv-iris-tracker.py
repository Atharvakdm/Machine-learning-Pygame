import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
mpFaceMesh = mp.solutions.face_mesh
# refine_landmarks=True is necessary for iris tracking
face_mesh = mpFaceMesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imgRGB)

    if results.multi_face_landmarks:
        for face_lms in results.multi_face_landmarks:
            # --- IRIS AND EYE CORNER LANDMARKS ---
            # Right Eye (from camera perspective)
            # 468-472 are iris landmarks
            # 33 and 133 are the corners of the eye
            iris_center = face_lms.landmark[468]
            eye_right_corner = face_lms.landmark[33]
            eye_left_corner = face_lms.landmark[133]

            # Converting to pixel coordinates
            ix, iy = int(iris_center.x * w), int(iris_center.y * h)
            rx, ry = int(eye_right_corner.x * w), int(eye_right_corner.y * h)
            lx, ly = int(eye_left_corner.x * w), int(eye_left_corner.y * h)

            # Calculating the total width of the eye
            total_eye_width = math.hypot(lx - rx, ly - ry)
            # Calculating the distance from iris to the right corner
            iris_to_right = math.hypot(ix - rx, iy - ry)

            # --- GAZE RATIO ---
            # Ratio of 0.5 means center, <0.4 is one side, >0.6 is the other
            ratio = iris_to_right / total_eye_width

            if ratio < 0.42:
                text = "Looking Left"
            elif ratio > 0.58:
                text = "Looking Right"
            else:
                text = "Looking Center"

            cv2.putText(img, f"{text} ({round(ratio, 2)})", (50, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            # Drawing iris center
            cv2.circle(img, (ix, iy), 2, (0, 255, 255), -1)

    cv2.imshow("Iris Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
