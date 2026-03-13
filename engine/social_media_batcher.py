import os
import cv2
from typing import List, Dict

def calculate_safe_zones(file_path: str, target_formats: List[str]) -> Dict[str, Dict[str, int]]:
    """
    Analyzes the source video resolution and calculates precise 
    cropping coordinates (safe zones) for various social media formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")

    # Open video to read metadata
    cap = cv2.VideoCapture(file_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    crop_data = {}
    
    for fmt in target_formats:
        if fmt == "9:16": # Reels / Shorts / TikTok
            target_w = int(height * (9 / 16))
            x_offset = (width - target_w) // 2
            crop_data["9:16"] = {"x": x_offset, "y": 0, "w": target_w, "h": height}
            
        elif fmt == "1:1": # Instagram Feed / LinkedIn
            target_w = min(width, height)
            target_h = min(width, height)
            x_offset = (width - target_w) // 2
            y_offset = (height - target_h) // 2
            crop_data["1:1"] = {"x": x_offset, "y": y_offset, "w": target_w, "h": target_h}
            
        elif fmt == "16:9": # YouTube Standard
            target_h = int(width * (9 / 16))
            y_offset = (height - target_h) // 2
            crop_data["16:9"] = {"x": 0, "y": y_offset, "w": width, "h": target_h}
            
    return crop_data
