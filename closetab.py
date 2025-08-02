import cv2
import mediapipe as mp
import time
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Capture video from webcam
cap = cv2.VideoCapture(0)

def is_single_hand_cross_gesture(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calculate the distance between the tips of the index and middle fingers
    distance_tips = ((index_finger_tip.x - middle_finger_tip.x) ** 2 + (index_finger_tip.y - middle_finger_tip.y) ** 2) ** 0.5

    # Adjust the threshold as needed for detecting the crossing gesture
    return distance_tips < 0.05

def is_two_hands_x_gesture(hand_landmarks1, hand_landmarks2):
    index_finger_tip_1 = hand_landmarks1.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_tip_2 = hand_landmarks2.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Calculate the distance between the tips of index fingers of both hands
    distance_tips = ((index_finger_tip_1.x - index_finger_tip_2.x) ** 2 + (index_finger_tip_1.y - index_finger_tip_2.y) ** 2) ** 0.5

    # Adjust the threshold as needed for detecting the crossing gesture
    return distance_tips < 0.1

def close_current_tab():
    # Simulate pressing Ctrl+W to close the current tab
    pyautogui.hotkey('ctrl', 'w')
    print("Tab closed")

def close_current_application():
    # Simulate pressing Alt+F4 to close the current application window
    pyautogui.hotkey('alt', 'f4')
    print("Application window closed")

GESTURE_DETECTION_DELAY = 1  # seconds
last_gesture_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand_landmarks1 = result.multi_hand_landmarks[0]

        # Drawing hand landmarks (optional)
        mp_drawing.draw_landmarks(frame, hand_landmarks1, mp_hands.HAND_CONNECTIONS)

        if len(result.multi_hand_landmarks) == 2:
            hand_landmarks2 = result.multi_hand_landmarks[1]
            mp_drawing.draw_landmarks(frame, hand_landmarks2, mp_hands.HAND_CONNECTIONS)

            if is_two_hands_x_gesture(hand_landmarks1, hand_landmarks2):
                current_time = time.time()
                if (current_time - last_gesture_time) > GESTURE_DETECTION_DELAY:
                    print("X gesture detected. Closing current application window...")
                    close_current_application()
                    last_gesture_time = current_time

        if is_single_hand_cross_gesture(hand_landmarks1):
            current_time = time.time()
            if (current_time - last_gesture_time) > GESTURE_DETECTION_DELAY:
                print("Single hand cross gesture detected. Closing tab...")
                close_current_tab()
                last_gesture_time = current_time

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Check if the window has been closed
    if cv2.getWindowProperty('Hand Tracking', cv2.WND_PROP_VISIBLE) < 1:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()