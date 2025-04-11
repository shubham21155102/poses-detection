import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

def analyze_image(image):
    # Ensure image is valid
    if image is None:
        print("Error: Input image is None")
        return None
    
    # Get image dimensions
    height, width, _ = image.shape
    print(f"Image dimensions: {width}x{height}")
    
    # Convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process with MediaPipe Pose
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        print("No person detected in the image")
        return []
    
    landmarks = results.pose_landmarks.landmark
    poses = []
    
    # Calculate key positions
    hip_y = (landmarks[23].y + landmarks[24].y) / 2
    shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
    left_knee_y = landmarks[25].y
    right_knee_y = landmarks[26].y
    left_hip_y = landmarks[23].y
    right_hip_y = landmarks[24].y
    
    # Debug output
    print(f"Hip Y: {hip_y:.3f}, Shoulder Y: {shoulder_y:.3f}")
    print(f"Left Knee Y: {left_knee_y:.3f}, Left Hip Y: {left_hip_y:.3f}")
    print(f"Right Knee Y: {right_knee_y:.3f}, Right Hip Y: {right_hip_y:.3f}")
    
    # Sitting: Hips lower than shoulders, at least one knee below hip
    if hip_y > shoulder_y + 0.05 and (left_knee_y > left_hip_y or right_knee_y > right_hip_y):
        poses.append("sitting")
    # Standing: Hips close to shoulders, at least one knee above hip
    elif hip_y < shoulder_y + 0.1 and (left_knee_y < left_hip_y or right_knee_y < right_hip_y):
        poses.append("standing")
    
    return poses

# Load the image
image_path = 'image.png'
image = cv2.imread(image_path)

if image is not None:
    result = analyze_image(image)
    if result is not None:
        if result:
            print(f"Detected poses: {result}")
        else:
            print("No poses detected")
    else:
        print("Error: Failed to process image")
else:
    print(f"Error: Could not load image at {image_path}")

# Release resources
pose.close()