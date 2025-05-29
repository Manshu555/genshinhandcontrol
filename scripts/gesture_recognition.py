import cv2
import numpy as np
import mediapipe as mp
import pyautogui

pyautogui.PAUSE = 0.03

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
FRAME_WIDTH, FRAME_HEIGHT = 640, 480

last_keys = set()
current_movement_key = None

FINGER_TIPS = [
    mp_hands.HandLandmark.THUMB_TIP,
    mp_hands.HandLandmark.INDEX_FINGER_TIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
    mp_hands.HandLandmark.RING_FINGER_TIP,
    mp_hands.HandLandmark.PINKY_TIP
]
FINGER_MCP = [
    mp_hands.HandLandmark.THUMB_MCP,
    mp_hands.HandLandmark.INDEX_FINGER_MCP,
    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
    mp_hands.HandLandmark.RING_FINGER_MCP,
    mp_hands.HandLandmark.PINKY_MCP
]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    movement_key = None
    current_keys = set()
    extended_fingers_left = 0
    left_hand_detected = False

    thumb_extended = False
    index_extended = False
    middle_extended = False
    ring_extended = False
    pinky_extended = False

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label
            landmarks = hand_landmarks.landmark
            wrist = landmarks[mp_hands.HandLandmark.WRIST]

            if hand_label == "Left":
                left_hand_detected = True
                extended_fingers = 0
                for tip, mcp in zip(FINGER_TIPS, FINGER_MCP):
                    tip_y = landmarks[tip].y
                    mcp_y = landmarks[mcp].y
                    tip_dist = np.sqrt(
                        (landmarks[tip].x - wrist.x) ** 2 +
                        (landmarks[tip].y - wrist.y) ** 2
                    )
                    if tip_y < mcp_y and tip_dist > 0.2:
                        extended_fingers += 1
                extended_fingers_left = extended_fingers

                if extended_fingers == 1:
                    movement_key = "w"
                    print("Left: 1 finger -> W")
                elif extended_fingers == 2:
                    movement_key = "s"
                    print("Left: 2 fingers -> S")
                elif extended_fingers == 3:
                    movement_key = "a"
                    print("Left: 3 fingers -> A")
                elif extended_fingers == 4:
                    movement_key = "d"
                    print("Left: 4 fingers -> D")

            elif hand_label == "Right":
                for i, (tip, mcp) in enumerate(zip(FINGER_TIPS, FINGER_MCP)):
                    tip_y = landmarks[tip].y
                    mcp_y = landmarks[mcp].y
                    tip_dist = np.sqrt(
                        (landmarks[tip].x - wrist.x) ** 2 +
                        (landmarks[tip].y - wrist.y) ** 2
                    )
                    is_extended = tip_y < mcp_y and tip_dist > 0.2

                    if i == 0:
                        thumb_extended = is_extended
                        if is_extended:
                            current_keys.add("1")
                            print("Right: Thumb -> 1")
                    elif i == 1:
                        index_extended = is_extended
                        if is_extended:
                            current_keys.add("2")
                            print("Right: Index -> 2")
                    elif i == 2:
                        middle_extended = is_extended
                        if is_extended:
                            current_keys.add("3")
                            print("Right: Middle -> 3")
                    elif i == 3:
                        ring_extended = is_extended
                        if is_extended:
                            current_keys.add("e")
                            print("Right: Ring -> E")
                    elif i == 4:
                        pinky_extended = is_extended
                        if is_extended:
                            current_keys.add("q")
                            print("Right: Pinky -> Q")

    if movement_key:
        if movement_key != current_movement_key:
            if current_movement_key:
                pyautogui.keyUp(current_movement_key)
            pyautogui.keyDown(movement_key)
            current_movement_key = movement_key
    elif current_movement_key and not left_hand_detected:
        pyautogui.keyUp(current_movement_key)
        current_movement_key = None

    for key in current_keys - last_keys:
        pyautogui.press(key)
    last_keys = current_keys.copy()

    cv2.putText(frame, f"L Fingers: {extended_fingers_left}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    right_fingers = f"R: {'T' if thumb_extended else '-'} {'I' if index_extended else '-'} {'M' if middle_extended else '-'} {'R' if ring_extended else '-'} {'P' if pinky_extended else '-'}"
    cv2.putText(frame, right_fingers, (FRAME_WIDTH - 200, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Hand Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        if current_movement_key:
            pyautogui.keyUp(current_movement_key)
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
