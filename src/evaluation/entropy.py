"""
Shannon Entropy Evaluation Submodule.
Computes bitwise and byte-wise Shannon Entropy for generated keys and sequences.
"""

import numpy as np
from typing import Union


def calculate_shannon_entropy_bytes(data: bytes) -> float:
    """
    Calculates Shannon Entropy in bits per byte (theoretical max = 8.0 bits).
    H(X) = - sum( p_i * log2(p_i) )
    """
    if not data:
        return 0.0

    array = np.frombuffer(data, dtype=np.uint8)
    _, counts = np.unique(array, return_counts=True)
    probabilities = counts / len(array)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return float(entropy)


def calculate_shannon_entropy_bits(bit_array: Union[np.ndarray, bytes, list]) -> float:
    """
    Calculates Shannon Entropy in bits per binary symbol (theoretical max = 1.0 bit).
    Reference paper calculates entropy on discrete symbol alphabets (e.g. 3.24 bits for 10-bin histogram).
    """
    if isinstance(bit_array, bytes):
        bits = np.unpackbits(np.frombuffer(bit_array, dtype=np.uint8))
    else:
        bits = np.array(bit_array).flatten()

    if len(bits) == 0:
        return 0.0

    _, counts = np.unique(bits, return_counts=True)
    probabilities = counts / len(bits)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return float(entropy)
