import cv2
import numpy as np
import mediapipe as mp
import screen_brightness_control as sbc
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class HandControl:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            max_num_hands=2
        )
        self.draw_utils = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.volume = self.init_audio()
        self.brightness_level = 50
        self.volume_level = 0
        self.is_running = True

    def init_audio(self):
        """Initialize audio control for volume"""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume

    def adjust_brightness(self, landmarks):
        """Adjust brightness based on the left hand distance"""
        if landmarks:
            distance = self.calculate_distance(landmarks)
            self.brightness_level = int(np.interp(distance, [50, 220], [0, 100]))
            sbc.set_brightness(self.brightness_level)

    def adjust_volume(self, landmarks):
        """Adjust volume based on the right hand distance"""
        if landmarks:
            distance = self.calculate_distance(landmarks)
            min_vol, max_vol, _ = self.volume.GetVolumeRange()
            self.volume_level = np.interp(distance, [50, 220], [min_vol, max_vol])
            self.volume.SetMasterVolumeLevel(self.volume_level, None)

    def calculate_distance(self, landmarks):
        """Calculate the distance between two landmarks"""
        if len(landmarks) < 2:
            return 0
        (x1, y1), (x2, y2) = landmarks
        distance = hypot(x2 - x1, y2 - y1)
        return distance

    def process_hands(self, frame, results):
        """Process detected hands and identify landmarks for brightness and volume control"""
        left_landmarks = []
        right_landmarks = []

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                landmarks = []
                for point_idx, landmark in enumerate(hand_landmarks.landmark):
                    height, width, _ = frame.shape
                    x, y = int(landmark.x * width), int(landmark.y * height)
                    if point_idx in [4, 8]:
                        landmarks.append((x, y))

                if landmarks:
                    if idx == 0:
                        left_landmarks = landmarks
                    elif idx == 1:
                        right_landmarks = landmarks

                self.draw_utils.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return left_landmarks, right_landmarks

    def display_feedback(self, frame):
        """Display the current brightness and volume on the frame"""
        cv2.putText(frame, f'Brightness: {self.brightness_level}%', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f'Volume: {int(self.volume_level)}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    def run(self):
        """Run the main loop to capture video and process hand movements"""
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to capture video frame.")
                    break

                frame = cv2.flip(frame, 1)  # Mirror the frame for intuitive control
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(frame_rgb)

                left_landmarks, right_landmarks = self.process_hands(frame, results)

                # Adjust brightness and volume
                self.adjust_brightness(left_landmarks)
                self.adjust_volume(right_landmarks)

                # Display feedback
                self.display_feedback(frame)

                cv2.imshow('Hand Control', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_running = False
                    print("Exiting...")
                    break
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    hand_control = HandControl()
    hand_control.run()
