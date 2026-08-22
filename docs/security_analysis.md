# Security Analysis & Threat Model

## Threat Model & Security Guarantees

### Assumptions
1. Facial biometric features are non-secret and publicly observable (e.g., via high-resolution photography).
2. Attacker has access to public blockchain records and encrypted ciphertext storage.
3. Attacker knows the system algorithms, LFSR polynomial, and GA configuration (Kerckhoffs's principle).

### Security Protections
1. **No Biometric Data on Chain**: Only cryptographic hashes of user ID and ciphertext are stored on the blockchain ledger.
2. **Authenticated Encryption**: AES-256-GCM guarantees payload confidentiality and detects any ciphertext modification via 128-bit authentication tags.
3. **Cryptographic Key Separation**: Biometric noise is processed via HKDF-SHA256, generating uniform 256-bit keys that resist direct key-recovery attacks from landmark coordinates.

### Known Limitations & Research Directions
1. **Biometric Key Reproduction**: Without a formal Fuzzy Extractor or Error-Correcting Code (ECC) helper dataset, minor biometric sensor noise between distinct image captures will produce distinct derived keys.
2. **Replay & Spoofing Risks**: The prototype does not currently incorporate active liveness detection (anti-spoofing) against 3D face masks or high-resolution photos.
