"""
Pearson Correlation Coefficient Evaluation Submodule.
Computes pair-wise Pearson correlation matrix and average correlation coefficient.
"""

import numpy as np
from typing import List, Tuple, Union


def calculate_pearson_correlation(seq1: np.ndarray, seq2: np.ndarray) -> float:
    """
    Computes Pearson correlation coefficient between two 1D numerical sequences.
    """
    if len(seq1) != len(seq2) or len(seq1) == 0:
        return 0.0

    s1 = seq1.astype(float)
    s2 = seq2.astype(float)

    std1 = np.std(s1)
    std2 = np.std(s2)

    if std1 < 1e-12 or std2 < 1e-12:
        return 0.0

    corr_matrix = np.corrcoef(s1, s2)
    return float(corr_matrix[0, 1])


def calculate_average_pearson_correlation(sequences: List[np.ndarray]) -> Tuple[float, np.ndarray]:
    """
    Calculates average off-diagonal Pearson correlation across a list of generated sequences.
    Returns:
        (avg_correlation, correlation_matrix)
    """
    if len(sequences) < 2:
        return 0.0, np.ones((1, 1))

    # Stack sequences into rows
    data_mat = np.array(sequences, dtype=float)
    corr_matrix = np.corrcoef(data_mat)

    # Replace NaNs with 0
    corr_matrix = np.nan_to_num(corr_matrix, nan=0.0)

    # Mask diagonal
    n = len(sequences)
    off_diag = corr_matrix[~np.eye(n, dtype=bool)]
    avg_corr = np.mean(np.abs(off_diag)) if len(off_diag) > 0 else 0.0

    return float(avg_corr), corr_matrix
