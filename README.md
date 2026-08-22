# Biometric-based Key Sequence Generation using Genetic Algorithm for Enhanced Blockchain Security

A research prototype implementing biometric feature extraction, rigid Procrustes normalization, Genetic Algorithm (GA) multi-objective optimization, Linear Feedback Shift Register (LFSR) expansion, HKDF-SHA256 key derivation, AES-256-GCM authenticated encryption, and simulated Proof-of-Work Blockchain integrity verification.

Based on and evaluating the reference research paper:
> **Reference Paper**: *MS Sannidhan, Jason Elroy Martis, KN Pallavi, Vinayakumar Ravi, HL Gururaj, Tahani Jaser Alahmadi. "Genetic algorithms and deep learning for unique facial landmark-based key generation." Computers and Electrical Engineering 118 (2024): 109427.*

---

## Objectives

1. **Objective 1**: Develop a secure cryptographic framework that generates dynamic, user-specific encryption keys from facial biometrics using genetic algorithms, ensuring high entropy, uniqueness, and robustness.
2. **Objective 2**: Utilize the generated cryptographic keys for encrypting data using authenticated encryption (AES-256-GCM), enhancing confidentiality and security, before integrating it into blockchain operations for immutable and decentralized data management.
3. **Objective 3**: Address vulnerabilities in traditional cryptographic systems by combining biometric-driven key generation, adaptive optimization techniques, and blockchain technology for secure and transparent transaction verification.

---

## System Architecture

```
FACE IMAGE / SYNTHETIC BIOMETRICS
               │
               ▼
     Face Detection & 106 Facial Landmark Extraction (MediaPipe / OpenCV / Synthetic Fallback)
               │
               ▼
  Feature Normalization (Translation, Scale, Rotation Invariance via Procrustes Alignment)
               │
               ▼
   Genetic Algorithm (Binary Feature Selection Mask & Multi-Objective Fitness Optimization)
               │
               ▼
     Biometric Seed Material (Canonical Float Serialization + SHA-256 Hash)
               │
               ▼
    LFSR Pseudo-Random Bit Sequence Expansion (Registers X0..X7, Configurable Polynomial)
               │
               ▼
  Cryptographic Key Derivation (HKDF-SHA256 → 256-bit AES Key)
               │
               ▼
 Authenticated Encryption (AES-256-GCM: Nonce, Ciphertext, Tag)
               │
      ┌────────┴────────┐
      ▼                 ▼
 Encrypted Data     Metadata (SHA-256 Hash of Ciphertext + User ID Commitment + Tx ID)
                        │
                        ▼
            Simulated Blockchain (Block Header, Hash Chain, Proof-of-Work)
                        │
                        ▼
         Integrity Verification & Tamper Detection
```

---

## Repository Structure

```
biometric-blockchain-security/
├── src/
│   ├── biometric/            # Landmark extraction & Procrustes normalization
│   ├── optimization/         # Genetic Algorithm binary feature selection
│   ├── key_generation/       # Seed generator, LFSR expansion & HKDF key derivation
│   ├── encryption/           # AES-256-GCM authenticated encryption
│   ├── blockchain/           # Block, Blockchain ledger & tamper verifier
│   ├── evaluation/           # Shannon entropy, Pearson correlation, Runs test, Hamming distance
│   ├── config.py             # Central configuration dataclasses
│   └── pipeline.py           # End-to-end integration & baseline comparisons
├── experiments/              # 5 Jupyter research notebooks
├── tests/                    # Comprehensive pytest test suite
├── docs/                     # Technical documentation (architecture, methodology, security)
├── scripts/                  # Executable scripts (run_pipeline.py, run_evaluation.py)
├── main.py                   # CLI entry point
├── requirements.txt          # Package dependencies
└── README.md                 # Project documentation
```

---

## Installation & Quickstart

### 1. Requirements & Setup
```bash
# Verify Python version (Python 3.10+)
python --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Running End-to-End Pipeline
```bash
python main.py run-pipeline --text "Sensitive Financial Ledger Payload"
```
Or via script:
```bash
python scripts/run_pipeline.py
```

### 3. Running Benchmark Evaluation Suite
```bash
python scripts/run_evaluation.py
```

### 4. Running Unit Test Suite
```bash
pytest tests/
```

---

## CLI Commands

- `extract-face`: Extract 106 facial landmark coordinates.
- `generate-key`: Derive 256-bit AES key from facial biometrics.
- `encrypt`: Encrypt plaintext payload and mine block transaction on blockchain.
- `verify`: Verify ciphertext payload integrity against on-chain metadata hash.
- `evaluate`: Run statistical randomness tests and architecture baselines.

Example:
```bash
python main.py encrypt --input "Top Secret Payload" --user-id "user_alice" --tx-id "tx_101"
python main.py verify --tx-id "tx_101" --combined-hex "<HEX_STRING>"
```

---

## Baseline Architecture Comparison

*(Reproduced via `python scripts/run_evaluation.py` over $N=3,200$ byte streams / 1,000 symbol sequences)*

| Architecture | Key Stream Entropy | Runs Test Z-Stat | Runs Test P-Value | Randomness Status |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline A** (Raw -> SHA-256) | 7.9457 (bits/byte) | 0.9244 | 0.3553 | Passed |
| **Baseline B** (Raw -> HKDF) | 7.9438 (bits/byte) | 0.6667 | 0.5050 | Passed |
| **Baseline C** (GA -> HKDF) | 7.9433 (bits/byte) | 0.4715 | 0.6373 | Passed |
| **Base Paper** (GA -> LFSR) | 7.8941 (bits/symbol) | 0.0000 | 0.0000 | Failed (Low Runs Independence) |
| **Proposed System** (GA -> LFSR -> HKDF -> AES-GCM) | **7.9405 (bits/byte)** | **-0.7466** | **0.4553** | **Passed** |

---

## Security Principles & Limitations

1. **No Direct Biometric Keys**: Facial landmark features are noisy and publicly observable. They are never directly used as AES keys.
2. **Key Derivation**: HKDF-SHA256 transforms expanded seed material into cryptographically strong 256-bit keys.
3. **Blockchain Privacy**: Only metadata hashes (`user_id_hash`, `ciphertext_hash`) are recorded on-chain.
4. **Limitation**: Without a Fuzzy Extractor / ECC helper dataset, sensor noise across distinct image captures produces distinct keys.
