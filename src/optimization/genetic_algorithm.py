"""
Genetic Algorithm Optimization Module.
Implements binary feature selection mask chromosome, multi-objective fitness evaluation,
tournament selection, crossover, mutation, and elitism for biometric feature optimization.
"""

import numpy as np
from typing import Tuple, List, Dict, Any, Optional
from src.config import GAConfig


class GeneticAlgorithmOptimizer:
    """
    Genetic Algorithm for optimizing biometric landmark feature vectors.
    Chromosomes represent binary selection masks over feature vector indices.
    """

    def __init__(self, config: Optional[GAConfig] = None, seed: Optional[int] = 42):
        self.config = config or GAConfig()
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    def compute_fitness(
        self,
        chromosome: np.ndarray,
        subject_captures: Dict[int, List[np.ndarray]],
        weights: Tuple[float, float, float, float] = (0.35, 0.35, 0.15, 0.15)
    ) -> float:
        """
        Computes multi-objective fitness for a given binary chromosome mask:
        Fitness = w1 * F_intra + w2 * F_inter + w3 * F_entropy - w4 * F_corr

        Args:
            chromosome: Binary mask array of 0s and 1s.
            subject_captures: Dict mapping subject_id -> list of feature vectors.
            weights: (w_intra, w_inter, w_entropy, w_corr)
        """
        # Ensure chromosome has at least 4 active features
        active_indices = np.where(chromosome == 1)[0]
        if len(active_indices) < 4:
            return 0.001

        w_intra, w_inter, w_entropy, w_corr = weights

        # 1. Intra-class Stability (F_intra)
        intra_distances = []
        subject_means = {}
        for sub_id, captures in subject_captures.items():
            if len(captures) >= 2:
                sub_feats = [cap[active_indices] for cap in captures]
                mean_feat = np.mean(sub_feats, axis=0)
                subject_means[sub_id] = mean_feat
                for f in sub_feats:
                    intra_distances.append(np.linalg.norm(f - mean_feat))
            elif len(captures) == 1:
                subject_means[sub_id] = captures[0][active_indices]

        avg_intra_dist = np.mean(intra_distances) if intra_distances else 0.1
        f_intra = 1.0 / (1.0 + avg_intra_dist)  # Higher is better (lower intra distance)

        # 2. Inter-class Separation (F_inter)
        inter_distances = []
        sub_ids = list(subject_means.keys())
        for i in range(len(sub_ids)):
            for j in range(i + 1, len(sub_ids)):
                dist = np.linalg.norm(subject_means[sub_ids[i]] - subject_means[sub_ids[j]])
                inter_distances.append(dist)

        avg_inter_dist = np.mean(inter_distances) if inter_distances else 1.0
        f_inter = min(avg_inter_dist / (np.sqrt(len(active_indices)) + 1e-6), 1.0)  # Normalized

        # 3. Feature Subset Entropy (F_entropy)
        all_selected_feats = []
        for captures in subject_captures.values():
            for cap in captures:
                all_selected_feats.append(cap[active_indices])

        if len(all_selected_feats) > 1:
            data_mat = np.array(all_selected_feats)
            # Quantize values into 10 bins to compute Shannon entropy
            hist, _ = np.histogram(data_mat.flatten(), bins=10, density=True)
            hist = hist[hist > 0]
            shannon_entropy = -np.sum(hist * np.log2(hist))
            f_entropy = min(shannon_entropy / np.log2(10), 1.0)
        else:
            f_entropy = 0.5

        # 4. Correlation Penalty (F_corr)
        if len(all_selected_feats) > 2 and len(active_indices) > 1:
            data_mat = np.array(all_selected_feats)
            corr_matrix = np.abs(np.corrcoef(data_mat, rowvar=False))
            np.fill_diagonal(corr_matrix, 0)
            avg_corr = np.nanmean(corr_matrix) if not np.isnan(np.nanmean(corr_matrix)) else 0.0
            f_corr = avg_corr
        else:
            f_corr = 0.0

        fitness_score = (w_intra * f_intra) + (w_inter * f_inter) + (w_entropy * f_entropy) - (w_corr * f_corr)
        return float(max(fitness_score, 0.0001))

    def optimize(
        self,
        feature_dim: int,
        subject_captures: Dict[int, List[np.ndarray]]
    ) -> Tuple[np.ndarray, List[float]]:
        """
        Runs the Genetic Algorithm optimization over subject capture datasets.

        Returns:
            best_chromosome: Binary selection mask array of length feature_dim.
            history: List of best fitness score per generation.
        """
        pop_size = self.config.population_size
        generations = self.config.generations
        crossover_rate = self.config.crossover_rate
        mutation_rate = self.config.mutation_rate
        elitism_count = self.config.elitism_count

        # Initialize Population (random binary vectors with ~50% ones)
        population = self.rng.randint(0, 2, size=(pop_size, feature_dim))
        # Ensure no chromosome has zero active features
        for i in range(pop_size):
            if np.sum(population[i]) == 0:
                population[i, self.rng.choice(feature_dim, size=4, replace=False)] = 1

        history = []
        best_chromosome = population[0].copy()
        best_fitness = -1.0

        for gen in range(generations):
            fitness_scores = np.array([
                self.compute_fitness(chrom, subject_captures, self.config.weights)
                for chrom in population
            ])

            gen_best_idx = np.argmax(fitness_scores)
            gen_best_fit = fitness_scores[gen_best_idx]
            history.append(gen_best_fit)

            if gen_best_fit > best_fitness:
                best_fitness = gen_best_fit
                best_chromosome = population[gen_best_idx].copy()

            # Elitism: retain top individuals
            sorted_indices = np.argsort(fitness_scores)[::-1]
            new_population = [population[idx].copy() for idx in sorted_indices[:elitism_count]]

            # Breed remaining population
            while len(new_population) < pop_size:
                p1 = self._tournament_selection(population, fitness_scores)
                p2 = self._tournament_selection(population, fitness_scores)

                if self.rng.rand() < crossover_rate:
                    c1, c2 = self._uniform_crossover(p1, p2)
                else:
                    c1, c2 = p1.copy(), p2.copy()

                c1 = self._mutate(c1, mutation_rate)
                c2 = self._mutate(c2, mutation_rate)

                new_population.append(c1)
                if len(new_population) < pop_size:
                    new_population.append(c2)

            population = np.array(new_population[:pop_size])

        return best_chromosome, history

    def apply_mask(self, feature_vector: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Applies binary mask to select features."""
        active_indices = np.where(mask == 1)[0]
        if len(active_indices) == 0:
            return feature_vector
        return feature_vector[active_indices]

    def _tournament_selection(self, population: np.ndarray, fitness_scores: np.ndarray) -> np.ndarray:
        t_size = min(self.config.tournament_size, len(population))
        selected_indices = self.rng.choice(len(population), size=t_size, replace=False)
        best_in_t = selected_indices[np.argmax(fitness_scores[selected_indices])]
        return population[best_in_t].copy()

    def _uniform_crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        mask = self.rng.randint(0, 2, size=len(parent1))
        child1 = np.where(mask == 1, parent1, parent2)
        child2 = np.where(mask == 1, parent2, parent1)
        return child1, child2

    def _mutate(self, chromosome: np.ndarray, mutation_rate: float) -> np.ndarray:
        mutated = chromosome.copy()
        for i in range(len(mutated)):
            if self.rng.rand() < mutation_rate:
                mutated[i] = 1 - mutated[i]
        # Ensure at least 4 features selected
        if np.sum(mutated) < 4:
            mutated[self.rng.choice(len(mutated), size=4, replace=False)] = 1
        return mutated
