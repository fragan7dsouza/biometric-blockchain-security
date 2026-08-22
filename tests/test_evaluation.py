"""
Unit tests for Evaluation Metrics Submodule (Entropy, Correlation, Randomness, Hamming Distance).
"""

import pytest
import numpy as np
from src.evaluation.entropy import calculate_shannon_entropy_bytes, calculate_shannon_entropy_bits
from src.evaluation.correlation import calculate_pearson_correlation, calculate_average_pearson_correlation
from src.evaluation.randomness import runs_test, chi_square_uniformity_test, nist_monobit_frequency_test
from src.evaluation.hamming_distance import calculate_hamming_distance, calculate_average_pairwise_hamming


def test_shannon_entropy():
    # Uniform random bytes should have entropy close to 8.0 bits/byte
    rnd_bytes = bytes(np.random.randint(0, 256, size=10000, dtype=np.uint8))
    ent = calculate_shannon_entropy_bytes(rnd_bytes)
    assert ent > 7.5

    # Constant bytes should have 0 entropy
    const_bytes = b"\xAA" * 1000
    ent_const = calculate_shannon_entropy_bytes(const_bytes)
    assert ent_const == 0.0


def test_pearson_correlation():
    seq1 = np.arange(100, dtype=float)
    seq2 = np.arange(100, dtype=float)
    corr = calculate_pearson_correlation(seq1, seq2)
    assert abs(corr - 1.0) < 1e-5


def test_runs_test():
    # Alternating bits 01010101...
    alt_bits = np.tile([0, 1], 100)
    z_stat, p_val, is_rand = runs_test(alt_bits)
    assert is_rand is False or abs(z_stat) > 1.96

    # Random bits
    rnd_bits = np.random.randint(0, 2, size=1000)
    z_stat_r, p_val_r, is_rand_r = runs_test(rnd_bits)
    assert abs(z_stat_r) < 3.5


def test_hamming_distance():
    b1 = b"\x00" * 10
    b2 = b"\xFF" * 10
    abs_d, norm_d = calculate_hamming_distance(b1, b2)
    assert abs_d == 80
    assert norm_d == 1.0

    b3 = b"\x00" * 10
    abs_d0, norm_d0 = calculate_hamming_distance(b1, b3)
    assert abs_d0 == 0
    assert norm_d0 == 0.0
