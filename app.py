from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = load_model('custom_model.h5')
img_width, img_height = 48, 48
class_labels=["balancing","falling",  "hugging",  "⁠lookingup",	"sitting"  ,"standing"]
allowed_extensions = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        file_content = file.read()
        file_bytes = io.BytesIO(file_content)
        img = image.load_img(file_bytes, 
                           target_size=(img_width, img_height),
                           color_mode='grayscale')
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        confidence = float(np.max(prediction))
        print("Predicted Class ",predicted_class)
        return jsonify({
            "predicted_class": class_labels[predicted_class],
            "confidence": confidence
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
