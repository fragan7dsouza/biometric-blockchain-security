"""
AES-256-GCM Authenticated Encryption Submodule.
Provides authenticated encryption and decryption using AES-256 in Galois/Counter Mode (GCM).
Enforces confidentiality, integrity, and tamper detection.
"""

import os
from typing import Dict, Union, Tuple, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


class AESGCMCipher:
    """
    Handles AES-256-GCM authenticated encryption and decryption.
    """

    KEY_SIZE_BYTES = 32   # 256 bits
    NONCE_SIZE_BYTES = 12 # 96 bits (NIST standard for GCM)
    TAG_SIZE_BYTES = 16   # 128 bits authentication tag

    def __init__(self, key: bytes):
        if len(key) != self.KEY_SIZE_BYTES:
            raise ValueError(f"AES-256 key must be exactly {self.KEY_SIZE_BYTES} bytes ({self.KEY_SIZE_BYTES * 8} bits). Received {len(key)} bytes.")
        self.key = key
        self.aesgcm = AESGCM(key)

    def encrypt(
        self,
        plaintext: Union[str, bytes],
        associated_data: Optional[bytes] = None,
        nonce: Optional[bytes] = None
    ) -> Dict[str, bytes]:
        """
        Encrypts plaintext using AES-256-GCM.

        Args:
            plaintext: Text string or raw bytes payload.
            associated_data: Optional unencrypted header/context data for authentication.
            nonce: Optional 12-byte initialization vector (generates fresh random nonce if omitted).

        Returns:
            Dict containing:
                'nonce': 12-byte nonce
                'ciphertext': Encrypted ciphertext payload
                'tag': 16-byte GCM authentication tag (embedded/extracted)
                'combined': nonce + ciphertext (cryptography library output includes tag in ciphertext)
        """
        if isinstance(plaintext, str):
            payload = plaintext.encode('utf-8')
        else:
            payload = bytes(plaintext)

        if nonce is None:
            nonce = os.urandom(self.NONCE_SIZE_BYTES)
        elif len(nonce) != self.NONCE_SIZE_BYTES:
            raise ValueError(f"Nonce must be exactly {self.NONCE_SIZE_BYTES} bytes.")

        # AESGCM.encrypt returns ciphertext + tag appended at the end
        raw_output = self.aesgcm.encrypt(nonce, payload, associated_data)
        ciphertext = raw_output[:-self.TAG_SIZE_BYTES]
        tag = raw_output[-self.TAG_SIZE_BYTES:]

        return {
            'nonce': nonce,
            'ciphertext': ciphertext,
            'tag': tag,
            'combined': raw_output
        }

    def decrypt(
        self,
        encrypted_data: Dict[str, bytes],
        associated_data: Optional[bytes] = None
    ) -> bytes:
        """
        Decrypts AES-256-GCM encrypted payload and verifies authentication tag.

        Args:
            encrypted_data: Dict containing 'nonce', 'ciphertext', and optional 'tag' or 'combined'.
            associated_data: Optional associated data.

        Returns:
            Decrypted raw bytes payload.

        Raises:
            ValueError or InvalidTag on tampering or incorrect key/tag.
        """
        nonce = encrypted_data['nonce']

        if 'combined' in encrypted_data:
            raw_input = encrypted_data['combined']
        else:
            ciphertext = encrypted_data['ciphertext']
            tag = encrypted_data['tag']
            raw_input = ciphertext + tag

        try:
            plaintext_bytes = self.aesgcm.decrypt(nonce, raw_input, associated_data)
            return plaintext_bytes
        except InvalidTag:
            raise ValueError("Decryption failed: Authentication tag mismatch or payload tampering detected.")
