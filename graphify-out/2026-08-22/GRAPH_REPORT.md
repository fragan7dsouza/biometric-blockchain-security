# Graph Report - biometric-blockchain-security  (2026-08-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 253 nodes · 432 edges · 16 communities (9 shown, 7 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `62b970d2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Blockchain
- pipeline.py
- BiometricBlockchainPipeline
- LFSRBitGenerator
- HKDFKeyDeriver
- GeneticAlgorithmOptimizer
- AESGCMCipher
- FaceDetector
- ._generate_canonical_face_landmarks
- biometric/__init__.py
- blockchain/__init__.py
- encryption/__init__.py
- evaluation/__init__.py
- src/__init__.py
- key_generation/__init__.py
- optimization/__init__.py

## God Nodes (most connected - your core abstractions)
1. `BiometricBlockchainPipeline` - 23 edges
2. `Blockchain` - 21 edges
3. `LandmarkExtractor` - 19 edges
4. `Transaction` - 16 edges
5. `GeneticAlgorithmOptimizer` - 16 edges
6. `FeatureNormalizer` - 14 edges
7. `LFSRBitGenerator` - 14 edges
8. `AESGCMCipher` - 13 edges
9. `Block` - 11 edges
10. `BlockchainVerifier` - 11 edges

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

## Communities (16 total, 7 thin omitted)

### Community 0 - "Blockchain"
Cohesion: 0.06
Nodes (27): Block, Blockchain, Any, Simulated Blockchain Submodule. Implements Transaction, Block, and Blockchain…, Manages the chain of blocks, mining, transaction recording, and chain…, Creates the initial Genesis block., Represents a metadata-only transaction on the blockchain. Raw facial biometrics…, Adds transaction to pending list. (+19 more)

### Community 1 - "pipeline.py"
Cohesion: 0.07
Nodes (39): AppConfig, BiometricConfig, BlockchainConfig, Centralized Configuration Module for Biometric-Blockchain Security System.…, calculate_average_pearson_correlation(), calculate_pearson_correlation(), ndarray, Pearson Correlation Coefficient Evaluation Submodule. Computes pair-wise… (+31 more)

### Community 2 - "BiometricBlockchainPipeline"
Cohesion: 0.10
Nodes (26): main(), Main Command Line Interface (CLI) for Biometric-Blockchain Security System.…, Executable script for running full statistical randomness and baseline…, run(), Executable script for executing the full biometric-blockchain pipeline…, run(), LandmarkExtractor, Facial Landmark Extraction Submodule. Extracts 106 facial landmark coordinates… (+18 more)

### Community 3 - "LFSRBitGenerator"
Cohesion: 0.11
Nodes (16): LFSRConfig, LFSRBitGenerator, PaperLFSRSubsequenceGenerator, ndarray, Linear Feedback Shift Register (LFSR) Submodule. Provides configurable…, Galois/Fibonacci Linear Feedback Shift Register (LFSR). Generates pseudo-random…, Resets register state back to initial seed., Advances LFSR by one clock cycle and returns output bit (LSB). Galois LFSR… (+8 more)

### Community 4 - "HKDFKeyDeriver"
Cohesion: 0.12
Nodes (15): CryptographicConfig, HKDFKeyDeriver, Cryptographic Key Derivation Function (KDF) Submodule. Uses HKDF-SHA256 (RFC…, Derives cryptographically strong, uniform 256-bit symmetric keys from…, Derives a 256-bit (32-byte) AES key from input key material (ikm). Args: ikm:…, BiometricSeedGenerator, ndarray, Biometric Seed Generation Submodule. Serializes GA-optimized biometric features… (+7 more)

### Community 5 - "GeneticAlgorithmOptimizer"
Cohesion: 0.20
Nodes (10): GAConfig, GeneticAlgorithmOptimizer, ndarray, Runs the Genetic Algorithm optimization over subject capture datasets. Returns:…, Genetic Algorithm for optimizing biometric landmark feature vectors.…, Applies binary mask to select features., Computes multi-objective fitness for a given binary chromosome mask: Fitness =…, Unit tests for Genetic Algorithm Optimization Submodule. (+2 more)

### Community 6 - "AESGCMCipher"
Cohesion: 0.15
Nodes (11): AESGCMCipher, AES-256-GCM Authenticated Encryption Submodule. Provides authenticated…, Handles AES-256-GCM authenticated encryption and decryption., Encrypts plaintext using AES-256-GCM. Args: plaintext: Text string or raw bytes…, Decrypts AES-256-GCM encrypted payload and verifies authentication tag. Args:…, Any, Executes complete pipeline: Biometrics -> Landmarks -> Normalization -> GA ->…, Unit tests for AES-256-GCM Authenticated Encryption Submodule. (+3 more)

### Community 7 - "FaceDetector"
Cohesion: 0.20
Nodes (7): FaceDetector, ndarray, Face Detection and Alignment Submodule. Handles face bounding box detection and…, Detects faces in images and extracts ROI / bounding boxes. Supports OpenCV…, Detect face bounding box in image. Returns: (success, (x, y, w, h)), Crops and resizes image to target dimension., test_face_detector_synthetic()

### Community 8 - "._generate_canonical_face_landmarks"
Cohesion: 0.32
Nodes (5): RandomState, ndarray, Extracts 106 facial landmarks from an image. Returns: (success: bool,…, Generates synthetic 106 facial landmarks for a specific subject ID. Allows…, Generates structured 106 2D points following facial anatomy.

## Knowledge Gaps
- **2 isolated node(s):** `BiometricConfig`, `BlockchainConfig`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BiometricBlockchainPipeline` connect `BiometricBlockchainPipeline` to `Blockchain`, `pipeline.py`, `LFSRBitGenerator`, `HKDFKeyDeriver`, `GeneticAlgorithmOptimizer`, `AESGCMCipher`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `Blockchain` connect `Blockchain` to `pipeline.py`, `BiometricBlockchainPipeline`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `LandmarkExtractor` connect `BiometricBlockchainPipeline` to `._generate_canonical_face_landmarks`, `pipeline.py`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `BiometricBlockchainPipeline` (e.g. with `LandmarkExtractor` and `FeatureNormalizer`) actually correct?**
  _`BiometricBlockchainPipeline` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Blockchain` (e.g. with `BlockchainVerifier` and `BiometricBlockchainPipeline`) actually correct?**
  _`Blockchain` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `GeneticAlgorithmOptimizer` (e.g. with `GAConfig` and `BiometricBlockchainPipeline`) actually correct?**
  _`GeneticAlgorithmOptimizer` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `BiometricConfig`, `BlockchainConfig` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._