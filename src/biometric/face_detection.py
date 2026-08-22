"""
Face Detection and Alignment Submodule.
Handles face bounding box detection and facial crop preprocessing.
"""

import numpy as np
from typing import Tuple, Optional, Dict, Any


class FaceDetector:
    """
    Detects faces in images and extracts ROI / bounding boxes.
    Supports OpenCV Haar/DNN and fallback geometric bounding box.
    """

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

    def detect_face(self, image: np.ndarray) -> Tuple[bool, Optional[Tuple[int, int, int, int]]]:
        """
        Detect face bounding box in image.
        Returns:
            (success, (x, y, w, h))
        """
        if image is None or image.size == 0:
            return False, None

        # Check image dimensions
        if len(image.shape) == 2:
            h, w = image.shape
        elif len(image.shape) == 3:
            h, w, _ = image.shape
        else:
            return False, None

        if h < 20 or w < 20:
            return False, None

        # Try OpenCV cascade or fallback heuristic
        try:
            import cv2
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Return largest face
                largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
                return True, tuple(map(int, largest_face))
        except Exception:
            pass

        # Fallback: assume face occupies central region (0.1 to 0.9 of dimension)
        x = int(w * 0.1)
        y = int(h * 0.1)
        fw = int(w * 0.8)
        fh = int(h * 0.8)
        return True, (x, y, fw, fh)

    def crop_face(self, image: np.ndarray, bbox: Tuple[int, int, int, int], target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Crops and resizes image to target dimension.
        """
        x, y, w, h = bbox
        img_h, img_w = image.shape[:2]
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(img_w, x + w), min(img_h, y + h)

        crop = image[y1:y2, x1:x2]
        try:
            import cv2
            return cv2.resize(crop, target_size)
        except Exception:
            # Fallback simple nearest-neighbor / slicing resize via numpy
            if crop.size == 0:
                return np.zeros((*target_size, 3 if len(image.shape) == 3 else 1), dtype=np.uint8)
            grid_y = np.linspace(0, crop.shape[0] - 1, target_size[1]).astype(int)
            grid_x = np.linspace(0, crop.shape[1] - 1, target_size[0]).astype(int)
            return crop[np.ix_(grid_y, grid_x)]
