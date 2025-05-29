import numpy as np
import mediapipe as mp

FINGER_TIPS = [
    mp.solutions.hands.HandLandmark.THUMB_TIP,
    mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP,
    mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP,
    mp.solutions.hands.HandLandmark.RING_FINGER_TIP,
    mp.solutions.hands.HandLandmark.PINKY_TIP
]
FINGER_MCP = [
    mp.solutions.hands.HandLandmark.THUMB_MCP,
    mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP,
    mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP,
    mp.solutions.hands.HandLandmark.RING_FINGER_MCP,
    mp.solutions.hands.HandLandmark.PINKY_MCP
]

DISTANCE_THRESHOLD = 0.2

def detect_extended_fingers(landmarks):
    extended_fingers = 0
    wrist = landmarks[mp.solutions.hands.HandLandmark.WRIST]
    for tip, mcp in zip(FINGER_TIPS, FINGER_MCP):
        tip_y = landmarks[tip].y
        mcp_y = landmarks[mcp].y
        tip_dist = np.sqrt(
            (landmarks[tip].x - wrist.x) ** 2 +
            (landmarks[tip].y - wrist.y) ** 2
        )
        if tip_y < mcp_y and tip_dist > DISTANCE_THRESHOLD:
            extended_fingers += 1
    return extended_fingers

def get_movement_key(extended_fingers):
    movement_map = {
        1: 'w',
        2: 's',
        3: 'a',
        4: 'd'
    }
    return movement_map.get(extended_fingers, None)

def detect_right_hand_fingers(landmarks):
    keys = set()
    wrist = landmarks[mp.solutions.hands.HandLandmark.WRIST]
    for i, (tip, mcp) in enumerate(zip(FINGER_TIPS, FINGER_MCP)):
        tip_y = landmarks[tip].y
        mcp_y = landmarks[mcp].y
        tip_dist = np.sqrt(
            (landmarks[tip].x - wrist.x) ** 2 +
            (landmarks[tip].y - wrist.y) ** 2
        )
        is_extended = tip_y < mcp_y and tip_dist > DISTANCE_THRESHOLD
        if is_extended:
            if i == 0:
                keys.add('1')
            elif i == 1:
                keys.add('2')
            elif i == 2:
                keys.add('3')
            elif i == 3:
                keys.add('e')
            elif i == 4:
                keys.add('q')
    return keys

def get_right_hand_finger_states(landmarks):
    wrist = landmarks[mp.solutions.hands.HandLandmark.WRIST]
    states = []
    for tip, mcp in zip(FINGER_TIPS, FINGER_MCP):
        tip_y = landmarks[tip].y
        mcp_y = landmarks[mcp].y
        tip_dist = np.sqrt(
            (landmarks[tip].x - wrist.x) ** 2 +
            (landmarks[tip].y - wrist.y) ** 2
        )
        is_extended = tip_y < mcp_y and tip_dist > DISTANCE_THRESHOLD
        states.append(is_extended)
    return tuple(states)
