import json

scene_data = {
    "frame_id": 12,
    "timestamp": "00:00:05.120",
    "objects": [
        {"type": "autorickshaw", "bbox": [112, 212, 208, 287]},
        {"type": "person", "gender": "male", "age_estimate": 32, "bbox": [289, 210, 330, 295]},
        {"type": "dog", "bbox": [350, 222, 398, 273]}
    ]
}

# Save as JSON
with open('scene_data.json', 'w') as f:
    json.dump(scene_data, f, indent=2)
