"""
Generates all 9 publication figures for the research paper from:
  - the actual code-verified architecture of this repository (Figures 1-6, schematic diagrams)
  - results/tables/evaluation_summary.json (Figures 7-9, data charts, freshly re-generated)

No values are invented. Diagram figures describe only components that exist in src/.
Chart figures plot only values present in evaluation_summary.json at generation time.
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIG_DIR = os.path.join(HERE, "figures")
EVAL_JSON = os.path.join(REPO_ROOT, "results", "tables", "evaluation_summary.json")

BOX_FACE = "#EAF1FB"
BOX_EDGE = "#2C3E6B"
ACCENT = "#C0392B"
TEXT_COLOR = "#1B1F23"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.edgecolor": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "text.color": TEXT_COLOR,
})


def _box(ax, xy, w, h, label, fontsize=9.5, face=BOX_FACE, edge=BOX_EDGE):
    x, y = xy
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=1.4, edgecolor=edge, facecolor=face, zorder=2,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
             fontsize=fontsize, color=TEXT_COLOR, zorder=3, wrap=True)
    return (x + w / 2, y), (x + w / 2, y + h), (x, y + h / 2), (x + w, y + h / 2)


def _arrow(ax, p1, p2, color=BOX_EDGE, style="-|>", lw=1.4, connectionstyle="arc3,rad=0.0"):
    arr = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                           color=color, linewidth=lw, zorder=1,
                           connectionstyle=connectionstyle)
    ax.add_patch(arr)


def _new_ax(figsize, xlim, ylim, title):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.set_title(title, fontsize=12.5, fontweight="bold", pad=14)
    return fig, ax


def fig1_overall_architecture():
    fig, ax = _new_ax((7.5, 9.5), (0, 6), (0, 15.5),
                       "Figure 1. Overall System Architecture")
    stages = [
        "Face Image / Synthetic\nBiometric Capture",
        "Facial Landmark Extraction\n(MediaPipe / Synthetic Fallback)",
        "Procrustes Feature\nNormalization (212-D vector)",
        "Genetic Algorithm\nFeature Selection",
        "Biometric Seed Generation\n(SHA-256)",
        "LFSR Key-Material\nExpansion",
        "HKDF-SHA256 Key\nDerivation (256-bit)",
        "AES-256-GCM Authenticated\nEncryption",
        "Blockchain Metadata Ledger\n(Proof-of-Work)",
        "Integrity Verification\n(Hash Comparison)",
    ]
    w, h, gap = 4.4, 1.05, 0.42
    top = 15.0
    centers = []
    for i, s in enumerate(stages):
        y = top - i * (h + gap)
        pts = _box(ax, (0.8, y - h), w, h, s)
        centers.append((0.8 + w / 2, y - h))
    for i in range(len(centers) - 1):
        x, y0 = centers[i]
        _arrow(ax, (x, y0), (x, y0 - gap))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig1_overall_architecture.png"), dpi=300)
    plt.close(fig)


def fig2_biometric_pipeline():
    fig, ax = _new_ax((9, 5.5), (0, 12), (0, 6),
                       "Figure 2. Biometric Processing Pipeline")
    _box(ax, (0.3, 4.2), 2.6, 1.2, "Input Image /\nSynthetic Landmarks")
    _box(ax, (3.3, 4.2), 2.8, 1.2, "MediaPipe Face Mesh\n468 landmarks\n(or synthetic fallback)")
    _box(ax, (6.5, 4.2), 2.6, 1.2, "Uniform Downsample\nnp.linspace(0,467,106)\n→ 106 landmarks (x,y)")
    _box(ax, (9.5, 4.2), 2.2, 1.2, "212-D Raw\nFeature Vector")
    _arrow(ax, (2.9, 4.8), (3.3, 4.8))
    _arrow(ax, (6.1, 4.8), (6.5, 4.8))
    _arrow(ax, (9.1, 4.8), (9.5, 4.8))

    steps = ["Centroid\nSubtraction\n(translation\ninvariance)",
             "RMS Scale\nNormalization\n(scale\ninvariance)",
             "SVD Rotation\nAlignment\n(pose\ninvariance)",
             "Bounding-Box\nScale to\n[-1, 1]"]
    xs = [0.5, 3.4, 6.3, 9.2]
    for x, s in zip(xs, steps):
        _box(ax, (x, 1.6), 2.6, 1.3, s, fontsize=9)
    for i in range(len(xs) - 1):
        _arrow(ax, (xs[i] + 2.6, 2.25), (xs[i + 1], 2.25))
    _arrow(ax, (10.6, 4.2), (10.6, 2.9), connectionstyle="arc3,rad=-0.4")
    ax.text(10.9, 3.5, "Procrustes\nNormalization", fontsize=8.5, style="italic")
    _box(ax, (3.9, 0.0), 4.4, 1.1, "Normalized 212-D Feature Vector\n(106 landmarks × 2 coordinates)",
         face="#FDECEA", edge=ACCENT)
    _arrow(ax, (1.8, 1.6), (5.5, 1.1), connectionstyle="arc3,rad=0.2")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig2_biometric_pipeline.png"), dpi=300)
    plt.close(fig)


def fig3_ga_workflow():
    fig, ax = _new_ax((7, 8.5), (0, 6), (0, 11),
                       "Figure 3. Genetic Algorithm Feature-Selection Workflow")
    _box(ax, (0.7, 9.2), 4.6, 1.1, "Initialize Population\n(50 chromosomes, 212 bits, ≥ 4 active bits)")
    _box(ax, (0.7, 7.4), 4.6, 1.1, "Evaluate Fitness\n0.35 F_intra + 0.35 F_inter + 0.15 F_entropy − 0.15 F_corr")
    _box(ax, (0.7, 5.6), 4.6, 1.1, "Elitism: carry top 2\nchromosomes unchanged")
    _box(ax, (0.7, 3.8), 4.6, 1.1, "Tournament Selection\n(tournament size = 3)")
    _box(ax, (0.7, 2.0), 4.6, 1.1, "Uniform Crossover (rate 0.8)\n+ Bit-flip Mutation (rate 0.05)")
    _box(ax, (0.7, 0.2), 4.6, 1.1, "Termination: fixed 30 generations\n→ best chromosome (65 features typical)")
    ys = [9.2, 7.4, 5.6, 3.8, 2.0]
    for y in ys:
        _arrow(ax, (3.0, y), (3.0, y - 0.7))
    _arrow(ax, (0.7, 3.0), (-0.9, 3.0))
    _arrow(ax, (-0.9, 3.0), (-0.9, 7.95))
    _arrow(ax, (-0.9, 7.95), (0.7, 7.95))
    ax.text(-1.55, 5.5, "loop until\ngenerations = 30", rotation=90, fontsize=8.5,
            style="italic", ha="center", va="center")
    ax.set_xlim(-2.3, 6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig3_ga_workflow.png"), dpi=300)
    plt.close(fig)


def fig4_key_generation_pipeline():
    fig, ax = _new_ax((10.5, 3.6), (0, 13), (0, 3.6),
                       "Figure 4. Key-Generation Pipeline")
    stages = [
        "GA-Selected\nFeatures\n(~65-D)",
        "Seed Generator\nIEEE-754 encode\n→ SHA-256\n(32-byte digest)",
        "LFSR\n32-bit Galois,\ntaps (32,31,29,1)\n→ 64 bytes",
        "HKDF-SHA256\nRFC 5869\nExtract-and-Expand",
        "256-bit AES-256\nSymmetric Key\n(32 bytes)",
    ]
    w, h = 2.2, 2.2
    xs = [0.3, 2.9, 5.5, 8.1, 10.7]
    for x, s in zip(xs, stages):
        _box(ax, (x, 0.6), w, h, s, fontsize=8.7)
    for i in range(len(xs) - 1):
        _arrow(ax, (xs[i] + w, 1.7), (xs[i + 1], 1.7))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig4_key_generation_pipeline.png"), dpi=300)
    plt.close(fig)


def fig5_encryption_blockchain_workflow():
    fig, ax = _new_ax((9.5, 7.8), (0, 12), (0, 10.2),
                       "Figure 5. Encryption and Blockchain Integrity Workflow")
    _box(ax, (0.3, 7.4), 3.0, 1.4, "Plaintext\nPayload")
    _box(ax, (3.9, 7.4), 3.4, 1.4, "AES-256-GCM Encrypt\n(12-byte nonce,\n16-byte auth tag)")
    _box(ax, (7.9, 7.4), 3.6, 1.4, "Ciphertext + Tag\n(combined bytes)")
    _arrow(ax, (3.3, 8.1), (3.9, 8.1))
    _arrow(ax, (7.3, 8.1), (7.9, 8.1))

    _box(ax, (7.9, 5.1), 3.6, 1.4, "SHA-256(ciphertext)\n→ ciphertext_hash")
    _arrow(ax, (9.7, 7.4), (9.7, 6.5))

    _box(ax, (7.9, 2.8), 3.6, 1.4, "Transaction record:\nuser_id_hash,\nciphertext_hash,\nencrypted_data_ref")
    _arrow(ax, (9.7, 5.1), (9.7, 4.2))

    _box(ax, (7.9, 0.5), 3.6, 1.4, "Blockchain Block\nProof-of-Work (difficulty=2)\nSHA-256 chained hash")
    _arrow(ax, (9.7, 2.8), (9.7, 1.9))

    _box(ax, (0.3, 0.5), 6.6, 1.4,
         "Verification: recompute SHA-256 of candidate ciphertext,\ncompare to on-chain ciphertext_hash → INTEGRITY_VERIFIED / TAMPER_DETECTED",
         face="#FDECEA", edge=ACCENT, fontsize=8.7)
    _arrow(ax, (7.9, 1.2), (6.9, 1.2))
    ax.text(5.9, 9.55, "No raw biometrics or secret keys are ever written to the ledger",
            fontsize=8.5, style="italic", ha="center")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig5_encryption_blockchain_workflow.png"), dpi=300)
    plt.close(fig)


def fig6_evaluation_architecture():
    fig, ax = _new_ax((10, 8), (0, 12), (0, 10),
                       "Figure 6. Experimental Evaluation Architecture (5-way baseline comparison)")
    _box(ax, (4.0, 8.4), 4.0, 1.1, "Normalized 212-D Features\n(shared input to all 5 paths)")
    rows = [
        ("A. SHA-256", "Raw features → SHA-256\n(direct hash, no GA/HKDF)"),
        ("B. HKDF", "Raw features → HKDF-SHA256\n(no GA)"),
        ("C. GA-HKDF", "GA-selected features → HKDF-SHA256\n(no LFSR)"),
        ("Proposed. GA-LFSR-HKDF", "GA-selected → Seed → LFSR → HKDF-SHA256\n(full chain)"),
        ("Base-Paper GA-LFSR", "GA-selected → 8-register X0..X7 LFSR\n(1287 iterations, no HKDF)"),
    ]
    y0 = 6.6
    for i, (name, desc) in enumerate(rows):
        y = y0 - i * 1.5
        _box(ax, (0.3, y), 3.2, 1.1, name, fontsize=8.8, face="#EAF1FB")
        _box(ax, (3.9, y), 5.0, 1.1, desc, fontsize=8.3)
        _arrow(ax, (3.5, y + 0.55), (3.9, y + 0.55))
        _arrow(ax, (6.0, 8.4), (1.9, y + 1.1), connectionstyle="arc3,rad=0.05")
        _box(ax, (9.2, y), 2.4, 1.1,
             "100 keys × 32 bytes\n= 3200-byte stream" if i < 4 else "1287 subsequences\n(flattened symbols)",
             fontsize=8, face="#FDECEA", edge=ACCENT)
        _arrow(ax, (8.9, y + 0.55), (9.2, y + 0.55))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig6_evaluation_architecture.png"), dpi=300)
    plt.close(fig)


def _load_eval():
    with open(EVAL_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def fig7_entropy_comparison(data):
    baselines = data["architecture_baselines"]
    names = ["Baseline_A_SHA256", "Baseline_B_HKDF", "Baseline_C_GA_HKDF", "Proposed_GA_LFSR_HKDF"]
    labels = ["A: SHA-256", "B: HKDF", "C: GA-HKDF", "Proposed:\nGA-LFSR-HKDF"]
    values = [baselines[n]["entropy_bits_per_byte"] for n in names]

    fig, ax = plt.subplots(figsize=(7.5, 5))
    bars = ax.bar(labels, values, color="#2C3E6B", width=0.55, zorder=3)
    ax.axhline(8.0, color=ACCENT, linestyle="--", linewidth=1.3, label="Theoretical maximum (8.0 bits/byte)")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.4f}", ha="center", fontsize=9)
    paper_val = baselines["Base_Paper_GA_LFSR"]["entropy_bits_per_symbol"]
    ax.text(3.85, paper_val - 0.35,
            f"Base_Paper_GA_LFSR: {paper_val:.4f}\nbits/SYMBOL (0–255 registers)\n"
            "— different unit basis, not\ndirectly comparable to the\nbits/byte values at left",
            fontsize=7.8, style="italic", ha="left",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF6E5", edgecolor="#B8860B"))
    ax.set_ylim(0, 8.6)
    ax.set_ylabel("Shannon entropy (bits per byte)")
    ax.set_title("Figure 7. Byte-Level Shannon Entropy Across Architectures\n(N = 3200-byte stream, 100 keys × 32 bytes)",
                  fontsize=11.5, fontweight="bold")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(axis="y", linestyle=":", alpha=0.5, zorder=0)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig7_entropy_comparison.png"), dpi=300)
    plt.close(fig)


def fig8_runs_test_comparison(data):
    baselines = data["architecture_baselines"]
    order = ["Baseline_A_SHA256", "Baseline_B_HKDF", "Baseline_C_GA_HKDF",
             "Proposed_GA_LFSR_HKDF", "Base_Paper_GA_LFSR"]
    labels = ["A: SHA-256", "B: HKDF", "C: GA-HKDF", "Proposed:\nGA-LFSR-HKDF", "Base-Paper\nGA-LFSR*"]
    z_values = [baselines[n]["runs_z_stat"] for n in order]
    colors = ["#2C3E6B"] * 4 + ["#8A8D91"]

    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.axhspan(-1.96, 1.96, color="#D6E4F0", alpha=0.6, zorder=0, label="Non-significant region (|Z| < 1.96)")
    bars = ax.bar(labels, z_values, color=colors, width=0.55, zorder=3)
    for b, v in zip(bars, z_values):
        ax.text(b.get_x() + b.get_width() / 2, v + (0.08 if v >= 0 else -0.18),
                f"{v:.4f}", ha="center", fontsize=9, va="bottom" if v >= 0 else "top")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Runs-test Z-statistic")
    ax.set_title("Figure 8. Wald–Wolfowitz Runs-Test Z-Statistic Comparison",
                  fontsize=12, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.grid(axis="y", linestyle=":", alpha=0.5, zorder=0)
    ax.text(4, min(z_values) - 0.9,
            "*Base-Paper_GA_LFSR's Z = 0.0 reflects a measurement-code artifact\n"
            "(the runs test assumes binary input but is fed 0–255 register symbols),\n"
            "not a verified randomness failure — see Discussion / Security Analysis.",
            fontsize=7.6, style="italic", ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF6E5", edgecolor="#B8860B"))
    ax.set_ylim(min(z_values) - 1.6, max(2.4, max(z_values) + 0.6))
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig8_runs_test_comparison.png"), dpi=300)
    plt.close(fig)


def fig9_biometric_stability(data):
    bs = data["biometric_stability"]
    fig, ax = plt.subplots(figsize=(7, 5.2))
    labels = ["Intra-subject\n(same person,\ndifferent captures)", "Inter-subject\n(different people)"]
    means = [bs["intra_mean"], bs["inter_mean"]]
    stds = [bs["intra_std"], bs["inter_std"]]
    bars = ax.bar(labels, means, yerr=stds, capsize=8, color=["#2C3E6B", "#C0392B"], width=0.5, zorder=3)
    for b, m in zip(bars, means):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.35, f"mean = {m:.4f}", ha="center", fontsize=9)
    ax.axhline(bs["threshold"], color="#B8860B", linestyle="--", linewidth=1.4,
               label=f"Decision threshold = {bs['threshold']:.2f}")
    ax.set_ylabel("Normalized Euclidean feature distance")
    ax.set_title("Figure 9. Intra-Subject vs. Inter-Subject Feature Distance\n"
                  f"(10 subjects × 5 captures; FRR = {bs['frr']:.2f}, FAR = {bs['far']:.2f})",
                  fontsize=11.5, fontweight="bold")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.grid(axis="y", linestyle=":", alpha=0.5, zorder=0)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig9_biometric_stability.png"), dpi=300)
    plt.close(fig)


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    fig1_overall_architecture()
    fig2_biometric_pipeline()
    fig3_ga_workflow()
    fig4_key_generation_pipeline()
    fig5_encryption_blockchain_workflow()
    fig6_evaluation_architecture()
    data = _load_eval()
    fig7_entropy_comparison(data)
    fig8_runs_test_comparison(data)
    fig9_biometric_stability(data)
    print("All 9 figures generated in", FIG_DIR)
    for f in sorted(os.listdir(FIG_DIR)):
        print(" -", f)


if __name__ == "__main__":
    main()
