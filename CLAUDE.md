# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Execution & Benchmarking
- Run full end-to-end demo pipeline: `python main.py run-pipeline` or `python scripts/run_pipeline.py`
- Run evaluation & benchmark suite: `python main.py evaluate` or `python scripts/run_evaluation.py`
- Encrypt payload & record transaction on blockchain: `python main.py encrypt --input "Text payload"`
- Verify ciphertext integrity against blockchain: `python main.py verify --tx-id "TX_ID" --combined-hex "<HEX_STRING>"`

### Testing
- Run full test suite (set `PYTHONPATH` on PowerShell): `$env:PYTHONPATH='.'; pytest tests/`
- Run a single test file: `$env:PYTHONPATH='.'; pytest tests/test_biometric.py`
- Run a single test function: `$env:PYTHONPATH='.'; pytest tests/test_biometric.py -k test_translation_and_scale_invariance`
- Test files map 1:1 to `src/` submodules: `test_biometric.py`, `test_ga.py`, `test_lfsr.py`, `test_key_derivation.py`, `test_encryption.py`, `test_blockchain.py`, `test_evaluation.py`.

---

## High-Level Code Architecture & Pipeline Flow

The system implements a biometric-driven cryptographic key sequence generation and blockchain integrity verification architecture based on *Sannidhan et al. (Computers & Electrical Engineering, 2024)*.

```
Facial Image / Synthetic Capture
       │
       ▼
src/biometric/ (LandmarkExtractor -> FeatureNormalizer)
  - Extracts 106 2D facial landmark coordinates (x, y) (synthetic fallback available).
  - Procrustes normalization: Centroid subtraction -> RMS scale normalization -> SVD rotation alignment.
       │
       ▼
src/optimization/ (GeneticAlgorithmOptimizer)
  - 212-bit binary selection mask chromosome over normalized landmark coordinates.
  - Multi-objective fitness balancing intra-class stability, inter-class separation, Shannon entropy, and correlation penalty.
       │
       ▼
src/key_generation/ (BiometricSeedGenerator -> LFSRBitGenerator -> HKDFKeyDeriver)
  - Canonical IEEE-754 float serialization + SHA-256 seed hashing.
  - Galois LFSR bit stream expansion (or paper 8-register X0..X7 modulus-256 generator).
  - RFC 5869 HKDF-SHA256 key derivation producing 32-byte (256-bit) symmetric AES key.
       │
       ▼
src/encryption/ (AESGCMCipher)
  - Authenticated AES-256-GCM encryption returning Nonce (12 bytes), Ciphertext, and Auth Tag (16 bytes).
       │
       ▼
src/blockchain/ (Blockchain -> Transaction -> BlockchainVerifier)
  - Proof-of-Work block mining (difficulty = 2).
  - Metadata-only ledger (`user_id_hash`, `ciphertext_hash`, `encrypted_data_ref`). Raw biometrics and secret keys are NEVER stored on-chain.
  - Verifier checks candidate ciphertext SHA-256 hash against immutable block commitment to detect tampering.
       │
       ▼
src/evaluation/ (entropy, correlation, randomness, hamming_distance, biometric_stability)
  - Evaluates Shannon entropy, Pearson correlation, Runs test Z-statistic, NIST Monobit, bitwise Hamming distance, and FAR/FRR metrics.
```

### Module Responsibilities
- `src/config.py`: Centralized configuration dataclasses (`BiometricConfig`, `GAConfig`, `LFSRConfig`, `CryptographicConfig`, `BlockchainConfig`) — every stage of the pipeline is parameterized from `DEFAULT_CONFIG`/`AppConfig` rather than hardcoded constants.
- `src/pipeline.py`: Main system orchestrator (`BiometricBlockchainPipeline`) and baseline comparison engine (SHA-256, HKDF, GA-HKDF, Base Paper GA-LFSR, Proposed System). `_build_ga_training_dataset()` synthesizes a multi-subject multi-capture dataset (1 primary subject with 5 perturbed captures + 4 synthetic reference subjects) so the GA's intra-class stability and inter-class separation fitness terms are non-degenerate.
- `main.py`: Main CLI entry point.
- `scripts/`: Executable scripts (`run_pipeline.py`, `run_evaluation.py`).
- `experiments/`: 5 research Jupyter notebooks (`01_feature_analysis.ipynb` through `05_blockchain_analysis.ipynb`).
- `docs/`: `architecture.md`, `methodology.md` (algorithmic formulas per stage, including MediaPipe 468→106 landmark downsampling vs. the paper's MobileNetV2 model), `security_analysis.md`, `experiment_plan.md`.
- `results/tables/evaluation_summary.json`: Machine-readable output of `run_evaluation.py` — the source of truth for the baseline comparison numbers quoted in `README.md`.

### Notes for Future Work
- Landmark extraction uses MediaPipe Face Mesh (468 points downsampled to 106 via `np.linspace`) or a deterministic synthetic generator — not a custom-trained MobileNetV2 as in the reference paper. Keep this distinction explicit in any docs/paper text (see `src/biometric/landmark_extraction.py` docstrings).
- Stream-level randomness/entropy evaluation (`run_baseline_comparisons()`) concatenates 100 derived keys (3,200 bytes) per architecture rather than measuring a single 32-byte key, since a single key's entropy is capped at `log2(32) = 5.0` bits/byte.
- Without a fuzzy extractor/ECC helper dataset, sensor noise across distinct biometric captures produces distinct keys — this is a known limitation, not a bug (see README "Security Principles & Limitations").
