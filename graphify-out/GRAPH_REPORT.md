# Graph Report - biometric-blockchain-security  (2026-08-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 257 nodes · 409 edges · 19 communities (11 shown, 8 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62b970d2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Blockchain
- LandmarkExtractor
- test_evaluation.py
- LFSRBitGenerator
- config.py
- GeneticAlgorithmOptimizer
- AESGCMCipher
- FaceDetector
- ._generate_canonical_face_landmarks
- .normalize_landmarks
- .verify_ciphertext_integrity
- biometric/__init__.py
- blockchain/__init__.py
- encryption/__init__.py
- evaluation/__init__.py
- src/__init__.py
- key_generation/__init__.py
- optimization/__init__.py
- Any

## God Nodes (most connected - your core abstractions)
1. `Blockchain` - 19 edges
2. `LandmarkExtractor` - 19 edges
3. `Transaction` - 14 edges
4. `GeneticAlgorithmOptimizer` - 14 edges
5. `BiometricBlockchainPipeline` - 13 edges
6. `FeatureNormalizer` - 12 edges
7. `LFSRBitGenerator` - 12 edges
8. `Block` - 11 edges
9. `AESGCMCipher` - 11 edges
10. `BlockchainVerifier` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_landmark_extractor_synthetic()` --calls--> `LandmarkExtractor`  [EXTRACTED]
  tests/test_biometric.py → src/biometric/landmark_extraction.py
- `test_lfsr_bit_generator_determinism()` --calls--> `LFSRBitGenerator`  [EXTRACTED]
  tests/test_lfsr.py → src/key_generation/lfsr.py
- `test_lfsr_bytes_generation()` --calls--> `LFSRBitGenerator`  [EXTRACTED]
  tests/test_lfsr.py → src/key_generation/lfsr.py
- `test_paper_lfsr_subsequence_generator()` --calls--> `PaperLFSRSubsequenceGenerator`  [EXTRACTED]
  tests/test_lfsr.py → src/key_generation/lfsr.py
- `test_hkdf_different_ikm_produces_different_keys()` --calls--> `HKDFKeyDeriver`  [EXTRACTED]
  tests/test_key_derivation.py → src/key_generation/key_derivation.py

## Import Cycles
- None detected.

## Communities (19 total, 8 thin omitted)

### Community 0 - "Blockchain"
Cohesion: 0.07
Nodes (25): AppConfig, Block, Blockchain, Any, Simulated Blockchain Submodule. Implements Transaction, Block, and Blockchain…, Manages the chain of blocks, mining, transaction recording, and chain…, Creates the initial Genesis block., Represents a metadata-only transaction on the blockchain. Raw facial biometrics… (+17 more)

### Community 1 - "LandmarkExtractor"
Cohesion: 0.11
Nodes (25): main(), Main Command Line Interface (CLI) for Biometric-Blockchain Security System.…, Executable script for running full statistical randomness and baseline…, run(), Executable script for executing the full biometric-blockchain pipeline…, run(), LandmarkExtractor, Facial Landmark Extraction Submodule. Extracts 106 2D facial landmark… (+17 more)

### Community 2 - "test_evaluation.py"
Cohesion: 0.09
Nodes (30): calculate_average_pearson_correlation(), calculate_pearson_correlation(), ndarray, Pearson Correlation Coefficient Evaluation Submodule. Computes pair-wise…, Computes Pearson correlation coefficient between two 1D numerical sequences., Calculates average off-diagonal Pearson correlation across a list of generated…, calculate_shannon_entropy_bits(), calculate_shannon_entropy_bytes() (+22 more)

### Community 3 - "LFSRBitGenerator"
Cohesion: 0.08
Nodes (21): Any, LFSRConfig, LFSRBitGenerator, PaperLFSRSubsequenceGenerator, ndarray, Linear Feedback Shift Register (LFSR) Submodule. Provides configurable…, Galois/Fibonacci Linear Feedback Shift Register (LFSR). Generates pseudo-random…, Resets register state back to initial seed. (+13 more)

### Community 4 - "config.py"
Cohesion: 0.10
Nodes (19): AppConfig, BiometricConfig, BlockchainConfig, CryptographicConfig, Centralized Configuration Module for Biometric-Blockchain Security System.…, HKDFKeyDeriver, Cryptographic Key Derivation Function (KDF) Submodule. Uses HKDF-SHA256 (RFC…, Derives cryptographically strong, uniform 256-bit symmetric keys from… (+11 more)

### Community 5 - "GeneticAlgorithmOptimizer"
Cohesion: 0.18
Nodes (11): GAConfig, GeneticAlgorithmOptimizer, ndarray, Genetic Algorithm Optimization Module. Implements binary feature selection mask…, Runs the Genetic Algorithm optimization over subject capture datasets. Returns:…, Genetic Algorithm for optimizing biometric landmark feature vectors.…, Applies binary mask to select features., Computes multi-objective fitness for a given binary chromosome mask: Fitness =… (+3 more)

### Community 6 - "AESGCMCipher"
Cohesion: 0.19
Nodes (9): AESGCMCipher, AES-256-GCM Authenticated Encryption Submodule. Provides authenticated…, Handles AES-256-GCM authenticated encryption and decryption., Encrypts plaintext using AES-256-GCM. Args: plaintext: Text string or raw bytes…, Decrypts AES-256-GCM encrypted payload and verifies authentication tag. Args:…, Unit tests for AES-256-GCM Authenticated Encryption Submodule., test_aes_gcm_encrypt_decrypt(), test_aes_gcm_invalid_key_length() (+1 more)

### Community 7 - "FaceDetector"
Cohesion: 0.20
Nodes (7): FaceDetector, ndarray, Face Detection and Alignment Submodule. Handles face bounding box detection and…, Detects faces in images and extracts ROI / bounding boxes. Supports OpenCV…, Detect face bounding box in image. Returns: (success, (x, y, w, h)), Crops and resizes image to target dimension., test_face_detector_synthetic()

### Community 8 - "._generate_canonical_face_landmarks"
Cohesion: 0.32
Nodes (5): RandomState, ndarray, Generates structured 106 2D points following facial anatomy., Extracts 106 facial landmarks from an image. Returns: (success: bool,…, Generates synthetic 106 facial landmarks for a specific subject ID. Allows…

### Community 9 - ".normalize_landmarks"
Cohesion: 0.40
Nodes (3): ndarray, Normalizes landmarks (shape: N x 2, e.g., 106 x 2). Returns: Normalized 1D…, Quantizes floating-point feature vector to fixed-point integer representation.

### Community 10 - ".verify_ciphertext_integrity"
Cohesion: 0.40
Nodes (3): Any, Computes SHA-256 hash of raw ciphertext bytes., Verifies if ciphertext_bytes match the metadata stored in tx_id on the…

## Knowledge Gaps
- **3 isolated node(s):** `AppConfig`, `BiometricConfig`, `BlockchainConfig`
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LandmarkExtractor` connect `LandmarkExtractor` to `._generate_canonical_face_landmarks`, `Blockchain`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `BiometricBlockchainPipeline` connect `LandmarkExtractor` to `Blockchain`, `LFSRBitGenerator`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **What connects `AppConfig`, `BiometricConfig`, `BlockchainConfig` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Blockchain` be split into smaller, more focused modules?**
  _Cohesion score 0.06914893617021277 - nodes in this community are weakly interconnected._
- **Should `LandmarkExtractor` be split into smaller, more focused modules?**
  _Cohesion score 0.10793650793650794 - nodes in this community are weakly interconnected._
- **Should `test_evaluation.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0873440285204991 - nodes in this community are weakly interconnected._
- **Should `LFSRBitGenerator` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._