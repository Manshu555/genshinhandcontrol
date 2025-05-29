Hand Gesture Controller for Genshin Impact
Overview
This project uses hand gestures to control gameplay in Genshin Impact by leveraging the MediaPipe Hands library for real-time hand tracking and the pyautogui library for simulating keyboard inputs. The script captures video from your webcam, processes hand gestures, and maps them to in-game actions such as movement, character switching, and skill usage.

Left Hand: Controls character movement (W, A, S, D) using finger counting.
Right Hand: Controls character switching (1, 2, 3), elemental skill (E), and ultimate skill (Q) using individual finger detection.

Prerequisites

Python 3.11. dont use other modules.
A webcam (at least 720p recommended for better detection)
Genshin Impact installed and running on your computer in windowed mode

Required Libraries
Install the following Python libraries using pip:
pip install opencv-python mediapipe pyautogui


opencv-python: For capturing and processing webcam video.
mediapipe: For hand tracking and gesture recognition.
pyautogui: For simulating keyboard inputs.

Setup

Save the script as gesture_recognition.py.
Ensure your webcam is connected and functioning.
Launch Genshin Impact and ensure it’s in focus (active window).
Run the script:

python gesture_recognition.py


Position your hands in front of the webcam (about 30–50 cm away) and ensure good lighting for accurate detection.

Controls
Left Hand (Movement)
The left hand uses finger counting to control character movement in Genshin Impact. The number of extended fingers determines the direction:

1 finger: Hold W (move forward)
2 fingers: Hold S (move backward)
3 fingers: Hold A (move left)
4 fingers: Hold D (move right)

Right Hand (Character Switching and Skills)
The right hand uses individual finger detection to control character switching and skills. Each finger maps to a specific key:

Thumb extended: Press 1 (switch to Character 1)
Index finger extended: Press 2 (switch to Character 2)
Middle finger extended: Press 3 (switch to Character 3)
Ring finger extended: Press E (use elemental skill)
Pinky finger extended: Press Q (use ultimate skill)

Notes:

Multiple fingers can be extended simultaneously to press multiple keys (e.g., thumb and index extended will press 1 and 2).
To switch to the fourth character, you’ll need to press the 4 key manually on your keyboard, as it’s not mapped to a gesture.

Exiting the Script

Press the p key on your keyboard to stop the script and release any held keys.

Usage

Launch Genshin Impact and enter a gameplay session.
Run the script (python gesture_recognition.py).
Position your hands in front of the webcam:
Ensure your hands are clearly visible and about 30–50 cm from the camera.
Face your palms toward the camera with fingers spread apart when extended.
Use good lighting to avoid shadows or detection issues.


Use your left hand to move your character and your right hand to switch characters or use skills.
Monitor the on-screen feedback:
L Fingers: X: Number of fingers detected on the left hand (for movement).
R: T I M R P: Indicates which right-hand fingers are extended (T = thumb, I = index, M = middle, R = ring, P = pinky).


Check the console for debug logs to confirm which gestures are detected and which keys are pressed.

Debugging Tips

Finger Detection Issues:

Ensure your hands are centered in the frame and facing the camera directly.
Spread your fingers apart when extending them to avoid overlap.
If a finger isn’t detected, adjust your hand position or improve lighting. You can also tweak the wrist-to-tip distance threshold in the script (default: 0.2).


Performance Issues:

If the script feels laggy, reduce the frame size by modifying the script:cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
FRAME_WIDTH, FRAME_HEIGHT = 320, 240


Close other applications to free up CPU resources.


Multiple Keys Pressed:

The script allows multiple right-hand fingers to trigger keys simultaneously (e.g., thumb and index extended → press 1 and 2). If this causes issues, you can modify the script to prioritize a single key per frame.



Limitations

The script only maps character switching for the first three characters (1, 2, 3). Use the keyboard to switch to the fourth character (4).
Detection accuracy depends on lighting, webcam quality, and hand positioning.
Some in-game actions (e.g., sprint, jump, attack) are not mapped and require manual keyboard input.

License
This project is for personal use and provided as-is. Feel free to modify the script to suit your needs.
# genshinhandcontrol
