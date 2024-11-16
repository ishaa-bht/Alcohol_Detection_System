# Alcohol and Drowsiness Detection System

This project implements a real-time driver alertness detection system that monitors drowsiness and alcohol impairment using computer vision and facial landmark detection. The system uses **MediaPipe** to analyze the driver's face in video frames and issues audio alerts based on specific parameters related to drowsiness and alcohol detection.

## Features

- **Drowsiness Detection**: 
  - Monitors eye aspect ratio (EAR) to detect if the driver's eyes are closed for too long.
  - Issues primary and secondary alerts when drowsiness is detected.

- **Alcohol Detection**: 
  - Analyzes gaze deviation, mouth aspect ratio (MAR), and head pose to detect alcohol impairment.
  - Issues alerts if alcohol impairment is suspected.

- **Snapshot Capture**: 
  - Takes a snapshot of the driver when alcohol is detected or drowsiness is suspected.
  - Saves the snapshot with a timestamp in a designated folder.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- SciPy

Install dependencies:
```bash
pip install opencv-python mediapipe scipy
```

## Usage

1. Run the program:
   ```bash
   python snapshot.py
   ```

2. The system will start processing the webcam feed, detecting drowsiness and alcohol impairment.

3. Press 'q' to quit the application.

## Alert System

- **Primary Alert**: Played when the driver shows signs of drowsiness.
- **Secondary Alert**: Played after several drowsy detections.
- **Alcohol Alert**: Played when alcohol impairment is detected.
