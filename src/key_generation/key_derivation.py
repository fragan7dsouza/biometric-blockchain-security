"""
Cryptographic Key Derivation Function (KDF) Submodule.
Uses HKDF-SHA256 (RFC 5869) to derive 256-bit AES cryptographic key material
from LFSR-expanded pseudo-random biometric seeds.
"""

import os
from typing import Optional
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from src.config import CryptographicConfig


class HKDFKeyDeriver:
    """
    Derives cryptographically strong, uniform 256-bit symmetric keys
    from biometric/LFSR seed sequences using HKDF-SHA256.
    """

    def __init__(
        self,
        salt: Optional[bytes] = None,
        info: Optional[bytes] = None,
        key_size: int = 32
    ):
        self.salt = salt or CryptographicConfig.salt
        self.info = info or CryptographicConfig.info
        self.key_size = key_size

    def derive_key(self, ikm: bytes, custom_salt: Optional[bytes] = None, custom_info: Optional[bytes] = None) -> bytes:
        """
        Derives a 256-bit (32-byte) AES key from input key material (ikm).

        Args:
            ikm: Input Key Material (e.g. LFSR output bytes or biometric seed).
            custom_salt: Optional salt override.
            custom_info: Optional context info string override.

        Returns:
            32-byte cryptographically derived symmetric key.
        """
        if not ikm:
            raise ValueError("Input Key Material (ikm) cannot be empty.")

        salt_to_use = custom_salt if custom_salt is not None else self.salt
        info_to_use = custom_info if custom_info is not None else self.info

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=self.key_size,
            salt=salt_to_use,
            info=info_to_use,
        )
        return hkdf.derive(ikm)
