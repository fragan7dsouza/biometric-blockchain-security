# Algorithmic Methodology

## 0. Biometric Landmark Extraction
The system captures 106 2D facial landmark coordinates $P = \{(x_i, y_i)\}_{i=1}^{106}$:
- **Reference Paper Architecture (Sannidhan et al., 2024)**: Utilizes a MobileNetV2 deep neural network trained for 106-point landmark regression.
- **Prototype Implementation**: Uses Google MediaPipe Face Mesh (468 3D landmarks downsampled to 106 canonical coordinates via uniform indexing `np.linspace(0, 467, 106)`).
- **Synthetic Fallback**: When image captures are unavailable or for controlled benchmark experiments, a 106-landmark anatomical facial generator constructs reproducible subject profiles with configurable zero-mean Gaussian capture noise and rigid spatial transforms.

## 1. Biometric Landmark Normalization
Given raw 2D landmark coordinates $P = \{(x_i, y_i)\}_{i=1}^{106}$:
1. **Centroid Subtraction**:
   $$\mu = \frac{1}{N} \sum_{i=1}^N P_i, \quad P_i' = P_i - \mu$$
2. **RMS Scale Normalization**:
   $$s = \sqrt{\frac{1}{N} \sum_{i=1}^N \|P_i'\|^2}, \quad P_i'' = \frac{P_i'}{s}$$
3. **Rotation Alignment**: Align principal component vector $v_1$ to horizontal axis via SVD rotation matrix $R(-\theta)$.

## 2. Genetic Algorithm Optimization
- **Population**: $N_p = 50$ binary chromosomes $C \in \{0, 1\}^{212}$.
- **Multi-Objective Fitness**:
  $$F(C) = w_1 \cdot F_{\text{intra}} + w_2 \cdot F_{\text{inter}} + w_3 \cdot F_{\text{entropy}} - w_4 \cdot F_{\text{corr}}$$
  where $w_1 = 0.35, w_2 = 0.35, w_3 = 0.15, w_4 = 0.15$.

## 3. LFSR Pseudo-Random Expansion
- **Galois LFSR**: 32-bit register with primitive feedback polynomial $x^{32} + x^{31} + x^{29} + x^1 + 1$.
- **Base Paper Mechanism**: 8 registers $X_0 \dots X_7$ with modulus-256 addition:
  $$X_0^{(t+1)} = (X_7^{(t)} + \sum_{\text{even } i} X_i^{(t)} + t) \pmod{256}$$

## 4. Cryptographic Key Derivation (HKDF-SHA256)
Using RFC 5869:
$$\text{PRK} = \text{HMAC-SHA256}(\text{salt}, \text{IKM})$$
$$\text{OKM} = \text{HMAC-SHA256}(\text{PRK}, \text{info} \parallel 0x01) \quad (\text{length} = 32 \text{ bytes})$$

## 5. Blockchain Proof-of-Work
Find nonce $k$ such that:
$$\text{SHA256}(\text{BlockHeader}(k)) < 2^{256 - 4 \times d}$$
where $d = 2$ is difficulty.
