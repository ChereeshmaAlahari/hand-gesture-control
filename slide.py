import cv2
import mediapipe as mp
import pyautogui
import time


# Initialize MediaPipe Hands module.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam setup.
cap = cv2.VideoCapture(0)

# Variables for gesture detection.
prev_x = 0
prev_y = 0
gesture_delay = 2  # Delay between gestures (seconds).
last_gesture_time = time.time()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally for a mirror-like effect.
    
    # Convert the image to RGB for MediaPipe processing.
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the wrist (landmark 0).
            h, w, _ = img.shape
            wrist_x = int(hand_landmarks.landmark[0].x * w)
            wrist_y = int(hand_landmarks.landmark[0].y * h)

            # Calculate the horizontal movement (swipe).
            if prev_x != 0:
                movement_x = wrist_x - prev_x

                # Detect a swipe gesture.
                if movement_x > 50 and time.time() - last_gesture_time > gesture_delay:
                    print("Swiped Right - Next Slide")
                    pyautogui.press('right')  # Simulate "Next Slide"
                    last_gesture_time = time.time()
                elif movement_x < -50 and time.time() - last_gesture_time > gesture_delay:
                    print("Swiped Left - Previous Slide")
                    pyautogui.press('left')  # Simulate "Previous Slide"
                    last_gesture_time = time.time()

            prev_x = wrist_x
            prev_y = wrist_y

    # Display the webcam feed with landmarks.
    cv2.imshow('Slide Control with Hand Gestures', img)

    # Break the loop when 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy windows.
cap.release()
cv2.destroyAllWindows()