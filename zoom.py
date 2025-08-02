import cv2
import mediapipe as mp
import math
import pyautogui

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the MediaPipe Hands module
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Open a webcam feed
cap = cv2.VideoCapture(0)

def calculate_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Previous distance to keep track of zoom gesture
prev_distance = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    # Convert image back to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get landmarks for index and thumb tips
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Calculate distance between thumb tip and index tip
            distance = calculate_distance(thumb_tip, index_tip)
            
            # Zoom in or out based on distance
            if prev_distance is not None:
                if distance > prev_distance + 0.02:  # Adjust threshold as needed
                    pyautogui.hotkey('ctrl', '+')  # Simulate Ctrl + to zoom in
                elif distance < prev_distance - 0.02:  # Adjust threshold as needed
                    pyautogui.hotkey('ctrl', '-')  # Simulate Ctrl - to zoom out
            
            # Update previous distance
            prev_distance = distance

    else:
        # Reset previous distance if no hands are detected
        prev_distance = None

    # Show the video feed
    cv2.imshow('Hand Gesture Zoom', image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()