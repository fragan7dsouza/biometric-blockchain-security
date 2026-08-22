"""
Unit tests for Genetic Algorithm Optimization Submodule.
"""

import pytest
import numpy as np
from src.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from src.config import GAConfig


def test_ga_optimizer_initialization():
    config = GAConfig(population_size=10, generations=5)
    ga = GeneticAlgorithmOptimizer(config=config, seed=42)

    # Generate dummy features for 2 subjects
    sub_dict = {
        1: [np.random.rand(212), np.random.rand(212)],
        2: [np.random.rand(212), np.random.rand(212)]
    }

    best_chrom, history = ga.optimize(feature_dim=212, subject_captures=sub_dict)
    assert len(best_chrom) == 212
    assert len(history) == 5
    assert np.sum(best_chrom) >= 4


def test_ga_apply_mask():
    ga = GeneticAlgorithmOptimizer()
    feature_vector = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    mask = np.array([1, 0, 1, 0, 1])

    selected = ga.apply_mask(feature_vector, mask)
    assert len(selected) == 3
    assert np.array_equal(selected, np.array([1.0, 3.0, 5.0]))
