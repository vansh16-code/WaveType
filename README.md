# Virtual Keyboard with Hand Gesture Recognition

This project implements a virtual keyboard controlled by hand gestures using OpenCV, MediaPipe, and Python. The user can type on a virtual keyboard displayed on the screen using hand gestures, such as pinching the thumb and index finger together to "click" on a key.

## Features

- **Hand Gesture Recognition**: Detects hand movements using MediaPipe and responds to gestures such as pinching the thumb and index finger to select keys.
- **Interactive Virtual Keyboard**: A dynamic on-screen keyboard that updates the typed text.
- **Web Search Integration**: Allows the user to perform a Google search by typing the desired text and pressing the "SEARCH" button.
- **Backspace Functionality**: Users can delete the last typed character by pressing the "BACK" button.
- **Full-Screen Layout**: The keyboard layout adjusts dynamically to the screen size.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

You can install the required dependencies using `pip`:

```bash
pip install opencv-python mediapipe numpy
