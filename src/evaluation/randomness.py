"""
Statistical Randomness Evaluation Submodule.
Implements Runs Test (Z-statistic), Chi-Square Uniformity Test, and NIST Monobit Frequency Test.
"""

import math
import numpy as np
from scipy import stats
from typing import Tuple, Dict, Any, Union


def runs_test(sequence: Union[np.ndarray, bytes, list]) -> Tuple[float, float, bool]:
    """
    Performs the Wald-Wolfowitz Runs Test for randomness on a binary sequence.

    Returns:
        (z_stat: float, p_value: float, is_random: bool at alpha=0.05)
    """
    if isinstance(sequence, bytes):
        bits = np.unpackbits(np.frombuffer(sequence, dtype=np.uint8))
    else:
        bits = np.array(sequence).flatten()

    n = len(bits)
    if n < 10:
        return 0.0, 1.0, True

    # Convert to binary elements (+1 / -1) or (0 / 1)
    n1 = np.sum(bits == 1)
    n0 = np.sum(bits == 0)

    if n0 == 0 or n1 == 0:
        return 0.0, 0.0, False

    # Count runs (number of contiguous blocks of same value)
    runs = 1 + np.sum(bits[1:] != bits[:-1])

    # Expected runs and variance
    mean_runs = 1.0 + (2.0 * n0 * n1) / n
    var_runs = (2.0 * n0 * n1 * (2.0 * n0 * n1 - n)) / (n**2 * (n - 1.0))

    if var_runs <= 0:
        return 0.0, 1.0, True

    # Z-statistic with continuity correction
    z_stat = (runs - mean_runs) / math.sqrt(var_runs)
    p_value = 2.0 * (1.0 - stats.norm.cdf(abs(z_stat)))

    is_random = abs(z_stat) < 1.96  # 95% confidence level
    return float(z_stat), float(p_value), is_random


def chi_square_uniformity_test(sequence: Union[np.ndarray, bytes], num_bins: int = 16) -> Tuple[float, float, bool]:
    """
    Performs Chi-Square Uniformity Test on a numerical byte/int sequence.

    Returns:
        (chi_stat: float, p_value: float, is_uniform: bool at alpha=0.05)
    """
    if isinstance(sequence, bytes):
        arr = np.frombuffer(sequence, dtype=np.uint8)
    else:
        arr = np.array(sequence).flatten()

    if len(arr) == 0:
        return 0.0, 1.0, True

    observed, _ = np.histogram(arr, bins=num_bins)
    expected = np.full(num_bins, len(arr) / float(num_bins))

    chi_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)
    is_uniform = p_value > 0.05
    return float(chi_stat), float(p_value), is_uniform


def nist_monobit_frequency_test(sequence: Union[np.ndarray, bytes]) -> Tuple[float, float, bool]:
    """
    NIST SP 800-22 Frequency (Monobit) Test.
    Tests whether the ratio of 1s and 0s is approximately equal.

    Returns:
        (s_obs: float, p_value: float, passes: bool at alpha=0.01)
    """
    if isinstance(sequence, bytes):
        bits = np.unpackbits(np.frombuffer(sequence, dtype=np.uint8))
    else:
        bits = np.array(sequence).flatten()

    n = len(bits)
    if n == 0:
        return 0.0, 1.0, True

    # Transform 0 -> -1 and 1 -> +1
    x_i = np.where(bits == 1, 1, -1)
    s_n = np.sum(x_i)
    s_obs = abs(s_n) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2.0))

    passes = p_value >= 0.01
    return float(s_obs), float(p_value), passes
