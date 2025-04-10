from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


def analyze_image(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    poses = []
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        if (landmarks[23].y + landmarks[24].y) / 2 > (landmarks[11].y + landmarks[12].y) / 2 + 0.1 and \
           landmarks[25].y > landmarks[23].y and landmarks[26].y > landmarks[24].y:
            poses.append("sitting")
        elif (landmarks[23].y + landmarks[24].y) / 2 < (landmarks[11].y + landmarks[12].y) / 2 + 0.05 and \
                landmarks[25].y < landmarks[23].y and landmarks[26].y < landmarks[24].y:
            poses.append("standing")
    return poses


@app.route('/detect_poses', methods=['POST'])
def detect_poses():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(
        file.read(), np.uint8), cv2.IMREAD_COLOR)
    poses = analyze_image(image)
    return jsonify({"results": [{"poses": poses}]})

# New local file processing function


def process_local_image(file_path):
    image = cv2.imread(file_path)
    if image is not None:
        return analyze_image(image)
    return ["Error: Could not read image"]


if __name__ == '__main__':
    # Example usage for local files:
    # print(process_local_image('path/to/your/image.jpg'))
    app.run(debug=True)
