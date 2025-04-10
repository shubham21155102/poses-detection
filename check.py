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


result = process_local_image('path/to/image.jpg')