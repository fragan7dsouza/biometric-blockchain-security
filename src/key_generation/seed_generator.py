"""
Biometric Seed Generation Submodule.
Serializes GA-optimized biometric features canonically and computes a deterministic SHA-256 seed.
"""

import hashlib
import struct
import numpy as np
from typing import Tuple, Union, Optional


class BiometricSeedGenerator:
    """
    Transforms biometric feature vectors into deterministic seed material for pseudo-random expansion.
    """

    def __init__(self, salt: bytes = b"biometric-seed-salt-v1"):
        self.salt = salt

    def generate_seed_bytes(self, feature_vector: np.ndarray) -> bytes:
        """
        Canonical serialization of feature vector float values to IEEE-754 double precision bytes,
        hashed with SHA-256 to generate 32 bytes (256 bits) of seed material.
        """
        if feature_vector is None or len(feature_vector) == 0:
            feature_vector = np.zeros(16, dtype=float)

        # Canonical binary serialization: struct pack 64-bit IEEE floats in big-endian order
        buffer = bytearray(self.salt)
        for val in feature_vector:
            buffer.extend(struct.pack(">d", float(val)))

        # SHA-256 digest
        hasher = hashlib.sha256()
        hasher.update(buffer)
        return hasher.digest()

    def generate_seed_integer(self, feature_vector: np.ndarray, bit_length: int = 32) -> int:
        """
        Derives an unsigned integer seed of specified bit length (e.g. 32 bits for LFSR state).
        """
        seed_bytes = self.generate_seed_bytes(feature_vector)
        raw_int = int.from_bytes(seed_bytes[:4], byteorder="big")
        mask = (1 << bit_length) - 1
        val = raw_int & mask
        # Ensure seed is non-zero (LFSR requirement)
        return val if val != 0 else 0xDEADBEEF
