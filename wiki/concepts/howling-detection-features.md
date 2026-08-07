---
type: concept
created: 2026-08-07
updated: 2026-08-07
sources:
  - raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md
tags:
  - acoustic-howling
  - howling-detection
  - signal-processing
  - feature-engineering
---

# Howling Detection Features

**Howling detection (HD) features** are signal features computed on the microphone signal STFT to discriminate howling components from desired speech and music components. They form the core of the [[concepts/howling-detection|howling detection]] stage in [[concepts/notch-filter-based-howling-suppression|NHS]]. Each feature compares the power of an STFT time-frequency bin to a specific reference power, exploiting different properties of howling (high power, narrowband, persistence, lack of harmonics).

## Spectral Features

Spectral features operate on a single STFT frame (across frequency bins). Each compares the power at frequency $\omega_i$ to a reference power:

### Peak-to-Threshold Power Ratio (PTPR)

Reference: a fixed absolute power threshold $P_0$. Assumes desired speech/music is power-limited.

$$\mathrm{PTPR}(\omega_i, t) = 10 \log_{10} \frac{|Y(\omega_i, t)|^2}{P_0}$$

### Peak-to-Average Power Ratio (PAPR)

Reference: the average microphone signal power $\hat{P}_y(t)$. Relaxes the power-limited assumption but still requires howling to be loud relative to the desired signal — excludes early-howling detection.

$$\mathrm{PAPR}(\omega_i, t) = 10 \log_{10} \frac{|Y(\omega_i, t)|^2}{\hat{P}_y(t)}, \quad \hat{P}_y(t) = \frac{1}{M}\sum_{k=0}^{M-1} |Y(\omega_k, t)|^2$$

### Peak-to-Neighboring Power Ratio (PNPR)

Reference: the power of the $m$th neighboring frequency component. Exploits the sinusoidal (narrowband) nature of howling. The value of $m$ depends on STFT resolution and windowing.

$$\mathrm{PNPR}(\omega_i, t, m) = 10 \log_{10} \frac{|Y(\omega_i, t)|^2}{|Y(\omega_i + 2\pi m/M, t)|^2}$$

### Peak-to-Harmonic Power Ratio (PHPR)

Reference: the power of the $m$th (sub)harmonic. Exploits the fact that howling has no harmonics (in the absence of loudspeaker clipping/saturation).

$$\mathrm{PHPR}(\omega_i, t, m) = 10 \log_{10} \frac{|Y(\omega_i, t)|^2}{|Y(m\omega_i, t)|^2}$$

## Temporal Features

Temporal features operate across multiple STFT frames (along time) for a single frequency bin.

### Interframe Peak Magnitude Persistence (IPMP)

Counts how often a frequency bin is among the $C$ largest-magnitude bins over the past $\mathcal{Q}_M$ frames. Captures howling persistence. **The only normalized baseline feature** (values in $[0,1]$).

$$\mathrm{IPMP}(\omega_i, t) = \frac{\sum_{j=0}^{\mathcal{Q}_M} [\omega_i \in \mathcal{C}_\omega(t-jP)]}{\mathcal{Q}_M}$$

### Interframe Magnitude Slope Deviation (IMSD)

Measures frame-wise variation of the log-magnitude slope. Expected to approach zero for howling (constant log-magnitude growth) while being time-varying for speech/music. Computationally expensive ($O(M\mathcal{Q}_M^2)$) and **extremely sensitive to the detection threshold**, consistently performing worst in benchmarks.

## Complexity Comparison

| Feature | Type | Complexity | Normalized? |
|---------|------|:---:|:---:|
| PTPR | Spectral | $O(M)$ | No |
| PAPR | Spectral | $O(M)$ | No |
| PNPR | Spectral | $O(M)$ | No |
| PHPR | Spectral | $O(M)$ | No |
| IPMP | Temporal | $O(M\mathcal{Q}_M)$ | Yes |
| IMSD | Temporal | $O(M\mathcal{Q}_M^2)$ | No |
| [[concepts/ninosp2-transposed\|NINOS²-T]] | Temporal | $O(M\mathcal{Q}_M)$ | Yes |

## Limitations of the Baseline Features

- **Candidate-selection dependence** — all were designed to operate only on peak-picked candidate frequencies, structurally excluding early howling and ringing.
- **Threshold sensitivity** — except IPMP, none is normalized, so signal-dependent normalization is needed before thresholding, complicating deployment. IMSD is particularly fragile.
- **Power-limited assumptions** — PTPR/PAPR require howling to be loud, which contradicts early-howling detection.
- **ROC-based evaluation bias** — prior benchmarks used ROC curves on candidate sets, yielding overly optimistic performance that does not reflect the full-grid, class-imbalanced reality.

## Related Concepts

- [[concepts/howling-detection|Howling Detection]] — the problem these features solve
- [[concepts/notch-filter-based-howling-suppression|Notch-Filter-Based Howling Suppression (NHS)]] — the solution scheme using these features
- [[concepts/ninosp2-transposed|NINOS²-T]] — the proposed feature that overcomes the candidate-selection and normalization limitations
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — broader AHS context

## Related Sources

- [[sources/mounir-2025-robust-early-howling-detection-sparsity|Mounir, Bernardi & van Waterschoot 2025]] — surveys these six baseline features and benchmarks them against NINOS²-T under the full-grid PR-based evaluation
- Waterschoot & Moonen 2010, "Comparative evaluation of howling detection criteria in notch-filter-based howling suppression" (J. Audio Eng. Soc.) — the reference survey that established these features as the state-of-the-art baselines
