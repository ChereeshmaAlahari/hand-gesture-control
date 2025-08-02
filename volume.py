import cv2
import mediapipe as mp
import pyautogui

# Initialize variables
x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

def detect_fist_gesture(hand1, hand2, frame_width, frame_height):
    x1, y1 = int(hand1.landmark[8].x * frame_width), int(hand1.landmark[8].y * frame_height)
    x2, y2 = int(hand2.landmark[8].x * frame_width), int(hand2.landmark[8].y * frame_height)
    return abs(x1 - x2) < 50 and abs(y1 - y2) < 50

def detect_super_gesture(hand, frame_width, frame_height):
    x1, y1 = int(hand.landmark[8].x * frame_width), int(hand.landmark[8].y * frame_height)
    x2, y2 = int(hand.landmark[4].x * frame_width), int(hand.landmark[4].y * frame_height)
    return abs(x1 - x2) < 20 and abs(y1 - y2) < 20

while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x2 = x
                    y2 = y
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
            if dist > 50:
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")

    cv2.imshow("Hand Volume Control using Python", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()