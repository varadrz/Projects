import face_recognition
import os
import pickle
import cv2

KNOWN_DIR = 'known_faces'
known_encodings = []
known_names = []

for name in os.listdir(KNOWN_DIR):
    img_path = os.path.join(KNOWN_DIR, name)
    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_encodings.append(encodings[0])
        known_names.append(os.path.splitext(name)[0])
    else:
        print(f"No face found in {name}")

with open('encodings.pickle', 'wb') as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Encodings saved successfully.")
