"""
Biometric Feature Preprocessing and Normalization Submodule.
Implements Procrustes alignment, scale, translation, and rotation normalization
to produce stable biometric feature vectors from facial landmark coordinates.
"""

import numpy as np
from typing import Tuple, Optional


class FeatureNormalizer:
    """
    Normalizes 106 2D facial landmark coordinates to produce invariant biometric feature vectors.
    """

    def __init__(self, target_bounds: Tuple[float, float] = (-1.0, 1.0), quantization_bits: int = 16):
        self.target_bounds = target_bounds
        self.quantization_bits = quantization_bits

    def normalize_landmarks(self, landmarks: np.ndarray, align_rotation: bool = True) -> np.ndarray:
        """
        Normalizes landmarks (shape: N x 2, e.g., 106 x 2).
        Returns:
            Normalized 1D feature vector of shape (2 * N, ) in range target_bounds.
        """
        if landmarks is None or len(landmarks) == 0:
            return np.zeros(212, dtype=float)

        pts = landmarks.copy().astype(float)

        # 1. Translation Normalization: Subtract Centroid
        centroid = np.mean(pts, axis=0)
        pts -= centroid

        # 2. Scale Normalization: Scale by Root Mean Square (RMS) distance
        rms_scale = np.sqrt(np.mean(np.sum(pts**2, axis=1)))
        if rms_scale > 1e-8:
            pts /= rms_scale

        # 3. Rotation Normalization (Alignment along principal axis or eye line)
        if align_rotation and pts.shape[0] >= 2:
            # Use Principal Component Analysis (SVD) for main orientation axis
            cov = np.dot(pts.T, pts) / pts.shape[0]
            u, s, vt = np.linalg.svd(cov)
            angle = np.arctan2(vt[0, 1], vt[0, 0])
            rot_mat = np.array([
                [np.cos(-angle), -np.sin(-angle)],
                [np.sin(-angle),  np.cos(-angle)]
            ])
            pts = np.dot(pts, rot_mat.T)

        # 4. Bounding Box Scaling to target_bounds [-1, 1]
        min_val = np.min(pts)
        max_val = np.max(pts)
        val_range = max_val - min_val
        if val_range > 1e-8:
            low, high = self.target_bounds
            pts = low + (pts - min_val) * (high - low) / val_range

        # Flatten into 1D feature vector (x1, y1, x2, y2, ..., x106, y106)
        return pts.flatten()

    def quantize_features(self, feature_vector: np.ndarray) -> np.ndarray:
        """
        Quantizes floating-point feature vector to fixed-point integer representation.
        """
        max_int = (1 << self.quantization_bits) - 1
        low, high = self.target_bounds
        clipped = np.clip(feature_vector, low, high)
        scaled = (clipped - low) / (high - low) * max_int
        return np.round(scaled).astype(np.uint64)
