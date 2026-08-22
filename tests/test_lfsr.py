"""
Unit tests for Linear Feedback Shift Register (LFSR) Submodule.
"""

import pytest
import numpy as np
from src.key_generation.lfsr import LFSRBitGenerator, PaperLFSRSubsequenceGenerator


def test_lfsr_bit_generator_determinism():
    lfsr1 = LFSRBitGenerator(register_size=32, seed_state=0x12345678)
    lfsr2 = LFSRBitGenerator(register_size=32, seed_state=0x12345678)

    bits1 = lfsr1.generate_bits(64)
    bits2 = lfsr2.generate_bits(64)

    assert len(bits1) == 64
    assert np.array_equal(bits1, bits2)


def test_lfsr_bytes_generation():
    lfsr = LFSRBitGenerator(seed_state=0xABCDEF01)
    bytes_out = lfsr.generate_bytes(16)

    assert isinstance(bytes_out, bytes)
    assert len(bytes_out) == 16


def test_paper_lfsr_subsequence_generator():
    paper_lfsr = PaperLFSRSubsequenceGenerator(num_registers=8, modulus=256)
    seed_feats = np.array([12.5, 45.3, 78.1, 99.0, 34.2, 88.5, 12.1, 67.4])

    seqs = paper_lfsr.generate_subsequences(seed_feats, num_iterations=100)
    assert len(seqs) == 100
    assert len(seqs[0]) == 8
    assert np.all(seqs[0] >= 0) and np.all(seqs[0] < 256)
