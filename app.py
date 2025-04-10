from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


@app.route('/detect_poses', methods=['POST'])
def detect_poses():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(
        file.read(), np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        poses = []
        if (landmarks[23].y + landmarks[24].y) / 2 > (landmarks[11].y + landmarks[12].y) / 2 + 0.1 and \
           landmarks[25].y > landmarks[23].y and landmarks[26].y > landmarks[24].y:
            poses.append("sitting")
        elif (landmarks[23].y + landmarks[24].y) / 2 < (landmarks[11].y + landmarks[12].y) / 2 + 0.05 and \
                landmarks[25].y < landmarks[23].y and landmarks[26].y < landmarks[24].y:
            poses.append("standing")
        return jsonify({"results": [{"poses": poses}]})
    else:
        return jsonify({"results": []})


if __name__ == '__main__':
    app.run(debug=True)
