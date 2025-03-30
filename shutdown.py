import cv2
import mediapipe as mp
import pyautogui
import os




mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip horizontally for a mirrored view
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Drawing hand landmarks (optional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the landmarks
            thumb_tip = hand_landmarks.landmark[4]   # Thumb tip
            index_tip = hand_landmarks.landmark[8]   # Index finger tip
            pinky_tip = hand_landmarks.landmark[20]  # Pinky finger tip

            # Logic to detect an open palm
            if thumb_tip.y < index_tip.y and pinky_tip.y < index_tip.y:
                # If thumb and pinky are both above the index finger, likely an open palm
                print("Open palm detected, shutting down...")
                os.system("shutdown /s /t 1")  # Trigger shutdown for Windows
                break

    # Display the frame
    cv2.imshow("Hand Gesture Recognition", frame)

    # Break loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

