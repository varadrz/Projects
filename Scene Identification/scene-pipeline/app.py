from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Save file, run object detection, summarize
    # Dummy analytics for illustration
    analytics = {
        "frame_count": 120,
        "objects": {
            "autorickshaw": 4,
            "person": 32,
            "dog": 2,
            "male": 18,
            "female": 14
        }
    }
    summary = (
        f"Detected {analytics['objects']['autorickshaw']} autorickshaws, "
        f"{analytics['objects']['person']} people "
        f"({analytics['objects']['male']} men, {analytics['objects']['female']} women), "
        f"{analytics['objects']['dog']} dogs in total across {analytics['frame_count']} frames."
    )
    return jsonify({
        "analytics": analytics,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(debug=True)
