import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Variables to store previous positions and time for hover detection
prev_x, prev_y = 0, 0
hover_start_time = None
hover_duration = 2  # seconds
tolerance = 35  # pixels

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the index finger tip and middle finger tip positions
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Convert the coordinates to screen space
            h, w, _ = img.shape
            index_x = int(index_finger_tip.x * w)
            index_y = int(index_finger_tip.y * h)
            middle_x = int(middle_finger_tip.x * w)
            middle_y = int(middle_finger_tip.y * h)

            # Flip the x-coordinates to match the real hand gesture
            screen_x = screen_width - (index_x / w) * screen_width
            screen_y = (index_y / h) * screen_height

            # Check if the cursor is hovering in the same position within the tolerance range
            if abs(screen_x - prev_x) < tolerance and abs(screen_y - prev_y) < tolerance:
                if hover_start_time is None:
                    hover_start_time = time.time()
                elif time.time() - hover_start_time > hover_duration:
                    pyautogui.click()
                    hover_start_time = None  # Reset hover start time after clicking
            else:
                hover_start_time = None  # Reset hover start time if the cursor moves

            prev_x, prev_y = screen_x, screen_y

            # Move the cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Draw circles at the index and middle finger tips
            cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (middle_x, middle_y), 10, (0, 0, 255), cv2.FILLED)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()