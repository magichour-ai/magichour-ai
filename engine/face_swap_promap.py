import cv2
import mediapipe as mp
from typing import Dict, Optional

def extract_face_landmarks(image_path: str) -> Optional[Dict]:
    """
    Extracts 468 3D face landmarks locally using Google MediaPipe.
    This module prepares the pro-map data to be sent to the cloud,
    drastically reducing server-side compute costs.
    """
    mp_face_mesh = mp.solutions.face_mesh
    
    # Load the source image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")
        
    # Process the image (requires RGB format)
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return None
            
        # Extract coordinates to generate a bounding box
        h, w, _ = image.shape
        landmarks = results.multi_face_landmarks[0].landmark
        
        x_coords = [int(pt.x * w) for pt in landmarks]
        y_coords = [int(pt.y * h) for pt in landmarks]
        
        # Calculate bounding box with a small margin
        margin = 20
        bbox = {
            "x_min": max(0, min(x_coords) - margin), 
            "y_min": max(0, min(y_coords) - margin),
            "x_max": min(w, max(x_coords) + margin), 
            "y_max": min(h, max(y_coords) + margin)
        }
        
        return {
            "landmarks_count": len(landmarks),
            "bounding_box": bbox,
            "status": "ready_for_cloud_swap"
        }
