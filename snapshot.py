import cv2
import mediapipe as mp
import numpy as np
import math
import time
from scipy.spatial import distance as dist
import winsound
import threading
import os
from datetime import datetime

class AlcoholAndDrowsinessDetectionSystem:
    def __init__(self):
        # Existing initializations
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Parameters for alcohol detection
        self.gaze_deviation_threshold = 0.1
        self.mar_threshold = 0.5
        self.head_yaw_threshold = 15
        self.head_pitch_threshold = 30
        self.alcohol_alert_threshold = 3
        
        # Parameters for drowsiness detection
        self.EAR_THRESHOLD = 0.2
        self.CLOSED_EYE_DURATION_THRESHOLD = 0.85
        
        # Eye landmarks for EAR calculations
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        # Alert sound parameters
        self.primary_alert = "primary_alert.wav"
        self.secondary_alert = "secondary_alert.wav"
        self.alcohol_alert = "alcohol_alert.wav"
        
        # Flags and state tracking
        self.drowsiness_alert_issued = False
        self.alcohol_alert_issued = False
        self.start_drowsy_time = None
        self.alcohol_alert_last_played_time = 0
        self.alcohol_alert_cooldown = 2
        self.drowsiness_alert_count = 0
        
        # Snapshot-related attributes
        self.snapshot_folder = "screenshots"
        self.last_snapshot_time = 0
        self.snapshot_cooldown = 5  # Minimum seconds between snapshots
        
        # Create snapshot directory if it doesn't exist
        if not os.path.exists(self.snapshot_folder):
            os.makedirs(self.snapshot_folder)

    def calculate_mouth_aspect_ratio(self, landmarks):
        upper_lip = np.array([landmarks.landmark[13].x, landmarks.landmark[13].y])
        lower_lip = np.array([landmarks.landmark[14].x, landmarks.landmark[14].y])
        left_corner = np.array([landmarks.landmark[61].x, landmarks.landmark[61].y])
        right_corner = np.array([landmarks.landmark[291].x, landmarks.landmark[291].y])
        
        vertical = np.linalg.norm(upper_lip - lower_lip)
        horizontal = np.linalg.norm(left_corner - right_corner)
        return vertical / horizontal

    def calculate_gaze_deviation(self, landmarks, frame_width, frame_height):
        left_eye_inner = np.array([landmarks.landmark[133].x * frame_width, landmarks.landmark[133].y * frame_height])
        left_eye_outer = np.array([landmarks.landmark[33].x * frame_width, landmarks.landmark[33].y * frame_height])
        left_pupil = np.array([landmarks.landmark[468].x * frame_width, landmarks.landmark[468].y * frame_height])
        
        right_eye_inner = np.array([landmarks.landmark[362].x * frame_width, landmarks.landmark[362].y * frame_height])
        right_eye_outer = np.array([landmarks.landmark[263].x * frame_width, landmarks.landmark[263].y * frame_height])
        right_pupil = np.array([landmarks.landmark[473].x * frame_width, landmarks.landmark[473].y * frame_height])
        
        left_ratio = (left_pupil[0] - left_eye_inner[0]) / (left_eye_outer[0] - left_eye_inner[0])
        right_ratio = (right_pupil[0] - right_eye_inner[0]) / (right_eye_outer[0] - right_eye_inner[0])
        
        return abs(left_ratio - right_ratio)

    def get_head_pose(self, landmarks):
        nose = np.array([landmarks.landmark[1].x, landmarks.landmark[1].y])
        chin = np.array([landmarks.landmark[152].x, landmarks.landmark[152].y])
        left_eye = np.array([landmarks.landmark[33].x, landmarks.landmark[33].y])
        right_eye = np.array([landmarks.landmark[362].x, landmarks.landmark[362].y])
        
        yaw = math.degrees(math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]))
        pitch = math.degrees(math.atan2(chin[1] - nose[1], chin[0] - nose[0]))
        return yaw, pitch

    def take_snapshot(self, original_frame):
        """Save a snapshot of the current frame with timestamp"""
        current_time = time.time()
        if current_time - self.last_snapshot_time >= self.snapshot_cooldown:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"suspect{timestamp}.jpg"
            filepath = os.path.join(self.snapshot_folder, filename)
            cv2.imwrite(filepath, original_frame)
            self.last_snapshot_time = current_time
            print(f"Snapshot saved: {filepath}")

    def alcohol_detection_logic(self, gaze_deviation, mar, head_yaw, head_pitch):
        criteria_met = 0
        if gaze_deviation > self.gaze_deviation_threshold:
            criteria_met += 1
        if mar > self.mar_threshold:
            criteria_met += 1
        if abs(head_yaw) > self.head_yaw_threshold and abs(head_pitch) > self.head_pitch_threshold:
            criteria_met += 1
        return criteria_met >= self.alcohol_alert_threshold

    def calculate_ear(self, eye_landmarks):
        vertical_1 = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        vertical_2 = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        horizontal = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear

    def play_sound(self, sound_file):
        threading.Thread(target=winsound.PlaySound, args=(sound_file, winsound.SND_FILENAME)).start()

    def process_frame(self, frame):
        # Store the original frame before any modifications
        original_frame = frame.copy()
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        frame_height, frame_width = frame.shape[:2]
        
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                # Draw landmarks on the display frame (not the original)
                self.mp_drawing.draw_landmarks(frame, landmarks, self.mp_face_mesh.FACEMESH_TESSELATION)
                
                # Alcohol detection
                mar = self.calculate_mouth_aspect_ratio(landmarks)
                gaze_deviation = self.calculate_gaze_deviation(landmarks, frame_width, frame_height)
                head_yaw, head_pitch = self.get_head_pose(landmarks)
                
                current_time = time.time()
                if self.alcohol_detection_logic(gaze_deviation, mar, head_yaw, head_pitch):
                    if not self.alcohol_alert_issued and (current_time - self.alcohol_alert_last_played_time > self.alcohol_alert_cooldown):
                        self.play_sound(self.alcohol_alert)
                        self.alcohol_alert_issued = True
                        self.alcohol_alert_last_played_time = current_time
                        # Take snapshot of the original frame without landmarks
                        self.take_snapshot(original_frame)
                    alert_text = "Alcohol Detected!"
                else:
                    if self.alcohol_alert_issued:
                        self.alcohol_alert_issued = False
                    alert_text = "No Alcohol Detected"
                
                # Drowsiness detection
                left_eye = [(landmarks.landmark[i].x * frame.shape[1], landmarks.landmark[i].y * frame.shape[0]) for i in self.LEFT_EYE]
                right_eye = [(landmarks.landmark[i].x * frame.shape[1], landmarks.landmark[i].y * frame.shape[0]) for i in self.RIGHT_EYE]
                left_ear = self.calculate_ear(left_eye)
                right_ear = self.calculate_ear(right_eye)
                avg_ear = (left_ear + right_ear) / 2.0
                
                if avg_ear < self.EAR_THRESHOLD:
                    if self.start_drowsy_time is None:
                        self.start_drowsy_time = time.time()
                    elif time.time() - self.start_drowsy_time >= self.CLOSED_EYE_DURATION_THRESHOLD:
                        self.drowsiness_alert_count += 1
                        if self.drowsiness_alert_count <= 3:
                            if not self.drowsiness_alert_issued:
                                self.play_sound(self.primary_alert)
                                self.drowsiness_alert_issued = True
                        elif self.drowsiness_alert_count == 4:
                            if not self.drowsiness_alert_issued:
                                self.play_sound(self.secondary_alert)
                                self.drowsiness_alert_issued = True
                            self.drowsiness_alert_count = 0
                        alert_text += " | Drowsiness Detected!"
                else:
                    self.start_drowsy_time = None
                    self.drowsiness_alert_issued = False
                
                # Display the parameters
                params_text = f"EAR: {avg_ear:.2f}  MAR: {mar:.2f}  Gaze Dev: {gaze_deviation:.2f}  Yaw: {head_yaw:.2f}  Pitch: {head_pitch:.2f}"
                cv2.putText(frame, alert_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, params_text, (10, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow('Frame', frame)

    def start_detection(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.process_frame(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = AlcoholAndDrowsinessDetectionSystem()
    system.start_detection()