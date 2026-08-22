"""
Executable script for running full statistical randomness and baseline evaluation suite.
Saves results to results/tables/ directory.
"""

import sys
import os
import json
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import BiometricBlockchainPipeline
from src.biometric.landmark_extraction import LandmarkExtractor
from src.biometric.preprocessing import FeatureNormalizer
from src.evaluation.biometric_stability import evaluate_biometric_stability
from src.evaluation.hamming_distance import calculate_average_pairwise_hamming

def run():
    print("Running Statistical Randomness and Biometric Evaluation Suite...")
    os.makedirs("results/tables", exist_ok=True)
    os.makedirs("results/figures", exist_ok=True)

    pipeline = BiometricBlockchainPipeline()
    extractor = LandmarkExtractor()
    normalizer = FeatureNormalizer()

    # 1. Comparative Architecture Evaluation
    sample_landmarks = extractor.generate_synthetic_subject_landmarks(subject_id=1)
    baseline_metrics = pipeline.run_baseline_comparisons(sample_landmarks)

    print("\n--- ARCHITECTURE COMPARISON RESULTS ---")
    for arch, metrics in baseline_metrics.items():
        print(f"\n[{arch}]")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

    # 2. Biometric Stability Evaluation (Intra-person vs Inter-person)
    print("\n--- BIOMETRIC STABILITY EVALUATION (10 Subjects x 5 Captures) ---")
    subject_captures = {}
    for sub in range(1, 11):
        caps = []
        for cap_idx in range(5):
            lm = extractor.generate_synthetic_subject_landmarks(
                subject_id=sub,
                capture_index=cap_idx,
                noise_level=0.02
            )
            norm_feat = normalizer.normalize_landmarks(lm)
            caps.append(norm_feat)
        subject_captures[sub] = caps

    stability_results = evaluate_biometric_stability(subject_captures, threshold=0.35)
    for k, v in stability_results.items():
        print(f"  {k}: {v:.6f}" if isinstance(v, float) else f"  {k}: {v}")

    # 3. Save Summary JSON (Convert numpy types to standard Python types for JSON)
    def clean_json(obj):
        if isinstance(obj, dict):
            return {k: clean_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_json(v) for v in obj]
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, (np.integer, int)):
            return int(obj)
        elif isinstance(obj, (np.floating, float)):
            return float(obj)
        return obj

    summary_data = clean_json({
        'architecture_baselines': baseline_metrics,
        'biometric_stability': stability_results
    })
    output_path = "results/tables/evaluation_summary.json"
    with open(output_path, 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f"\nEvaluation summary successfully saved to: {output_path}")

if __name__ == '__main__':
    run()
