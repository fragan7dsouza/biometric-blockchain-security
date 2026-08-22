"""
Unit tests for AES-256-GCM Authenticated Encryption Submodule.
"""

import pytest
import os
from src.encryption.aes import AESGCMCipher


def test_aes_gcm_encrypt_decrypt():
    key = os.urandom(32)
    cipher = AESGCMCipher(key)

    plaintext = "Biometric Security AES-256-GCM Payload Test"
    encrypted = cipher.encrypt(plaintext)

    assert 'nonce' in encrypted
    assert 'ciphertext' in encrypted
    assert 'tag' in encrypted
    assert 'combined' in encrypted

    decrypted_bytes = cipher.decrypt(encrypted)
    assert decrypted_bytes.decode('utf-8') == plaintext


def test_aes_gcm_invalid_key_length():
    with pytest.raises(ValueError):
        AESGCMCipher(b"short_key_16byte")


def test_aes_gcm_tamper_detection():
    key = os.urandom(32)
    cipher = AESGCMCipher(key)

    encrypted = cipher.encrypt("Secret Blockchain Payload")
    tampered_combined = bytearray(encrypted['combined'])
    tampered_combined[0] ^= 0xFF  # Tamper first byte

    with pytest.raises(ValueError, match="Decryption failed"):
        cipher.decrypt({'nonce': encrypted['nonce'], 'combined': bytes(tampered_combined)})
