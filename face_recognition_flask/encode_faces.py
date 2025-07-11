import face_recognition
import os
import pickle

path = 'images'
known_encodings = []
known_names = []

for filename in os.listdir(path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(path, filename)
        name = os.path.splitext(filename)[0]

        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)

with open('encodings.pickle', 'wb') as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Encodings saved to encodings.pickle.")
