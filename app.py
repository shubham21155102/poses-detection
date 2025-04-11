from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

# Load the custom model
custom_model = load_model('custom_model.h5')

# Example: Define image size and class labels
img_width, img_height = 224, 224  # Adjust to your model's input size
class_labels = ['sitting', 'standing']  # Modify based on your dataset

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)



def process_local_image(file_path):
    image = cv2.imread(file_path)
    if image is not None:
        return analyze_image(image)
    return ["Error: Could not read image"]

@app.route('/predict_custom_model', methods=['POST'])
def predict_custom_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    img = keras_image.load_img(file, target_size=(img_width, img_height), color_mode='grayscale')
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = custom_model.predict(img_array)
    predicted_class = np.argmax(prediction)

    return jsonify({"predicted_class": class_labels[predicted_class]})

if __name__ == '__main__':
    app.run(debug=True)
