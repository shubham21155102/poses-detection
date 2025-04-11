from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
model = load_model('custom_model.h5')
img_width, img_height = 48, 48 
from tensorflow.keras.preprocessing import image
import numpy as np

img_path = 'image.png';
img = image.load_img(img_path, target_size=(img_width, img_height), color_mode='grayscale')

img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) 
img_array = img_array / 255.0 

prediction = model.predict(img_array)
predicted_class = np.argmax(prediction)
class_labels=["balancing","falling",  "hugging",  "⁠lookingup",	"sitting"  ,"standing"]
print("Predicted class:", class_labels[predicted_class])
