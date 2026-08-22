"""
Unified System Pipeline and Comparative Architecture Submodule.
Orchestrates end-to-end processing from biometric image to blockchain integrity verification.
Runs baseline comparisons against traditional and paper methodologies.
"""

import hashlib
import numpy as np
from typing import Dict, Any, Tuple, Optional, List

from src.config import AppConfig, DEFAULT_CONFIG
from src.biometric.landmark_extraction import LandmarkExtractor
from src.biometric.preprocessing import FeatureNormalizer
from src.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from src.key_generation.seed_generator import BiometricSeedGenerator
from src.key_generation.lfsr import LFSRBitGenerator, PaperLFSRSubsequenceGenerator
from src.key_generation.key_derivation import HKDFKeyDeriver
from src.encryption.aes import AESGCMCipher
from src.blockchain.blockchain import Blockchain, Transaction
from src.blockchain.verifier import BlockchainVerifier

from src.evaluation.entropy import calculate_shannon_entropy_bytes, calculate_shannon_entropy_bits
from src.evaluation.randomness import runs_test, chi_square_uniformity_test, nist_monobit_frequency_test
from src.evaluation.hamming_distance import calculate_hamming_distance


class BiometricBlockchainPipeline:
    """
    End-to-End Integrated Biometric Blockchain Security System.
    """

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.extractor = LandmarkExtractor(num_landmarks=self.config.biometric.num_landmarks)
        self.normalizer = FeatureNormalizer(
            target_bounds=self.config.biometric.coord_bounds,
            quantization_bits=self.config.biometric.quantization_bits
        )
        self.ga_optimizer = GeneticAlgorithmOptimizer(config=self.config.ga, seed=self.config.random_seed)
        self.seed_generator = BiometricSeedGenerator(salt=self.config.crypto.salt)
        self.hkdf_deriver = HKDFKeyDeriver(
            salt=self.config.crypto.salt,
            info=self.config.crypto.info,
            key_size=self.config.crypto.key_size_bytes
        )
        self.blockchain = Blockchain(difficulty=self.config.blockchain.difficulty)
        self.verifier = BlockchainVerifier(self.blockchain)

    def _build_ga_training_dataset(self, primary_norm_features: np.ndarray) -> Dict[int, List[np.ndarray]]:
        """
        Constructs a multi-subject multi-capture dataset for GA optimization.
        Ensures intra-class stability and inter-class separation fitness components
        are meaningfully evaluated during feature selection.
        """
        dataset: Dict[int, List[np.ndarray]] = {}

        # Primary Subject (ID 1): 5 capture perturbations
        primary_captures = []
        rng = np.random.RandomState(42)
        for _ in range(5):
            noise = rng.normal(0, 0.015, size=primary_norm_features.shape)
            perturbed = primary_norm_features + noise
            primary_captures.append(perturbed)
        dataset[1] = primary_captures

        # Reference Subjects (IDs 2..5): 5 captures each
        for sub in range(2, 6):
            sub_caps = []
            for cap_idx in range(5):
                lm = self.extractor.generate_synthetic_subject_landmarks(
                    subject_id=sub,
                    capture_index=cap_idx,
                    noise_level=0.02
                )
                norm_f = self.normalizer.normalize_landmarks(lm)
                sub_caps.append(norm_f)
            dataset[sub] = sub_caps

        return dataset

    def process_end_to_end(
        self,
        image_or_landmarks: Any,
        plaintext_data: str,
        user_id: str = "user_001",
        tx_id: str = "tx_0001"
    ) -> Dict[str, Any]:
        """
        Executes complete pipeline:
        Biometrics -> Landmarks -> Normalization -> GA -> Seed -> LFSR -> HKDF -> AES-GCM -> Blockchain -> Verification.
        """
        # 1. Landmark Extraction
        if isinstance(image_or_landmarks, np.ndarray) and image_or_landmarks.ndim == 2 and image_or_landmarks.shape[1] == 2:
            landmarks = image_or_landmarks
        else:
            _, landmarks = self.extractor.extract_landmarks(image_or_landmarks)

        # 2. Feature Normalization
        norm_features = self.normalizer.normalize_landmarks(landmarks)

        # 3. GA Feature Selection Mask (using multi-subject dataset for non-degenerate fitness)
        subject_dict = self._build_ga_training_dataset(norm_features)
        best_chromosome, ga_history = self.ga_optimizer.optimize(
            feature_dim=len(norm_features),
            subject_captures=subject_dict
        )
        ga_features = self.ga_optimizer.apply_mask(norm_features, best_chromosome)

        # 4. Seed Generation
        seed_bytes = self.seed_generator.generate_seed_bytes(ga_features)
        seed_int = self.seed_generator.generate_seed_integer(ga_features)

        # 5. LFSR Bit Sequence Expansion
        lfsr = LFSRBitGenerator(
            register_size=self.config.lfsr.register_size,
            taps=self.config.lfsr.taps,
            seed_state=seed_int
        )
        lfsr_bytes = lfsr.generate_bytes(64)  # Generate 64 bytes (512 bits) of material

        # 6. HKDF-SHA256 Key Derivation (derived 256-bit AES key)
        aes_key = self.hkdf_deriver.derive_key(lfsr_bytes)

        # 7. AES-256-GCM Encryption
        cipher = AESGCMCipher(aes_key)
        encrypted_result = cipher.encrypt(plaintext_data)

        # 8. Blockchain Record Creation
        ciphertext_hash = self.verifier.compute_ciphertext_hash(encrypted_result['combined'])
        user_id_hash = hashlib.sha256(user_id.encode('utf-8')).hexdigest()

        tx = Transaction(
            tx_id=tx_id,
            user_id_hash=user_id_hash,
            ciphertext_hash=ciphertext_hash,
            encrypted_data_ref=f"ref://data/{tx_id}"
        )
        self.blockchain.add_transaction(tx)
        mined_block = self.blockchain.mine_pending_transactions()

        # 9. Integrity Verification
        is_valid, status_msg, metadata = self.verifier.verify_ciphertext_integrity(
            tx_id=tx_id,
            ciphertext_bytes=encrypted_result['combined']
        )

        # 10. Decryption verification
        decrypted_bytes = cipher.decrypt(encrypted_result)
        decrypted_str = decrypted_bytes.decode('utf-8')

        return {
            'landmarks_count': len(landmarks),
            'normalized_features_dim': len(norm_features),
            'ga_selected_dim': len(ga_features),
            'ga_history': ga_history,
            'lfsr_bytes_len': len(lfsr_bytes),
            'aes_key_len': len(aes_key),
            'encrypted_result': encrypted_result,
            'ciphertext_hash': ciphertext_hash,
            'tx_id': tx_id,
            'block_index': mined_block.index,
            'block_hash': mined_block.hash,
            'verification_valid': is_valid,
            'verification_msg': status_msg,
            'decrypted_str': decrypted_str,
            'decryption_correct': (decrypted_str == plaintext_data)
        }

    def run_baseline_comparisons(
        self,
        sample_landmarks: np.ndarray
    ) -> Dict[str, Dict[str, Any]]:
        """
        Runs comparative benchmarks across 5 architectures:
        - Baseline A: Raw Features -> SHA-256
        - Baseline B: Raw Features -> HKDF-SHA256
        - Baseline C: GA Features -> HKDF-SHA256
        - Base Paper: Landmarks -> GA -> LFSR Subsequences (Registers X0..X7)
        - Proposed System: Landmarks -> Normalization -> GA -> Seed -> LFSR -> HKDF -> AES-GCM -> Blockchain
        """
        norm_features = self.normalizer.normalize_landmarks(sample_landmarks)
        subject_dict = self._build_ga_training_dataset(norm_features)

        # Optimize GA features with proper multi-subject dataset
        chrom, _ = self.ga_optimizer.optimize(len(norm_features), subject_dict)
        ga_feats = self.ga_optimizer.apply_mask(norm_features, chrom)

        # Generate multi-key streams (100 keys x 32 bytes = 3,200 bytes) for statistical evaluation
        stream_a = b''.join([hashlib.sha256(norm_features.tobytes() + i.to_bytes(4, 'big')).digest() for i in range(100)])
        stream_b = b''.join([self.hkdf_deriver.derive_key(norm_features.tobytes(), custom_info=f"hkdf_info_{i}".encode()) for i in range(100)])
        stream_c = b''.join([self.hkdf_deriver.derive_key(ga_feats.tobytes(), custom_info=f"ga_info_{i}".encode()) for i in range(100)])

        # Proposed System Stream (LFSR expansion + HKDF)
        seed_int = self.seed_generator.generate_seed_integer(ga_feats)
        lfsr = LFSRBitGenerator(seed_state=seed_int)
        stream_proposed = b''.join([self.hkdf_deriver.derive_key(lfsr.generate_bytes(64), custom_info=f"proposed_{i}".encode()) for i in range(100)])

        # Base Paper: LFSR 8-register Subsequences
        paper_lfsr = PaperLFSRSubsequenceGenerator()
        paper_seqs = paper_lfsr.generate_subsequences(norm_features, num_iterations=1287)
        paper_flat = np.array(paper_seqs).flatten()

        # Metrics computation
        results = {}
        for name, stream in [
            ('Baseline_A_SHA256', stream_a),
            ('Baseline_B_HKDF', stream_b),
            ('Baseline_C_GA_HKDF', stream_c),
            ('Proposed_GA_LFSR_HKDF', stream_proposed)
        ]:
            entropy = calculate_shannon_entropy_bytes(stream)
            z_stat, p_val, is_rand = runs_test(stream)
            results[name] = {
                'entropy_bits_per_byte': round(entropy, 4),
                'runs_z_stat': round(z_stat, 4),
                'runs_p_value': round(p_val, 4),
                'is_random': is_rand,
                'stream_bytes_len': len(stream)
            }

        # Add Base Paper evaluation
        paper_entropy = calculate_shannon_entropy_bits(paper_flat)
        paper_z, paper_p, paper_rand = runs_test(paper_flat[:1000])
        results['Base_Paper_GA_LFSR'] = {
            'entropy_bits_per_symbol': round(paper_entropy, 4),
            'runs_z_stat': round(paper_z, 4),
            'runs_p_value': round(paper_p, 4),
            'is_random': paper_rand,
            'total_subsequences': len(paper_seqs)
        }

        return results
