# Experimental Evaluation Plan

## Evaluation Objectives
1. Measure Shannon Entropy of generated keys (target: ~8.0 bits/byte for derived keys).
2. Measure Pearson correlation across keys (target: near 0 correlation).
3. Evaluate Runs Test Z-statistic (target: $|Z| < 1.96$).
4. Measure bitwise Hamming distance between keys (target: ~50% bit flip).
5. Evaluate biometric stability (Intra-person distance vs Inter-person distance).

## Executing Evaluation
To execute the complete evaluation suite:
```bash
python scripts/run_evaluation.py
```
Output files will be written to `results/tables/evaluation_summary.json`.
