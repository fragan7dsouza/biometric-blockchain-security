# System Architecture

## Overview
The Biometric-Blockchain Security System integrates facial landmark extraction, rigid Procrustes feature normalization, Genetic Algorithm (GA) feature selection optimization, Linear Feedback Shift Register (LFSR) pseudo-random expansion, HKDF-SHA256 key derivation, AES-256-GCM authenticated encryption, and a simulated Proof-of-Work Blockchain ledger for integrity verification.

## Component Breakdown

```
[Face Image / Synthetic Capture]
             │
             ▼
[LandmarkExtractor] ──► Extracts 106 2D facial landmark coordinates (x_i, y_i)
             │
             ▼
[FeatureNormalizer] ──► Procrustes alignment (Centroid subtraction + RMS scale + SVD rotation)
             │
             ▼
[GeneticAlgorithm]  ──► Binary selection mask optimizing multi-objective fitness
             │
             ▼
[SeedGenerator]     ──► Canonical float serialization + SHA-256 hashing
             │
             ▼
[LFSRGenerator]     ──► Galois LFSR bit-sequence expansion (512 bits)
             │
             ▼
[HKDFKeyDeriver]    ──► RFC 5869 HKDF-SHA256 derives 256-bit symmetric AES key
             │
             ▼
[AESGCMCipher]      ──► Encrypts payload with 96-bit nonce & 128-bit auth tag
             │
      ┌──────┴──────┐
      ▼             ▼
[Ciphertext]  [Blockchain] ──► Stores metadata: User ID hash, Ciphertext SHA-256, Tx ID
```

### 1. Biometric Feature Extraction & Normalization (`src/biometric/`)
- **Extractor**: Detects faces and extracts 106 canonical facial landmark points.
- **Normalizer**: Applies Procrustes alignment to ensure features are invariant to translation, scale, and head rotation.

### 2. Genetic Algorithm Optimization (`src/optimization/`)
- **Chromosome**: Binary array of size 212 selecting active landmark features.
- **Fitness Function**: Balances intra-class stability, inter-class separation, Shannon entropy, and feature correlation penalty.

### 3. Key Generation & Derivation (`src/key_generation/`)
- **Seed Generator**: Hashing normalized features to deterministic seed material.
- **LFSR**: Pseudo-random bit sequence expansion.
- **HKDF-SHA256**: Standards-compliant Key Derivation Function producing uniform 32-byte (256-bit) AES keys.

### 4. Authenticated Encryption (`src/encryption/`)
- **AES-256-GCM**: Symmetric encryption with 12-byte nonces and 16-byte authentication tags.

### 5. Blockchain Ledger & Verification (`src/blockchain/`)
- **Block & Chain**: Proof-of-Work blockchain (difficulty = 2).
- **Metadata Ledger**: Stores non-sensitive metadata (`user_id_hash`, `ciphertext_hash`, `encrypted_data_ref`).
- **Verifier**: Audits stored ciphertext against on-chain hash commitments.
