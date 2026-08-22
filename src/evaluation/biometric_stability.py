"""
Biometric Stability Evaluation Submodule.
Measures intra-person vs inter-person feature distances, FRR/FAR stability metrics,
and key reproducibility rates under noise.
"""

import numpy as np
from typing import Dict, List, Tuple, Any


def evaluate_biometric_stability(
    subject_captures: Dict[int, List[np.ndarray]],
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Evaluates biometric feature stability across multiple captures of subjects.

    Args:
        subject_captures: Dict mapping subject_id -> list of normalized feature vectors.
        threshold: Distance threshold for matching decision.

    Returns:
        Dict with intra_mean, intra_std, inter_mean, inter_std, frr, far metrics.
    """
    intra_distances = []
    inter_distances = []
    subject_ids = list(subject_captures.keys())

    # 1. Intra-person distances (same subject, different captures)
    for sub_id, captures in subject_captures.items():
        if len(captures) >= 2:
            for i in range(len(captures)):
                for j in range(i + 1, len(captures)):
                    d = np.linalg.norm(captures[i] - captures[j])
                    intra_distances.append(d)

    # 2. Inter-person distances (different subjects)
    for i in range(len(subject_ids)):
        for j in range(i + 1, len(subject_ids)):
            caps1 = subject_captures[subject_ids[i]]
            caps2 = subject_captures[subject_ids[j]]
            for c1 in caps1:
                for c2 in caps2:
                    d = np.linalg.norm(c1 - c2)
                    inter_distances.append(d)

    intra_arr = np.array(intra_distances) if intra_distances else np.array([0.0])
    inter_arr = np.array(inter_distances) if inter_distances else np.array([1.0])

    # FRR: False Reject Rate (intra distances > threshold)
    frr = float(np.mean(intra_arr > threshold)) if len(intra_arr) > 0 else 0.0

    # FAR: False Accept Rate (inter distances <= threshold)
    far = float(np.mean(inter_arr <= threshold)) if len(inter_arr) > 0 else 0.0

    return {
        'intra_mean': float(np.mean(intra_arr)),
        'intra_std': float(np.std(intra_arr)),
        'inter_mean': float(np.mean(inter_arr)),
        'inter_std': float(np.std(inter_arr)),
        'frr': frr,
        'far': far,
        'threshold': threshold
    }
