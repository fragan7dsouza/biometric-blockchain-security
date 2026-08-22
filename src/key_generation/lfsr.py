"""
Linear Feedback Shift Register (LFSR) Submodule.
Provides configurable Galois/Fibonacci LFSR bit stream generation,
as well as the reference paper's 8-register (X0..X7) modulus-256 subsequence generator.
"""

import numpy as np
from typing import Tuple, List, Union, Optional
from src.config import LFSRConfig


class LFSRBitGenerator:
    """
    Galois/Fibonacci Linear Feedback Shift Register (LFSR).
    Generates pseudo-random bit stream from a given initial state and feedback polynomial.
    """

    def __init__(
        self,
        register_size: int = 32,
        taps: Tuple[int, ...] = (32, 31, 29, 1),
        seed_state: int = 0x12345678
    ):
        self.register_size = register_size
        self.taps = taps
        # Ensure seed state is non-zero and within register size bounds
        mask = (1 << register_size) - 1
        self.initial_state = (seed_state & mask) if (seed_state & mask) != 0 else 0x1
        self.state = self.initial_state

    def reset(self):
        """Resets register state back to initial seed."""
        self.state = self.initial_state

    def step(self) -> int:
        """
        Advances LFSR by one clock cycle and returns output bit (LSB).
        Galois LFSR feedback computation.
        """
        out_bit = self.state & 1
        self.state >>= 1
        if out_bit:
            # Feedback mask from taps
            feedback_mask = 0
            for tap in self.taps:
                feedback_mask |= (1 << (self.register_size - tap))
            self.state ^= feedback_mask
        return out_bit

    def generate_bits(self, length: int) -> np.ndarray:
        """Generates array of 'length' bits (0s and 1s)."""
        bits = np.zeros(length, dtype=np.uint8)
        for i in range(length):
            bits[i] = self.step()
        return bits

    def generate_bytes(self, num_bytes: int) -> bytes:
        """Generates byte sequence from LFSR bit stream."""
        raw_bits = self.generate_bits(num_bytes * 8)
        byte_list = []
        for i in range(num_bytes):
            byte_val = 0
            for b in range(8):
                byte_val = (byte_val << 1) | raw_bits[i * 8 + b]
            byte_list.append(byte_val)
        return bytes(byte_list)


class PaperLFSRSubsequenceGenerator:
    """
    Implements reference paper LFSR mechanism (Sannidhan et al., Section 4.4, Fig. 4).
    Operates on 8 registers (X0..X7) with modulus-256 arithmetic to produce subsequences.
    """

    def __init__(self, num_registers: int = 8, modulus: int = 256):
        self.num_registers = num_registers
        self.modulus = modulus

    def generate_subsequences(
        self,
        seed_features: np.ndarray,
        num_iterations: int = 1287
    ) -> List[np.ndarray]:
        """
        Generates paper-style subsequences from feature vector inputs.
        Input seed_features should contain at least 8 numerical values.
        """
        if len(seed_features) < self.num_registers:
            # Pad with repeating values if fewer than 8
            padded = np.pad(seed_features, (0, max(0, self.num_registers - len(seed_features))), mode='wrap')
        else:
            padded = seed_features[:self.num_registers].copy()

        # Convert to 8 integer registers X0..X7 in range [0, 255]
        registers = np.mod(np.abs(np.round(padded * 100).astype(int)), self.modulus)

        subsequences = []
        for it in range(num_iterations):
            # Even-numbered registers undergo modulus-256 addition and update
            even_sum = int(np.sum(registers[0::2])) % self.modulus
            # Circular shift registers right
            last_val = (registers[-1] + even_sum + it) % self.modulus
            registers[1:] = registers[:-1]
            registers[0] = last_val
            subsequences.append(registers.copy())

        return subsequences
