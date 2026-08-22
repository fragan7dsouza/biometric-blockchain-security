"""
Centralized Configuration Module for Biometric-Blockchain Security System.
Contains default parameters for biometric extraction, GA optimization,
LFSR expansion, HKDF derivation, AES encryption, and blockchain verification.
"""

from dataclasses import dataclass, field
from typing import Tuple, List, Optional
import os


@dataclass
class BiometricConfig:
    num_landmarks: int = 106
    input_shape: Tuple[int, int] = (224, 224)
    coord_bounds: Tuple[float, float] = (-1.0, 1.0)
    quantization_bits: int = 16


@dataclass
class GAConfig:
    population_size: int = 50
    generations: int = 30
    crossover_rate: float = 0.8
    mutation_rate: float = 0.05
    tournament_size: int = 3
    elitism_count: int = 2
    weights: Tuple[float, float, float, float] = (0.35, 0.35, 0.15, 0.15)  # intra, inter, entropy, corr


@dataclass
class LFSRConfig:
    register_size: int = 32
    # Standard primitive polynomial for 32-bit: x^32 + x^31 + x^29 + x^1 + 1
    taps: Tuple[int, ...] = (32, 31, 29, 1)
    sequence_length: int = 512  # Number of bits to generate
    num_registers: int = 8      # Reference paper 8-register structure (X0..X7)
    modulus: int = 256


@dataclass
class CryptographicConfig:
    kdf_algorithm: str = "HKDF-SHA256"
    salt: bytes = b"biometric-blockchain-salt-v1"
    info: bytes = b"aes-key-derivation-context"
    key_size_bytes: int = 32  # 256 bits for AES-256
    nonce_size_bytes: int = 12  # Standard 96-bit nonce for GCM
    tag_size_bytes: int = 16    # Standard 128-bit GCM tag


@dataclass
class BlockchainConfig:
    difficulty: int = 2
    reward: float = 1.0
    chain_file: str = "data/processed/blockchain_ledger.json"


@dataclass
class AppConfig:
    random_seed: int = 42
    data_dir: str = "data"
    results_dir: str = "results"
    docs_dir: str = "docs"

    biometric: BiometricConfig = field(default_factory=BiometricConfig)
    ga: GAConfig = field(default_factory=GAConfig)
    lfsr: LFSRConfig = field(default_factory=LFSRConfig)
    crypto: CryptographicConfig = field(default_factory=CryptographicConfig)
    blockchain: BlockchainConfig = field(default_factory=BlockchainConfig)


# Global default configuration instance
DEFAULT_CONFIG = AppConfig()
