Here's a detailed README file for your project:

---

# Hand Gesture Control for Brightness and Volume

This project allows you to control your system's screen brightness and volume using hand gestures. It utilizes computer vision techniques with OpenCV and MediaPipe for hand tracking and integrates with `screen_brightness_control` and `pycaw` for adjusting the system settings.

## Features
- **Hand Gesture Control**: Use hand gestures to adjust the screen brightness and system volume.
- **Real-time Feedback**: Display the current brightness and volume on the video feed.
- **Dual Hand Tracking**: Supports tracking both hands to control the brightness (left hand) and volume (right hand).
- **Cross-Platform**: Works with most systems that support Python and required libraries.

## Requirements
- Python 3.6+
- Libraries:
  - `opencv-python` (for video capture and display)
  - `mediapipe` (for hand tracking)
  - `screen_brightness_control` (for controlling screen brightness)
  - `pycaw` (for controlling system volume)
  - `numpy` (for numerical calculations)
  - `ctypes`, `comtypes` (for audio control)
  
You can install the necessary libraries using `pip`:

```bash
pip install opencv-python mediapipe screen_brightness_control pycaw numpy
```

## Setup

### 1. Install Python and Dependencies
Make sure you have Python 3.6 or later installed. Then, install the required dependencies using the command:

```bash
pip install opencv-python mediapipe screen_brightness_control pycaw numpy
```

### 2. Clone or Download the Repository
Clone this repository or download the `hand_control.py` file.

```bash
git clone https://github.com/yourusername/hand-gesture-control.git
```

### 3. Run the Application
Execute the script to start hand gesture control.

```bash
python hand_control.py
```

The application will launch a video stream and begin tracking your hands for adjusting brightness and volume.

## Usage

- **Left Hand**: Use your left hand to control the screen brightness. Move your thumb and index finger closer to decrease the brightness, and move them apart to increase it.
- **Right Hand**: Use your right hand to control the system volume in the same manner.
- **Feedback**: The current brightness percentage and system volume will be displayed on the video feed in real-time.

### Exit the Application
To exit the application, press the **'q'** key while the video feed window is active.

## How It Works

1. **Hand Tracking**: The program uses MediaPipe's hand tracking model to detect the positions of the index and thumb fingers.
2. **Brightness Control**: The distance between the thumb and index finger on the left hand is mapped to the screen brightness (0% to 100%).
3. **Volume Control**: Similarly, the distance between the thumb and index finger on the right hand is mapped to the system's volume.
4. **Real-time Feedback**: The program continuously updates the video feed with the current brightness and volume levels for user feedback.

## Libraries and Tools Used

- **OpenCV**: For video capture and processing.
- **MediaPipe**: For detecting hand landmarks and tracking hand gestures.
- **screen_brightness_control**: For controlling screen brightness on supported systems.
- **pycaw**: For controlling the system volume on Windows.
- **numpy**: For mathematical operations, particularly interpolation to map hand gestures to system settings.
















## Working 


This code enables hand gesture control for adjusting the screen brightness and system volume. It uses a combination of computer vision libraries, such as OpenCV and MediaPipe, to detect and track hand landmarks, and then manipulates the system's brightness and audio levels based on the distance between hand landmarks.

### Breakdown of the Code

#### **Imports**
1. **`cv2`**: This is OpenCV, a library used for image processing and computer vision tasks, such as capturing video frames and drawing on them.
2. **`numpy`**: This is used for numerical operations, particularly in this case for interpolation, which helps adjust brightness and volume based on the distance between landmarks.
3. **`mediapipe`**: This library provides hand tracking solutions. The `mp.solutions.hands` module is used to detect and track hand landmarks.
4. **`screen_brightness_control` (sbc)**: A third-party library used for controlling screen brightness.
5. **`pycaw`**: This library is used to control system audio. It interacts with the Windows Audio API to change the volume.
6. **`ctypes` & `comtypes`**: These are used to interact with the COM (Component Object Model) interface for audio control in Windows.

#### **Class: `HandControl`**
The class `HandControl` encapsulates all functionality for hand gesture recognition and control over brightness and volume.

1. **Initialization (`__init__`)**
   - The class sets up several objects:
     - **MediaPipe Hands**: This object is responsible for hand tracking.
     - **Video Capture (`cv2.VideoCapture(0)`)**: Captures live video from the default camera (usually the built-in webcam).
     - **Audio Initialization**: The `init_audio` method sets up the audio controls using `pycaw`.
     - **Brightness and Volume**: The initial brightness and volume levels are set, and flags to track the program’s state (`is_running`) are initialized.

2. **`init_audio` Method**
   - This method initializes the system's audio control interface using `pycaw`. It activates the speakers, and returns an interface for controlling the volume.
   
3. **`adjust_brightness` Method**
   - This method adjusts the screen's brightness based on the distance between two specific hand landmarks (typically the index finger and thumb). The distance is calculated using the `calculate_distance` method.
   - The brightness level is then adjusted using the `screen_brightness_control` library (`sbc.set_brightness`).

4. **`adjust_volume` Method**
   - This method adjusts the system’s volume based on the distance between the hand landmarks (presumably the other hand’s thumb and index finger).
   - The volume range is retrieved using the `pycaw` library, and the volume is adjusted accordingly.

5. **`calculate_distance` Method**
   - This method calculates the Euclidean distance between two points (x1, y1) and (x2, y2) on the screen. These points correspond to specific hand landmarks. The `hypot` function from the `math` library is used for this calculation.

6. **`process_hands` Method**
   - This method processes the hand landmarks detected by MediaPipe. For each hand, it tracks specific landmarks (thumb and index finger tips, indices 4 and 8). 
   - It separates landmarks into two sets: one for the left hand and one for the right. If two hands are detected, the landmarks are assigned to `left_landmarks` and `right_landmarks` respectively.
   - After processing, it returns the landmark coordinates for the left and right hands.

7. **`display_feedback` Method**
   - This method overlays text on the frame, displaying the current screen brightness and system volume on the video stream.

8. **`run` Method**
   - This method is the main loop where the program continuously captures video frames, processes the frames to detect hand landmarks, and adjusts the brightness and volume based on hand movements.
   - If the video frame is successfully captured, it is processed by MediaPipe to detect hand landmarks.
   - The brightness and volume are adjusted according to the hand gestures, and the feedback is displayed on the screen.
   - The loop continues until the user presses the 'q' key to quit.

#### **Main Execution (`if __name__ == '__main__':`)**
- If this file is run as the main program, an instance of the `HandControl` class is created, and the `run` method is called to start the hand gesture control system.

---

### Key Features:
1. **Real-time Hand Tracking**: Using MediaPipe, the code detects hand landmarks in real-time. Specifically, it uses the index finger and thumb positions to calculate the distance, which is then mapped to control the brightness and volume.
   
2. **Volume and Brightness Control**: 
   - The left hand controls screen brightness by adjusting the distance between the index finger and thumb.
   - The right hand controls the system volume in the same way.
   
3. **User Feedback**: The system provides visual feedback on the screen about the current brightness and volume levels.

4. **Cross-Platform Integration**: The use of OpenCV and MediaPipe ensures that the program can be used across different platforms (though the `pycaw` library is Windows-specific).

---

### Example of Use Case:
- The user raises their left hand and moves the thumb and index finger closer or farther apart to increase or decrease the screen brightness.
- The right hand performs a similar gesture to control the system's volume.
- Feedback about the current brightness and volume levels is displayed on the video feed in real-time.

### Conclusion:
This program provides an intuitive method for controlling system settings through hand gestures, making it useful in situations where traditional input methods (keyboard, mouse, touch) are not feasible or convenient, such as presentations, accessibility applications, or hands-free control setups.


## Troubleshooting

- **Camera Issues**: Make sure your camera is working properly. If you're using an external webcam, ensure it is connected and accessible.
- **Volume/Brightness Not Responding**: Ensure that your system is compatible with `pycaw` (Windows) and `screen_brightness_control`. The code is designed to work on Windows, but you might need platform-specific adjustments for other OSes.

## Contributing

If you'd like to contribute to this project, feel free to submit issues or pull requests. Any improvements, bug fixes, or suggestions are welcome!
