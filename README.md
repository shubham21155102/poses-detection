
# Pose Detection System

![Pose Detection](image.png)

A powerful ML-powered application that can identify human poses from images with high accuracy. This project combines a TensorFlow-based backend with a clean, modern React frontend.

## 🚀 Features

- **Real-time Pose Classification**: Instantly identify poses including balancing, falling, hugging, looking up, sitting, and standing
- **User-friendly Interface**: Simple drag-and-drop upload with instant visual feedback
- **Confidence Scoring**: Get probability scores for detection accuracy
- **Cross-platform**: Works on any device with a modern browser

## 🧠 Technology Stack

### Backend

- Flask REST API
- TensorFlow/Keras deep learning model
- Python image processing
- spaCy NLP for intelligent dataset curation

### Frontend

- React/Next.js
- Tailwind CSS for sleek UI
- React Dropzone for easy file uploads

## 📊 Model Information

- Custom CNN model trained on diverse human pose datasets
- Six pose classes: balancing, falling, hugging, looking up, sitting, standing
- 48x48 grayscale image input format
- High accuracy across different body types and positions

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ with pip
- Node.js and npm
- Git (with git-lfs for model files)
- spaCy with English language model (`python -m spacy download en_core_web_sm`)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/pose-detection.git
   cd pose-detection
   ```
2. Install backend dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:

   ```
   cd pose-detection-frontend
   npm install
   ```
4. Start the backend server:

   ```
   python app.py
   ```
5. Start the frontend development server:

   ```
   cd pose-detection-frontend
   npm run dev
   ```
6. Open your browser and navigate to http://localhost:3000

## 📸 Dataset

The model was trained on carefully curated images from Unsplash covering six human pose categories. We use two methods for dataset collection:

1. **Basic collection** (`download.py`): Filters images by aspect ratio for basic dataset curation.
2. **Advanced NLP-based collection** (`script.py`): Uses spaCy for intelligent filtering:

   - Performs lemmatization to match various forms of action words
   - Analyzes image alt-text descriptions
   - Verifies image integrity before saving
   - Implements rate limiting to respect API guidelines
   - Downloads highest quality training samples based on semantic relevance

This dual approach ensures a diverse, high-quality dataset that improves model performance.

## 🛠️ API Endpoints

- `POST /predict`: Submit an image file for pose detection
  - Returns: Predicted pose class and confidence score

## 📝 License

[MIT License](LICENSE)

## 👥 Contributors

- [Shubham](https://github.com/shubham21155102)

## 🔮 Future Improvements

- Support for multiple pose detection in a single image
- Real-time webcam integration
- Additional pose classes
- Mobile app version

---

Made with ❤️ by Shubham
