from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import os
import pandas as pd
from datetime import datetime
import pickle
import time

app = Flask(__name__)

# Load known face encodings
with open('encodings.pickle', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

SNAPSHOT_DIR = 'static/snapshots'
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

CSV_FILE = 'attendance.csv'
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=['Name', 'Date', 'Time', 'Snapshot']).to_csv(CSV_FILE, index=False)

marked_today = set()

message_global = None
message_time_global = 0

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

def generate_frames():
    global message_global, message_time_global
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_FPS, 60)

    delay_counters = {}

    while True:
        success, frame = cap.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for encoding, loc in zip(encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            name = "Unknown"

            if matches:
                best_match = face_distances.argmin()
                if matches[best_match]:
                    name = known_names[best_match].capitalize()
                    y1, x2, y2, x1 = [v * 4 for v in loc]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                    today = datetime.now().strftime("%Y-%m-%d")
                    unique_key = f"{name}_{today}"

                    if unique_key not in marked_today:
                        if unique_key not in delay_counters:
                            delay_counters[unique_key] = time.time()
                        elif time.time() - delay_counters[unique_key] > 2:
                            marked_today.add(unique_key)
                            mark_attendance(name, frame)
                            message_global = f"✅ Attendance Captured for {name}"
                            message_time_global = time.time()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/message')
def message():
    global message_global, message_time_global
    if message_global and time.time() - message_time_global < 3:
        return jsonify({"message": message_global})
    return jsonify({"message": ""})

if __name__ == '__main__':
    app.run(debug=True)
