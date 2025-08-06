# INDUSTRY-READY VERSION: Face Recognition Attendance System
# Technology Stack: PyQt5 + OpenCV + Face_Recognition + Pandas
# Features: Real-time camera, optimized frame processing, GUI popups, one-time attendance, snapshot storage

import sys
import os
import cv2
import face_recognition
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import pickle

SNAPSHOT_DIR = 'snapshots'
CSV_FILE = 'attendance.csv'
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Load known face encodings
with open('encodings.pickle', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

# Track attendance
marked_today = set()

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=['Name', 'Date', 'Time', 'Snapshot']).to_csv(CSV_FILE, index=False)

def mark_attendance(name, frame):
    now = datetime.now()
    time_str = now.strftime('%H-%M-%S')
    date_str = now.strftime('%Y-%m-%d')
    filename = f"{name}_{date_str}_{time_str}.jpg"
    filepath = os.path.join(SNAPSHOT_DIR, filename)
    cv2.imwrite(filepath, frame)

    df = pd.read_csv(CSV_FILE)
    if not ((df['Name'] == name) & (df['Date'] == date_str)).any():
        df.loc[len(df)] = [name, date_str, now.strftime('%H:%M:%S'), filename]
        df.to_csv(CSV_FILE, index=False)

class AttendanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Recognition Attendance System')
        self.video_label = QLabel()
        self.status_label = QLabel('Starting camera...')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        success, frame = self.cap.read()
        if not success:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            face_distances = face_recognition.face_distance(known_encodings, encoding)

            name = "Unknown"
            if True in matches:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_names[best_match_index].capitalize()

            y1, x2, y2, x1 = [v * 4 for v in location]
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, name, (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            today = datetime.now().strftime("%Y-%m-%d")
            unique_key = f"{name}_{today}"
            if name != "Unknown" and unique_key not in marked_today:
                marked_today.add(unique_key)
                mark_attendance(name, frame)
                self.show_popup(f"✅ Attendance Captured for {name}")

        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def show_popup(self, text):
        self.status_label.setText(text)
        msg = QMessageBox()
        msg.setWindowTitle("Attendance")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())
