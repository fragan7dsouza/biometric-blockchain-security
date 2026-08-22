"""
Unit tests for Cryptographic Key Derivation (HKDF-SHA256) Submodule.
"""

import pytest
import numpy as np
from src.key_generation.seed_generator import BiometricSeedGenerator
from src.key_generation.key_derivation import HKDFKeyDeriver


def test_seed_generator():
    seed_gen = BiometricSeedGenerator()
    feats = np.random.rand(50)

    seed_bytes = seed_gen.generate_seed_bytes(feats)
    assert len(seed_bytes) == 32

    seed_int = seed_gen.generate_seed_integer(feats, bit_length=32)
    assert isinstance(seed_int, int)
    assert seed_int != 0


def test_hkdf_key_deriver():
    deriver = HKDFKeyDeriver(key_size=32)
    ikm = b"lfsr-expanded-pseudo-random-input-seed-material-512bits"

    key1 = deriver.derive_key(ikm)
    key2 = deriver.derive_key(ikm)

    assert isinstance(key1, bytes)
    assert len(key1) == 32
    assert key1 == key2  # Deterministic derivation


def test_hkdf_different_ikm_produces_different_keys():
    deriver = HKDFKeyDeriver()
    key1 = deriver.derive_key(b"ikm_seed_A")
    key2 = deriver.derive_key(b"ikm_seed_B")

    assert key1 != key2
