import cv2
from ultralytics import YOLO
import os

# Load your 1080p video
input_video = "LifeFitness_Gym_Transformation_Animation.mp4"  # paste the path of your video here
output_video = "yolo.mp4"  # will be saved in the same directory

USE_YOLO = True

# Load YOLOv8 Pose Model
yolo_model = YOLO("yolov8n-pose.pt") if USE_YOLO else None   # <-- use pose model

# Open input video
cap = cv2.VideoCapture(input_video)

# Get input video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

# Setup output video writer
out = cv2.VideoWriter(
    output_video,
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps,
    (frame_width, frame_height)
)

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"📹 Processing {frame_count} frames from {input_video}...")

# Frame loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8 Pose Detection
    if yolo_model:
        yolo_results = yolo_model(frame, verbose=False)
        frame = yolo_results[0].plot()  # draw pose skeletons directly

    # Save the processed frame
    out.write(frame)

# Cleanup
cap.release()
out.release()
print(f"✅ Saved processed video to: {output_video}")
