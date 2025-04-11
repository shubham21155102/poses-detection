import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

def analyze_image(image, output_dir="output"):
   
    if image is None:
        print("Error: Input image is None")
        return None
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    original_path = os.path.join(output_dir, "original.png")
    cv2.imwrite(original_path, image)
    print(f"Saved original image: {original_path}")
    
    height, width, _ = image.shape
    print(f"Image dimensions: {width}x{height}")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    

    rgb_path = os.path.join(output_dir, "rgb_converted.png")
    cv2.imwrite(rgb_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)) 
    print(f"Saved RGB converted image: {rgb_path}")
    
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        print("No person detected in the image")
        return []
    
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
    )
    
    landmarks_path = os.path.join(output_dir, "landmarks.png")
    cv2.imwrite(landmarks_path, annotated_image)
    print(f"Saved landmarks image: {landmarks_path}")
    
    landmarks = results.pose_landmarks.landmark
    poses = []
    
    hip_y = (landmarks[23].y + landmarks[24].y) / 2
    shoulder_y = (landmarks[11].y + landmarks[12].y) / 2
    left_knee_y = landmarks[25].y
    right_knee_y = landmarks[26].y
    left_hip_y = landmarks[23].y
    right_hip_y = landmarks[24].y
    
    print(f"Hip Y: {hip_y:.3f}, Shoulder Y: {shoulder_y:.3f}")
    print(f"Left Knee Y: {left_knee_y:.3f}, Left Hip Y: {left_hip_y:.3f}")
    print(f"Right Knee Y: {right_knee_y:.3f}, Right Hip Y: {right_hip_y:.3f}")
    
    if hip_y > shoulder_y + 0.05 and (left_knee_y > left_hip_y or right_knee_y > right_hip_y):
        poses.append("sitting")
    elif hip_y < shoulder_y + 0.1 and (left_knee_y < left_hip_y or right_knee_y < right_hip_y):
        poses.append("standing")
    
    return poses


image_path = 'image.png'
image = cv2.imread(image_path)

if image is not None:
    result = analyze_image(image, output_dir="output")
    if result is not None:
        if result:
            print(f"Detected poses: {result}")
        else:
            print("No poses detected")
    else:
        print("Error: Failed to process image")
else:
    print(f"Error: Could not load image at {image_path}")

pose.close()