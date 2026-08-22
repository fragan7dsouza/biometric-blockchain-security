"""
Unit tests for Biometric Feature Extraction and Preprocessing Submodule.
"""

import pytest
import numpy as np
from src.biometric.landmark_extraction import LandmarkExtractor
from src.biometric.preprocessing import FeatureNormalizer
from src.biometric.face_detection import FaceDetector


def test_face_detector_synthetic():
    detector = FaceDetector()
    img = np.ones((200, 200, 3), dtype=np.uint8) * 128
    ok, bbox = detector.detect_face(img)
    assert ok is True
    assert bbox is not None
    assert len(bbox) == 4

    crop = detector.crop_face(img, bbox, target_size=(224, 224))
    assert crop.shape == (224, 224, 3)


def test_landmark_extractor_synthetic():
    extractor = LandmarkExtractor(num_landmarks=106)
    landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1, capture_index=0)
    assert landmarks is not None
    assert landmarks.shape == (106, 2)


def test_feature_normalizer():
    extractor = LandmarkExtractor(num_landmarks=106)
    normalizer = FeatureNormalizer(target_bounds=(-1.0, 1.0))

    landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1)
    norm_features = normalizer.normalize_landmarks(landmarks)

    assert len(norm_features) == 212
    assert np.min(norm_features) >= -1.0
    assert np.max(norm_features) <= 1.0


def test_translation_and_scale_invariance():
    extractor = LandmarkExtractor(num_landmarks=106)
    normalizer = FeatureNormalizer()

    lm1 = extractor.generate_synthetic_subject_landmarks(subject_id=1, capture_index=0)
    # Shift and scale lm1
    lm2 = (lm1 + np.array([50.0, 100.0])) * 2.5

    norm1 = normalizer.normalize_landmarks(lm1)
    norm2 = normalizer.normalize_landmarks(lm2)

    # Procrustes normalization should yield near identical feature vectors
    diff = np.max(np.abs(norm1 - norm2))
    assert diff < 1e-4
