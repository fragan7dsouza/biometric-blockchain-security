"""
Hamming Distance Evaluation Submodule.
Computes absolute and normalized bitwise Hamming distance between cryptographic keys.
"""

import numpy as np
from typing import Union, Tuple, List


def calculate_hamming_distance(seq1: Union[bytes, np.ndarray], seq2: Union[bytes, np.ndarray]) -> Tuple[int, float]:
    """
    Calculates absolute bitwise Hamming distance and normalized Hamming distance (0.0 to 1.0).
    Ideal random keys have normalized Hamming distance = 0.50 (50% bit flip).

    Returns:
        (absolute_distance: int, normalized_distance: float)
    """
    if isinstance(seq1, bytes):
        b1 = np.unpackbits(np.frombuffer(seq1, dtype=np.uint8))
    else:
        b1 = np.array(seq1).flatten()

    if isinstance(seq2, bytes):
        b2 = np.unpackbits(np.frombuffer(seq2, dtype=np.uint8))
    else:
        b2 = np.array(seq2).flatten()

    min_len = min(len(b1), len(b2))
    if min_len == 0:
        return 0, 0.0

    b1_trim = b1[:min_len]
    b2_trim = b2[:min_len]

    diff_bits = np.sum(b1_trim != b2_trim)
    norm_dist = float(diff_bits) / float(min_len)

    return int(diff_bits), norm_dist


def calculate_average_pairwise_hamming(keys: List[Union[bytes, np.ndarray]]) -> float:
    """
    Computes average normalized Hamming distance across all pairs in a list of keys.
    """
    if len(keys) < 2:
        return 0.0

    distances = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            _, norm_d = calculate_hamming_distance(keys[i], keys[j])
            distances.append(norm_d)

    return float(np.mean(distances))
