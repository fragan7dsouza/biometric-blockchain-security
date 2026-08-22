"""
Executable script for executing the full biometric-blockchain pipeline demonstration.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import BiometricBlockchainPipeline
from src.biometric.landmark_extraction import LandmarkExtractor

def run():
    print("Initializing Biometric Blockchain Security Pipeline...")
    pipeline = BiometricBlockchainPipeline()
    extractor = LandmarkExtractor()

    # Generate synthetic landmark capture for Subject #1
    landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1)

    plaintext = "Biometric Cryptography Blockchain Immutable Data Record - Test Payload"
    print(f"Encrypting payload: '{plaintext}'")

    res = pipeline.process_end_to_end(
        image_or_landmarks=landmarks,
        plaintext_data=plaintext,
        user_id="alice_subject_01",
        tx_id="tx_biometric_demo_101"
    )

    print("\n--- PIPELINE EXECUTION SUCCESS ---")
    print(f"Landmarks Count      : {res['landmarks_count']}")
    print(f"Normalized Features  : {res['normalized_features_dim']}")
    print(f"GA Selected Features : {res['ga_selected_dim']}")
    print(f"Derived AES-256 Key  : {res['aes_key_len']} bytes")
    print(f"Decryption Verified  : {res['decryption_correct']}")
    print(f"Mined Block Index    : {res['block_index']}")
    print(f"Mined Block Hash     : {res['block_hash']}")
    print(f"Ciphertext Hash      : {res['ciphertext_hash']}")
    print(f"Blockchain Status    : {res['verification_msg']}")

if __name__ == '__main__':
    run()
