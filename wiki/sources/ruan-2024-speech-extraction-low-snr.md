---
type: source
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md
  - https://doi.org/10.1016/j.apacoust.2024.110149
  - zotero://select/items/0_N9UGYX3K
tags:
  - blind-source-extraction
  - independent-vector-extraction
  - ogive
  - natural-gradient
  - speech-enhancement
  - low-snr
  - convergence-analysis
---

# Ruan, Liao, Chen & Lu 2024: Speech Extraction Under Extremely Low SNR Conditions

**Authors**: [[entities/haoxin-ruan|Haoxin Ruan]], [[entities/lele-liao|Lele Liao]] (co-first authors), [[entities/kai-chen|Kai Chen]], [[entities/jing-lu|Jing Lu]] (corresponding)
**Institution**: Key Laboratory of Modern Acoustics, Nanjing University; NJU-Horizon Intelligent Audio Lab, Horizon Robotics
**Venue**: Applied Acoustics (journal article), 2024, Art. 110149
**DOI**: [10.1016/j.apacoust.2024.110149](https://doi.org/10.1016/j.apacoust.2024.110149)
**Funding**: NSFC Grant No. 12274221
**Audio samples**: <https://github.com/hxruan-cpp/lowSNR-audio-samples>

## Summary

This paper tackles blind extraction of a speech source of interest at an extremely low SNR of −20 dB, where conventional [[concepts/independent-vector-extraction|IVE]] methods (designed for −5 to 5 dB) fail. Using real speech data, the authors analyze the OGIVE cost-function landscape under different SNR conditions and confirm that optimizing the **mixing vector** $\mathbf{a}$ — not the conventional demixing vector $\mathbf{w}$ — is advantageous at extremely low SNR due to its wide, flat region of convergence. They then propose two natural-gradient variants, **OGIVEa_NG** and **OGIVEw_NG**, which replace the ordinary gradient with the [[concepts/natural-gradient|natural gradient]] to gain convergence stability and avoid matrix inversions. Experiments across anechoic/reverberant simulated rooms and real recordings show OGIVEa_NG is the best extraction algorithm in nearly all conditions, achieving performance comparable to the ILRMA separation baseline.

## Problem Formulation

Blind source extraction (BSE) in the STFT domain uses a per-frequency-bin instantaneous mixing model $\mathbf{x}_{ij} = \mathbf{A}_i \mathbf{v}_{ij}$, and seeks only the source of interest (SOI) $s_{ij} = \mathbf{w}_i^{\mathrm{H}}\mathbf{x}_{ij}$, treating the background (BG) $\mathbf{z}_{ij}$ as a nuisance (see [[concepts/blind-source-extraction|Blind Source Extraction]]). The mixing/demixing matrices are partitioned around the SOI:

$$\mathbf{A}_i = [\mathbf{a}_i\ \ \mathbf{Q}_i], \qquad \mathbf{W}_i = \begin{bmatrix}\mathbf{w}_i^{\mathrm{H}}\\ \mathbf{B}_i\end{bmatrix}$$

with the distortionless-response constraint $\mathbf{w}_i^{\mathrm{H}}\mathbf{a}_i = 1$. The log-likelihood cost combines a non-Gaussian SOI prior (normalized tanh score function, Eq. 12) with a Gaussian BG model and $\sum_i \log|\det\mathbf{W}_i|^2$. The **orthogonal constraint (OG)** links the two parameterizations via the mixture covariance $\hat{\mathbf{C}}_{\mathbf{x}}^i$:

$$\mathbf{w}_i = \frac{(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\mathbf{a}_i}{\mathbf{a}_i^{\mathrm{H}}(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\mathbf{a}_i}, \qquad \mathbf{a}_i = \frac{\hat{\mathbf{C}}_{\mathbf{x}}^i \mathbf{w}_i}{\mathbf{w}_i^{\mathrm{H}}\hat{\mathbf{C}}_{\mathbf{x}}^i \mathbf{w}_i}$$

so the cost depends on either $\{\mathbf{a}_i\}$ or $\{\mathbf{w}_i\}$ alone — the question is **which parameterization to optimize** at extremely low SNR.

## Methodology

### 1. Convergence-region analysis on real speech

For a $2\times 2$ instantaneous mixture ($\mathbf{A} = \begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix}$) of real speech and Gaussian noise at SNR ∈ {−20, 0, 20} dB, the authors plot the cost function against $\mathbf{w} = [1, w]^{\mathrm{T}}$ and $\mathbf{a} = [1, a]^{\mathrm{T}}$ (desired solution $w = a = -1$). Findings:

- **−20 dB**: the cost w.r.t. $\mathbf{a}$ is *flat and wide* near the desired solution (large region of convergence, ROC — a slightly-off solution barely hurts), while the cost w.r.t. $\mathbf{w}$ is *sharp and narrow* (hard to land accurately). Optimizing $\mathbf{a}$ is advantageous.
- **0 dB**: the two landscapes are nearly identical.
- **+20 dB**: the situation reverses — optimizing $\mathbf{w}$ is advantageous.

With sparse (non-Gaussian) interference such as competing speech, a *local optimum* appears at the BG solution $a = 1$, but its ROC remains narrow and sharp while the desired solution's ROC stays wide and flat — so mixing-vector optimization remains robust. This validates, on realistic data, the earlier synthetic-data analysis of Koldovský & Tichavský (2018).

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/ca416ce4cd7ae04b99dfda7ad6449c5d5ec6e99e11d3513c7319a1d1e96032f6.jpg|Cost function vs demixing parameter w at SNR = −20/0/20 dB]]

*Figure 1: Cost function w.r.t. $\mathbf{w} = [1, w]^{\mathrm{T}}$ with Gaussian noise at initial SNR = (a) −20 dB, (b) 0 dB, (c) 20 dB. Red/green dots mark the theoretical SOI/BG solutions. At −20 dB the desired peak is sharp — hard to converge to.*

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/126bea871ef7365452b9b6cc8cd70e5ad1e7964df1099d662c32f03b3a2d6d5f.jpg|Cost function vs mixing parameter a at SNR = −20/0/20 dB]]

*Figure 2: Cost function w.r.t. $\mathbf{a} = [1, a]^{\mathrm{T}}$ under the same conditions. At −20 dB the desired peak is wide and flat — the region of convergence that makes mixing-vector optimization advantageous at extremely low SNR.*

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/5134934cd8fa2720a98932f9bb4cfcaecd62b0fdec62ef866ca89910b808b87b.jpg|Cost function vs a with speech interference]]

*Figure 6: Cost function w.r.t. $\mathbf{a}$ with (highly sparse) speech interference. A local optimum appears at the BG solution $a = 1$, but its ROC is narrow while the desired solution's ROC remains wide and flat — mixing-vector optimization stays robust even under severe deviation from the Gaussian BG assumption.*

### 2. Natural-gradient OGIVE algorithms (OGIVEw_NG, OGIVEa_NG)

The parameter space of nonsingular $\mathbf{W}_i$/$\mathbf{A}_i$ is a Riemannian manifold, where the ordinary (Euclidean) gradient does not point along the steepest ascent. Rewriting the OGIVEw/OGIVEa ordinary-gradient updates (Eqs. 10, 13) in matrix form and left-multiplying by $\mathbf{W}_i^{\mathrm{H}}\mathbf{W}_i$ resp. $\mathbf{A}_i\mathbf{A}_i^{\mathrm{H}}$ yields the [[concepts/natural-gradient|natural gradient]] update rules:

$$\Delta\mathbf{w}_i = \mathbf{w}_i - \frac{1}{J}\mathbf{W}_i^{\mathrm{H}}\mathbf{W}_i \sum_j \mathbf{x}_{ij}\varphi_i(\mathbf{s}_j), \qquad \Delta\mathbf{a}_i = \mathbf{a}_i - \frac{1}{J}\lambda(\mathbf{a}_i)\mathbf{A}_i\mathbf{A}_i^{\mathrm{H}}(\hat{\mathbf{C}}_{\mathbf{x}}^i)^{-1}\sum_j \mathbf{x}_{ij}\varphi_i(\mathbf{s}_j)$$

The score function is normalized each iteration so the stationary condition $J^{-1}\sum_j s_{ij}\varphi_i(\mathbf{s}_j) = 1$ holds. Compared with ordinary-gradient OGIVE, the natural-gradient versions **avoid matrix-inversion operations**, improving both computational efficiency and stability. See [[concepts/ogive|OGIVE]] for the variant family.

## Experimental Setup

| Item | Setting |
|------|---------|
| Array | 2 microphones, 2.5 cm spacing; SNR set to **−20 dB** at reference mic |
| Rooms (simulated) | RIR-Generator; walls 6–10 m, ceiling 2.8–4.5 m; $T_{60}$ ∈ {0, 200, 500, 800} ms; source distance 1–2 m (anechoic) or $d_{\mathrm{crit}}$ to $d_{\mathrm{crit}}+1$ m (reverberant); incident angle 45°–180° |
| Real recordings | Real room, $T_{60}$ > 500 ms; noise at 90°, 2.0 m; target at 45°, 1.5 m; 30 mixtures |
| Target speech | TIMIT (simulated), VCC 2016 (real); 10 s, 16 kHz, silence-trimmed |
| Noise | Gaussian white; DEMAND 'PSTATION', 'OMEETING', 'PCAFETER', 'STRAFFIC'; TIMIT competing speech |
| STFT | 2048-point Hann, 3/4 overlap |
| Preprocessing | Frequency-domain WPE dereverberation (reverberant cases), sub-band-variable filter length |
| Baselines | AuxIVA, ILRMA (separation; best-SDRimp output oracle-selected, for reference only); OGIVEa, OGIVEw (extraction) |
| Iterations / trials | 500 iterations; 30 trials per condition |
| Metrics | SDRimp, STOI, PESQ |

Note: back-projection amplitude adjustment was *removed* from AuxIVA/ILRMA because it degrades their performance at −20 dB SNR.

## Results

**Gaussian noise (Table 1)**: OGIVEa_NG is best on nearly all metrics/reverberations — SDRimp 46.46 dB (anechoic), 26.41 dB (200 ms), 18.81 dB (500 ms), 15.80 dB (800 ms). OGIVEw/OGIVEw_NG fail (negative output SDRs — they extract the dominant *noise*). AuxIVA/ILRMA degrade because their Laplacian/local-Gaussian source models mismatch Gaussian noise.

| SDRimp [dB] | 0 ms | 200 ms | 500 ms | 800 ms |
|---|---|---|---|---|
| AuxIVA | 36.79 | 22.32 | 15.71 | 12.64 |
| ILRMA | 33.86 | 22.90 | 15.42 | 11.96 |
| OGIVEw | 20.06 | 18.36 | 10.86 | 7.87 |
| OGIVEa | 33.16 | 24.63 | 17.47 | 14.21 |
| OGIVEw_NG | 29.73 | 18.61 | 10.04 | 7.17 |
| **OGIVEa_NG** | **46.46** | **26.41** | **18.81** | **15.80** |

**Non-Gaussian noise (Tables 2–4, 'PSTATION'/'OMEETING'/speech)**: as the BG deviates from the Gaussian assumption, extraction performance declines progressively (OGIVE models only the SOI and treats BG as Gaussian); ILRMA — with its sophisticated NMF noise modeling — is best overall, but **OGIVEa_NG remains comparable to ILRMA** (e.g. speech interference, 200 ms: 24.11 vs 24.38 dB) and clearly the best *extraction* method. Algorithms optimizing $\mathbf{a}$ consistently beat those optimizing $\mathbf{w}$, confirming the convergence-region analysis.

**Real recordings (Table 5, 'PSTATION'/'PCAFETER'/'STRAFFIC')**: OGIVEa_NG best (SDRimp 15.66 dB, STOI 0.58, PESQ 1.35), ahead of ILRMA (15.12 dB) — with all output SDRs negative, reflecting the difficulty of the real-room −20 dB condition.

**Convergence (Fig. 9)**: OGIVEa_NG converges smoothly without performance degradation in all scenarios. OGIVEw/OGIVEw_NG tend to extract the dominant source and can *degrade below their starting point*; ordinary-gradient OGIVEa shows unstable convergence — the natural gradient fixes this.

![[raw/papers/ruan-2024-speech-extraction-low-snr/figures/bba0c5890c9d31eadb8e92ab584f674001e596b6e953b86a5832f67d95ba1d4e.jpg|Convergence curves of SDRimp for 6 algorithms in different scenarios]]

*Figure 9: Averaged SDRimp convergence over 30 samples. OGIVEa_NG (blue) converges smoothly and non-degrading; demixing-vector methods collapse toward the dominant source; ordinary-gradient OGIVEa is unstable.*

## Key Contributions

1. **Real-data validation of SNR-dependent parameter choice**: cost-function/ROC analysis on real speech (not synthetic data) confirming that optimizing the mixing vector $\mathbf{a}$ is advantageous at extremely low SNR while the demixing vector $\mathbf{w}$ is advantageous at high SNR.
2. **Natural-gradient OGIVE variants**: OGIVEw_NG and OGIVEa_NG — replacing the ordinary gradient with the natural gradient, avoiding matrix inversions and gaining convergence stability.
3. **Robustness evidence**: systematic evaluation across 4 reverberation times, 4 noise types (Gaussian → highly sparse speech interference), and real recordings at −20 dB, showing OGIVEa_NG is the strongest extraction method and comparable to ILRMA separation.
4. **Practical finding**: back-projection amplitude adjustment *hurts* separation algorithms at extremely low SNR; WPE dereverberation used as preprocessing with sub-band-variable filter lengths.

## Related Concepts

- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/ogive|OGIVE]]
- [[concepts/natural-gradient|Natural Gradient]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
