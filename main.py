"""
Main Command Line Interface (CLI) for Biometric-Blockchain Security System.
Supports landmark extraction, key generation, AES-256-GCM encryption,
decryption, blockchain transaction verification, and full pipeline benchmarking.
"""

import sys
import os
import argparse
import json
import numpy as np

from src.config import DEFAULT_CONFIG
from src.pipeline import BiometricBlockchainPipeline
from src.biometric.landmark_extraction import LandmarkExtractor
from src.biometric.preprocessing import FeatureNormalizer
from src.encryption.aes import AESGCMCipher


def main():
    parser = argparse.ArgumentParser(
        description="Biometric-based Key Sequence Generation with Genetic Algorithm & Blockchain Security"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: extract-face
    p_extract = subparsers.add_parser("extract-face", help="Extract facial landmarks")
    p_extract.add_argument("--image", type=str, default=None, help="Path to facial image file")
    p_extract.add_argument("--subject-id", type=int, default=1, help="Synthetic subject ID if no image provided")

    # Command: generate-key
    p_keygen = subparsers.add_parser("generate-key", help="Generate 256-bit cryptographic key from facial biometrics")
    p_keygen.add_argument("--image", type=str, default=None, help="Path to facial image file")
    p_keygen.add_argument("--subject-id", type=int, default=1, help="Synthetic subject ID if no image provided")

    # Command: encrypt
    p_encrypt = subparsers.add_parser("encrypt", help="Encrypt data using biometric key and record on blockchain")
    p_encrypt.add_argument("--input", type=str, required=True, help="Data payload text to encrypt")
    p_encrypt.add_argument("--image", type=str, default=None, help="Path to facial image file")
    p_encrypt.add_argument("--user-id", type=str, default="user_001", help="User ID")
    p_encrypt.add_argument("--tx-id", type=str, default="tx_0001", help="Transaction ID")

    # Command: decrypt
    p_decrypt = subparsers.add_parser("decrypt", help="Decrypt ciphertext using biometric key")
    p_decrypt.add_argument("--combined-hex", type=str, required=True, help="Hex-encoded combined nonce+ciphertext+tag")
    p_decrypt.add_argument("--nonce-hex", type=str, default=None, help="Hex-encoded nonce if separate")
    p_decrypt.add_argument("--image", type=str, default=None, help="Path to facial image file")
    p_decrypt.add_argument("--subject-id", type=int, default=1, help="Synthetic subject ID if no image provided")

    # Command: verify
    p_verify = subparsers.add_parser("verify", help="Verify ciphertext integrity against blockchain metadata")
    p_verify.add_argument("--tx-id", type=str, required=True, help="Transaction ID")
    p_verify.add_argument("--combined-hex", type=str, required=True, help="Hex-encoded combined ciphertext bytes")

    # Command: evaluate
    p_eval = subparsers.add_parser("evaluate", help="Run statistical randomness & baseline evaluation suite")

    # Command: run-pipeline
    p_pipeline = subparsers.add_parser("run-pipeline", help="Run full end-to-end demonstration pipeline")
    p_pipeline.add_argument("--text", type=str, default="Confidential Blockchain Payload", help="Data to encrypt")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    pipeline = BiometricBlockchainPipeline()

    if args.command == "extract-face":
        extractor = LandmarkExtractor()
        if args.image and os.path.exists(args.image):
            import cv2
            img = cv2.imread(args.image)
            ok, landmarks = extractor.extract_landmarks(img)
        else:
            landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=args.subject_id)
            ok = True

        print(f"Extracted {len(landmarks)} landmark coordinates.")
        print("First 5 landmarks (x, y):")
        print(landmarks[:5])

    elif args.command == "generate-key":
        extractor = LandmarkExtractor()
        if args.image and os.path.exists(args.image):
            import cv2
            img = cv2.imread(args.image)
            ok, landmarks = extractor.extract_landmarks(img)
        else:
            landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=args.subject_id)

        res = pipeline.process_end_to_end(landmarks, plaintext_data="test")
        print("Generated 256-bit AES Key successfully.")
        print(f"Key length: {res['aes_key_len']} bytes")

    elif args.command == "encrypt":
        extractor = LandmarkExtractor()
        landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1)
        res = pipeline.process_end_to_end(
            image_or_landmarks=landmarks,
            plaintext_data=args.input,
            user_id=args.user_id,
            tx_id=args.tx_id
        )
        combined_hex = res['encrypted_result']['combined'].hex()
        print("--- ENCRYPTION COMPLETE ---")
        print(f"Transaction ID   : {res['tx_id']}")
        print(f"Block Index      : {res['block_index']}")
        print(f"Block Hash       : {res['block_hash']}")
        print(f"Ciphertext Hash  : {res['ciphertext_hash']}")
        print(f"Combined Ciphertext (hex): {combined_hex[:64]}...")

    elif args.command == "verify":
        ciphertext_bytes = bytes.fromhex(args.combined_hex)
        is_valid, msg, metadata = pipeline.verifier.verify_ciphertext_integrity(
            tx_id=args.tx_id,
            ciphertext_bytes=ciphertext_bytes
        )
        print("--- VERIFICATION RESULT ---")
        print(f"Valid       : {is_valid}")
        print(f"Status      : {msg}")

    elif args.command == "evaluate" or args.command == "run-pipeline":
        extractor = LandmarkExtractor()
        landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1)

        print("\n=======================================================")
        print(" RUNNING FULL END-TO-END PIPELINE & BASELINE BENCHMARK ")
        print("=======================================================\n")

        res = pipeline.process_end_to_end(landmarks, plaintext_data=getattr(args, 'text', 'Confidential Payload'))
        print("[1] End-to-End Pipeline Execution:")
        print(f"  - Landmarks Extracted : {res['landmarks_count']}")
        print(f"  - Normalized Dim      : {res['normalized_features_dim']}")
        print(f"  - GA Selected Dim     : {res['ga_selected_dim']}")
        print(f"  - LFSR Expanded Bytes : {res['lfsr_bytes_len']}")
        print(f"  - Derived AES Key Size: {res['aes_key_len']} bytes (256 bits)")
        print(f"  - Decryption Correct  : {res['decryption_correct']}")
        print(f"  - Blockchain Block    : Index #{res['block_index']} (Hash: {res['block_hash'][:16]}...)")
        print(f"  - Blockchain Verifier : {res['verification_msg']}")

        print("\n[2] Comparative Architecture Baselines:")
        baselines = pipeline.run_baseline_comparisons(landmarks)
        for b_name, b_metrics in baselines.items():
            print(f"\n  Architecture: {b_name}")
            for k, v in b_metrics.items():
                print(f"    - {k}: {v}")


if __name__ == "__main__":
    main()
