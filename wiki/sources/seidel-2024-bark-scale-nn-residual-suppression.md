---
type: source
created: 2026-07-17
updated: 2026-07-17
sources:
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
  - https://doi.org/10.1109/ICASSP48485.2024.10446427
  - zotero://select/items/0_QDIJS9HI
tags:
  - acoustic-echo-cancellation
  - speech-enhancement
  - residual-echo-suppression
  - noise-suppression
  - bark-scale
  - low-complexity
  - hybrid-aec
  - real-time
  - deep-learning
---

# Seidel, Mowlaee & Fingscheidt 2024: Efficient High-Performance Bark-Scale NN for Residual Echo and Noise Suppression

| Field | Value |
|-------|-------|
| **Authors** | [[entities/ernst-seidel\|Ernst Seidel]]<sup>∗</sup>, [[entities/pejman-mowlaee\|Pejman Mowlaee]]<sup>◦</sup>, [[entities/tim-fingscheidt\|Tim Fingscheidt]]<sup>∗</sup> |
| **Institution** | <sup>∗</sup>Institute for Communications Technology, Technische Universität Braunschweig, Germany; <sup>◦</sup>GN Audio A/S, Ballerup, Denmark |
| **Published** | ICASSP 2024, pp. 1–5 |
| **Type** | Conference Paper |
| **DOI** | [10.1109/ICASSP48485.2024.10446427](https://doi.org/10.1109/ICASSP48485.2024.10446427) |
| **Zotero** | [QDIJS9HI](zotero://select/items/0_QDIJS9HI) |

## Summary

This paper presents an efficient hybrid joint acoustic echo control and noise suppression system for speakerphones, consisting of a classical subband-NLMS linear echo canceller (LEC) followed by a lightweight [[concepts/nsnet2\|NSNet2]]-style neural postfilter that operates on [[concepts/bark-scale-spectral-features\|Bark-scale auditory features]]. The postfilter jointly performs residual echo suppression (RES) and noise reduction. With only **1.58M parameters** and **235 MMACs/s**, the proposed system achieves performance comparable to the end-to-end [[sources/indenbom-2023-deepvqe\|DeepVQE-S]] baseline (0.72M params, 2170 MMACs/s) on the ICASSP 2023 AEC Challenge blind test set, while requiring only about **10% of DeepVQE-S's MACs/s**. A perceptually motivated Bark-scale mapping (86 bands over 0–8 kHz) is shown to substantially improve nearend speech preservation (DT/ST Other) without sacrificing echo suppression, compared to an ablation using DFT log-power features with the same topology.

![[raw/papers/seidel-2024-bark-scale-nn-residual-suppression/figures/319183aa260b7aa69696566780d973aef79adc69ba72c68c6bb1aa50c391b4e1.jpg|Hybrid system block diagram]]
*Figure 1: Hybrid system consisting of a linear acoustic echo canceller (LEC) and the proposed neural postfilter performing residual echo and noise suppression.*

## Problem Formulation

For a speakerphone in full-duplex communication, the microphone signal is

$$
y(n) = s(n) + n(n) + d(n), \tag{1}
$$

with near-end speech $s(n)$, additive background noise $n(n)$, and echo $d(n) = h(n) * f_{\mathrm{NL}}(x(n))$, where $h(n)$ is the room impulse response and $f_{\mathrm{NL}}(\cdot)$ models loudspeaker nonlinearities. Given $y(n)$ and the far-end signal $x(n)$, the goal is to estimate $s(n)$.

The LEC produces a linear echo estimate $\hat{d}(n) = x(n) * \hat{h}(n)$, and subtraction in the DFT domain yields the LEC output:

$$
E_\ell(k) = Y_\ell(k) - X_\ell(k)\hat{H}_\ell(k). \tag{3}
$$

The neural postfilter predicts a real-valued time-frequency mask $M_\ell(k)$ applied to $E_\ell(k)$:

$$
\hat{S}_\ell(k) = M_\ell(k) E_\ell(k). \tag{4}
$$

The overall estimation error decomposes into a nearend-distortion term and a residual-noise/echo term:

$$
\epsilon_\ell(k) = (M_\ell(k)-1) S_\ell(k) + M_\ell(k)\bigl(N_\ell(k) + \Delta D_\ell(k)\bigr), \tag{6}
$$

where $\Delta D_\ell(k) = H_\ell(k) X_\ell'(k) - \hat{H}_\ell(k) X_\ell(k)$ is the residual (mostly nonlinear) echo not addressed by the LEC. The NN is trained to minimize this combined error.

## Methodology

![[raw/papers/seidel-2024-bark-scale-nn-residual-suppression/figures/abc0055b6e397e477bb12595f465194806bbfc6a4a72a328d2495513a5e0fb26.jpg|Neural network architecture of the proposed postfilter]]
*Figure 2: Neural network architecture of the proposed postfilter. The Bark-scale mapping $\mathbf{B}$ is highlighted in green. The network takes DFT power spectra of $\{E, Y, \hat{X}\}$ as inputs, projects them to 86 Bark bands, log-compresses, processes through FC/GRU layers, and projects back to the DFT domain via $\mathbf{B}^\top$ to yield the mask $M_\ell(k)$.*

### Linear Echo Canceller (LEC)

- **Filterbank**: over-sampled filterbank after Harteneck, Weiss & Stewart (1999) to minimize in-band and cross-band aliasing.
- **Adaptive algorithm**: subband [[concepts/subband-adaptive-filter\|NLMS]] with **joint optimization of normalized step-size and regularization parameters** (Ciochina et al. 2015).
- **Filter lengths**: $N_{\mathrm{LEC}} \in \{4, 8, 16, 32\}$ taps — addresses both fast and slow reactions to echo path changes.
- **Smoothing coefficient** $\beta \sim \mathcal{U}[0.5, 2]$ for PSD estimation is randomized during training for better generalization.

### Neural Postfilter (NSNet2-style on Bark features)

The architecture (Fig. 2) follows the [[concepts/nsnet2\|NSNet2]] topology (Braun & Tashev 2020) — a balance of FC and GRU layers:

1. **Perceptual feature extraction** — DFT power spectra of the three inputs $(|E_\ell(k)|^2, |Y_\ell(k)|^2, |\hat{X}_\ell(k)|^2)$ are projected to the Bark domain via the $K \times B$ mapping matrix $\mathbf{B} = (B(k,b))$:

$$
Z_\ell(b) = \sum_{k \in \mathcal{K}} B(k,b) |X_\ell(k)|^2,
$$

with the bth filter computed over its band edges $[f_{\mathrm{l}}(b), f_{\mathrm{u}}(b)]$ (Kabal 2003, PEAQ-style design):

$$
B(k,b) = \frac{\max\!\Bigl[0, \min\!\bigl(f_{\mathrm{u}}(b), \frac{(2k+1)f_s}{2K}\bigr) - \max\!\bigl(f_{\mathrm{l}}(b), \frac{(2k-1)f_s}{2K}\bigr)\Bigr]}{f_s / K}. \tag{7}
$$

2. **Log compression** — the mapped features are concatenated and log-compressed before the first FC layer.
3. **FC + GRU backbone** — NSNet2-style stack predicts a mask in the Bark domain.
4. **Inverse mapping** — the mask is projected back to DFT bins via $\mathbf{B}^\top$ to yield a real-valued DFT mask $M_\ell(k)$.

The Bark decomposition uniformly divides the 0–8 kHz range into **$B = 86$ bands** on the Bark scale.

### Loss Function: Complex Compressed MSE (CCMSE)

Training uses the [[concepts/complex-compressed-mse\|spectral complex compressed MSE (CCMSE)]] of Ephrat et al. (2018), combining magnitude-only and phase-aware terms:

$$
\begin{aligned}
J^{\mathrm{CCMSE}} = \sum_{k,\ell} &\,(1-\alpha)\bigl||\tilde{S}_\ell(k)|^c - |S_\ell(k)|^c\bigr|^2 \\
&+ \alpha\bigl||\tilde{S}_\ell(k)|^c e^{j\varphi_{\tilde{S}}(\ell,k)} - |S_\ell(k)|^c e^{j\varphi_S(\ell,k)}\bigr|^2,
\end{aligned} \tag{8}
$$

with $0 < \alpha < 1$ a weighting factor, compression exponent $c = 0.3$, and $\tilde{S}_\ell(k)$ obtained by re-applying the square-root Hann window and DFT to $\hat{s}(n)$ — the [[concepts/stft-consistency\|STFT consistency enforcement]] of Wisdom et al. (2019).

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Sampling rate** | 16 kHz |
| **Window length / DFT size / frame shift** | 1024 / $K=512$ / 128 samples |
| **LEC filter lengths $N_{\mathrm{LEC}}$** | $\{4, 8, 16, 32\}$ taps |
| **Bark bands $B$** | 86 (0–8 kHz, uniformly spaced on Bark scale) |
| **Training set** | Microsoft AEC Challenge 2023 (50,000 recordings / 10,000 environments) |
| **Noise data** | ICASSP 2023 DNS Challenge training set |
| **SNR** | $\sim \mathcal{U}[0, 30]$ dB |
| **SER** | $\sim \mathcal{U}[-30, 10]$ dB |
| **Loudspeaker nonlinearity** | 80% of files: $\eta^{-1}\mathrm{erfc}(\eta \cdot x)$ or scaled negative half-wave ($\eta \sim \mathcal{U}[-12, 0]$ dB) |
| **Clock drift** | 1% of nominal sampling rate |
| **RIR augmentation** | Cross-fading between two RIRs; dynamic direct-path gain ($\sigma = 1.0$) |
| **Optimizer** | Adam (default config) |
| **Learning rate** | $10^{-4}$, ×0.5 on plateau (patience 10) |
| **Epochs** | 400 (95,000 sequences per epoch) |
| **Test set** | ICASSP 2023 AEC Challenge blind test set (800 clips: 300 DT, 300 STFE, 200 STNE), with offline delay compensation |

### Reference Methods

| Label | Method | Description |
|-------|--------|-------------|
| LEC | Subband NLMS only | Linear stage alone |
| DTLN | [[concepts/dtln\|DTLN]] (Westhausen & Meyer 2021) | 4 LSTM layers (256 units each) + FC sigmoid; fully data-driven |
| DVQE-S | [[sources/indenbom-2023-deepvqe\|DeepVQE-S]] (Indenbom 2023) | SOTA deployed in Microsoft Teams |
| Ours (DFT) | Proposed topology, **DFT log-power features** (no Bark mapping) | Ablation isolating the Bark-mapping contribution |

### Evaluation Metrics

- **AECMOS** (Purin et al. 2022): non-intrusive echo-cancellation quality predictor, reported as DT Echo / DT Other / ST Echo / ST Other.
- **ERLE** (logarithmic echo return loss enhancement): $\mathrm{ERLE} = 10\log_{10}(\|y\|_2^2 / \|\hat{s}\|_2^2)$, STFE condition.
- **DNSMOS** (P.835): SIG / BAK / OVRL on STNE condition.

## Results

### Echo Return Loss Enhancement (Table 1, STFE)

| Method | LEC | **Ours (Bark)** | Ours (DFT) | DVQE-S | DTLN |
|--------|----:|----------------:|-----------:|-------:|-----:|
| ERLE (dB) | 37.57 | **60.10** | 62.00 | 40.00 | 68.78 |

The proposed postfilter dramatically improves ERLE over the LEC alone (+22.5 dB). DTLN achieves the highest ERLE, followed by the two proposed variants (DFT and Bark, which score comparably on ERLE despite their performance differences on AECMOS). DVQE-S scores significantly lower on ERLE than the proposed model despite a comparable ST Echo score — explained by the fact that AECMOS may overlook noise-like residual echo that ERLE still punishes.

### Efficiency Analysis (Table 2)

| Attribute | **Ours (Bark)** | Ours (STFT) | DVQE-S | DTLN |
|-----------|----------------:|------------:|-------:|-----:|
| Params (M) | 1.58 | 2.04 | **0.72** | 3.16 |
| MACs/s (M) | **235** | 240 | 2170 | 408 |
| RTF (%) | 0.22 | 0.23 | **0.20** | 0.97 |

> Measured on Intel i9-10850K @ 3.60 GHz. Bold = lowest demand; underline = second best.

**Key efficiency findings**:
- The proposed Bark model requires only **~10% of DVQE-S's MACs/s** (235M vs 2170M) while achieving comparable performance.
- DVQE-S has the lowest parameter count and RTF, but its convolutional architecture demands ~9× more MACs/s.
- The fully-connected proposed model is **much easier to implement efficiently on a speakerphone DSP** than convolutional architectures.
- Both proposed variants and DVQE-S are realtime-capable (RTF ≪ 1); DTLN is borderline (RTF 0.97).

### AECMOS / DNSMOS (Fig. 3)

AECMOS and DNSMOS scores are reported graphically in Figure 3 (not as a numeric table). Key qualitative findings from the figure:

1. **(a)** LEC scores highest on DT Other (near-end quality in double-talk) — expected, since LEC does not distort nearend speech.
2. **(b)** The Bark-scale mapping dramatically improves DT/ST Other (nearend speech preservation) over the DFT-feature ablation.
3. **(c)** In STNE, the proposed model shows no SIG degradation vs LEC and **(d)** achieves the highest OVRL score.
4. **(e), (f)** For double-talk, the proposed Bark model offers the highest DT Other among NN models, at the expense of a slightly reduced (but still high) DT Echo — a favorable trade-off for speakerphone use.
5. **(g), (h)** The DFT-feature reference model achieves good echo removal but noticeably worse nearend speech quality in both DT and STNE conditions — confirming the perceptual value of the Bark mapping.

### Discrepancy with Cited Values in Later Work

> **Note**: The later [[sources/li-2025-echofree-neural-aec\|EchoFree (Li et al. 2025)]] paper cites "Bark-AEC (Seidel et al. ICASSP 2024)" with **1.62M params / 107 MMACs/s / 100 Bark bands** and AECMOS scores (ST FE 3.16, ST NE 2.83, DT 2.96, DT Deg 3.27). The present (original) paper reports **1.58M params / 235 MMACs/s / 86 Bark bands** for its own model, and reports AECMOS only graphically. The discrepancy is likely due to different counting methodologies (e.g., inclusion/exclusion of the LEC, the mapping matrix $\mathbf{B}$, or different MACs/s measurement protocols) or possibly a different model variant. The values from the original paper are used in this source page.

## Key Contributions

1. **Efficient high-performance hybrid AEC+NS for speakerphones**: A classical subband-NLMS LEC cascaded with an NSNet2-style FC+GRU neural postfilter, achieving SOTA-comparable performance at ~10% of DeepVQE-S's compute (235 MMACs/s vs 2170 MMACs/s).
2. **Perceptually motivated Bark-scale input mapping for the postfilter**: An 86-band Bark filterbank $\mathbf{B}$ (0–8 kHz, PEAQ-style design) is applied to the DFT power spectra before the NN, with the inverse $\mathbf{B}^\top$ used to project the mask back to the DFT domain. This is shown via ablation to substantially improve nearend speech preservation (DT/ST Other) without hurting echo suppression.
3. **Joint residual echo and noise suppression in a single postfilter**: Unlike two-stage NN approaches with separate AEC and RES modules, the proposed postfilter handles both tasks simultaneously, reducing overall footprint.
4. **Comprehensive efficiency analysis**: Detailed comparison of params, MACs/s, and RTF across LEC, DTLN, DVQE-S, and the proposed Bark/DFT variants, demonstrating that fully-connected architectures are significantly easier to deploy on speakerphone-class hardware than convolutional ones at comparable quality.
5. **Insight on ERLE vs AECMOS rank-order mismatch**: The paper observes that ERLE and ST Echo rankings diverge across methods (e.g., the proposed Bark model scores much higher ERLE than DVQE-S despite comparable ST Echo) — AECMOS, trained on subjective tests, may overlook noise-like residual echo that ERLE still punishes.

## Related Concepts

- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]]
- [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]]
- [[concepts/percepnet-style-neural-post-filter\|PercepNet-Style Neural Post Filter]]
- [[concepts/nsnet2\|NSNet2]]
- [[concepts/complex-compressed-mse\|Complex Compressed MSE (CCMSE)]]
- [[concepts/stft-consistency\|STFT Consistency]]
- [[concepts/subband-adaptive-filter\|Subband Adaptive Filter]]
- [[concepts/oversampled-filterbank\|Oversampled Filterbank]]
- [[concepts/dtln\|DTLN]]
- [[concepts/adaptive-filtering\|Adaptive Filtering]]
- [[concepts/speech-enhancement\|Speech Enhancement]]

## Related Sources

- [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023: DeepVQE]] — DeepVQE-S is the primary SOTA baseline (deployed in Microsoft Teams); the proposed model matches its performance at ~10% of the MACs/s.
- [[sources/shetu-2024-hybrid-low-complexity-aenr\|Shetu et al. 2024: Hybrid Low-Complexity AENR]] — contemporary low-complexity hybrid AEC (ULCNet-AER, 1.12M / 173M); the proposed model is a different point on the same PercepNet-style efficiency frontier.
- [[sources/li-2025-echofree-neural-aec\|Li et al. 2025: EchoFree]] — later ultra-lightweight successor on the same Bark-scale postfilter lineage; cites this work as "Bark-AEC".

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se\|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — This paper extends the low-complexity AEC frontier at 235 MMACs/s, sitting between EchoFree (30 MMACs/s) and DeepVQE-S (2170 MMACs/s) on the efficiency axis. It is a canonical instance of the PercepNet-style hybrid pattern (Strategy: shared backbone across AEC+NS, but with classical LEC front-end).
