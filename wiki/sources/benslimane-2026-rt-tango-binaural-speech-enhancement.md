---
type: source
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/full-text.md
  - https://arxiv.org/abs/2607.01834
  - https://doi.org/10.48550/arXiv.2607.01834
  - zotero://select/items/0_8ZWV2E4T
tags:
  - speech-enhancement
  - distributed
  - binaural
  - hearing-aid
  - low-latency
  - real-time
  - efficiency
  - grouped-rnn
  - erb
  - stft
---

# Benslimane, Chouteau, Poreba, Auzanneau, Szczepanski, Chersi &amp; Serizel 2026: RT-Tango

**Authors**: [[entities/zahra-benslimane|Zahra Benslimane]]¹, [[entities/pierre-chouteau|Pierre Chouteau]]¹, [[entities/martyna-poreba|Martyna Poreba]]¹, [[entities/fabrice-auzanneau|Fabrice Auzanneau]]¹, [[entities/michal-szczepanski|Michal Szczepanski]]², [[entities/fabian-chersi|Fabian Chersi]]², [[entities/romain-serizel|Romain Serizel]]²
**Affiliations**: ¹ Université Paris-Saclay, CEA, List, F-91120 Palaiseau, France; ² Université de Lorraine, CNRS, Inria, LORIA, F-54000 Nancy, France
**Venue**: arXiv preprint (INTERSPEECH 2026 submission)
**Year**: 2026
**Type**: Preprint
**DOI**: [10.48550/arXiv.2607.01834](https://doi.org/10.48550/arXiv.2607.01834)
**arXiv**: [2607.01834](https://arxiv.org/abs/2607.01834)

## Summary

This paper introduces **RT-Tango**, a real-time distributed binaural speech enhancement (SE) framework designed for streaming on resource-constrained hearing-aid platforms. RT-Tango revisits the two-stage distributed [[concepts/tango-framework|Tango]] architecture through complementary architectural and signal-processing optimizations: perceptually motivated [[concepts/erb-scale|ERB]] feature compression, lightweight [[concepts/grouped-recurrent-neural-network|grouped recurrent]] mask estimation, [[concepts/fixed-rate-skipping|temporal sparsification]], and an [[concepts/asymmetric-stft|asymmetric STFT]] that decouples spectral resolution from algorithmic latency. Its strictly causal streaming variant, RT-Tango-OS, operates at an 8 ms algorithmic latency while achieving competitive SE quality and reducing computational cost to ~35 MMACs/s — nearly six times more efficient than the GTCRN baseline under identical conditions.

## Problem Formulation

Real-time [[concepts/distributed-binaural-speech-enhancement|distributed binaural SE]] for hearing aids must jointly satisfy:

- **Strict causality and ultra-low latency** ($\leq 10$ ms algorithmic delay) to preserve lip-reading sync and conversational naturalness.
- **Low computational complexity** for low-power embedded hardware.
- **Limited inter-node communication** — microphones are distributed across physically separated ear-nodes, and centralized processing would require continuous high-bandwidth wireless transmission, infeasible under energy/bandwidth budgets.

The baseline [[concepts/tango-framework|Tango]] framework demonstrates feasibility of reduced-bandwidth distributed binaural SE but imposes no latency or complexity constraints, leaving the joint achievement of low latency and low computational complexity as an open challenge that RT-Tango addresses.

## Methodology

![[raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/figures/fig1.png|Figure 1: RT-Tango block diagram]]

*Figure 1: Block diagram of RT-Tango. It preserves Tango's two-stage processing scheme while introducing additional or modified modules focused on efficiency (highlighted in yellow) and low-latency streaming (in italics).*

RT-Tango preserves the two-stage distributed spatial filtering scheme of Tango (SN-DNN → SDW-MWF → exchange → MN-DNN → SDW-MWF) and improves efficiency through four complementary design choices:

### Feature Compression (ERB)

The [[concepts/erb-scale|ERB]]-scaled filterbank is used as the front-end for both the SN-DNN and MN-DNN. This perceptually motivated transformation reduces spectral resolution at high frequencies (where human auditory sensitivity is coarser) while preserving finer resolution at low frequencies that carry most speech energy. The estimated masks are mapped back to the linear-frequency domain via an inverse ERB transform to restore the spectral resolution required for SDW-MWF filtering.

### Grouped RNN Mask Estimation

The mask estimation networks implement a [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network (GRNN)]] that partitions the hidden state into $G$ groups, reducing recurrent complexity from $\mathcal{O}(H^{2})$ to $\mathcal{O}(H^{2}/G)$. Cross-band dependencies are captured via a representation rearrangement mechanism. Asymmetric grouping is adopted: $G=8$ for the SN-DNN (robust to grouping) and $G=2$ for the MN-DNN (sensitive to aggressive grouping).

### Temporal Sparsification

[[concepts/fixed-rate-skipping|Fixed-Rate Skipping (FRS)]] executes the mask estimator at a predefined interval and reuses the previously estimated mask in between, exploiting temporal redundancy. RT-Tango uses update rates of $1/4$ (SN-DNN) and $1/2$ (MN-DNN), corresponding to 75% and 50% frame skipping. FRS is preferred over learned skip gates (Skip RNN, TinyLSTM) which, despite ~80% effective skip ratios, introduced additional MACs and caused larger quality degradation — especially in the MN-DNN.

### Low-Latency Streaming

An [[concepts/asymmetric-stft|asymmetric STFT]] uses a long 32 ms analysis window (preserving frequency resolution) with a shorter 8 ms asymmetric Hann synthesis window (reducing reconstruction latency). The [[concepts/spatial-covariance-matrix|spatial covariance matrices (SCM)]] required by the SDW-MWF are updated online using a recursive exponential moving average (EMA) with forgetting factor $\alpha=0.995$, applied every 8 frames at the 4 ms input rate (effective update interval ≈ 32 ms, ~31 updates/s). Under these streaming constraints the system operates as **RT-Tango-OS**.

## Experimental Setup

| Item | Detail |
|------|--------|
| **Training data** | Simulated binaural dataset (Monir et al. protocol); 4-mic hearing-aid config (2 mics/ear); LibriSpeech clean speech + speech-shaped & real-world environmental noise |
| **Evaluation data** | BinauRec subset: 1,200 mixtures; measured RIRs from a portable hearing laboratory (PHL) with behind-the-ear hearing aids on a dummy head |
| **Target/noise geometry** | Target in front; noise at 45° and 90° right (lower SIR at right ear) |
| **Input SNRs** | −5, 0, 5 dB |
| **STFT** | 32 ms analysis window; 16 ms hop (grouped ablations, FRS, RT-Tango) or 4 ms hop (RT-Tango/RT-Tango-OS streaming, learned skipping, GTCRN-4ms) |
| **Loss** | MSE between estimated mask and target ideal ratio mask |
| **Optimizer** | Adam, lr = $10^{-3}$ |
| **Baselines** | Tango (CNN), Tango-RNN (causal RNN variant), [[concepts/gtcrn|GTCRN]] (per-node lightweight) |
| **Metrics** | SI-SDR, SI-SIR, SI-SAR (dB); PESQ, STOI; MACs/s and MACs/frame (DNN + SDW-MWF; FFT/iFFT excluded) |
| **Online SCM** | EMA, $\alpha=0.995$, updated every 8 frames at 4 ms rate (RT-Tango-OS only); evaluated in steady state |

## Results

### Main comparison (Table 1)

| Model | STFT Hop | Total MMACs/s | SI-SIR L/R | SI-SDR L/R | PESQ L/R |
|-------|----------|---------------|------------|------------|----------|
| Unprocessed | — | — | 0.0 / −4.0 | −0.6 / −4.6 | 1.14 / 1.10 |
| Tango | 16 ms | 605.98 | 20.8 / 24.1 | 4.2 / 4.4 | 1.61 / 1.64 |
| GTCRN | 16 ms | 48.98 | 16.1 / 14.1 | 5.6 / 3.7 | 1.47 / 1.34 |
| GTCRN | 4 ms | 197.5 | 16.6 / 13.8 | 6.0 / 4.0 | 1.52 / 1.36 |
| Tango-RNN | 16 ms | 67.20 | 21.6 / 25.0 | 4.7 / 5.0 | 1.66 / 1.70 |
| + GRNN (SN=8, MN=2) | 16 ms | 18.22 | 21.3 / 24.8 | 4.5 / 4.8 | 1.66 / 1.70 |
| **RT-Tango (ours)** | 4 ms | **33.41** | 20.8 / 24.6 | 4.4 / 4.7 | 1.66 / 1.71 |
| **RT-Tango-OS (ours)** | 4 ms | **35.14** | 20.5 / 24.7 | 2.9 / 3.8 | 1.54 / 1.63 |

### Key findings

- **~6× more efficient than GTCRN** at the same 4 ms hop (33.4 vs 197.5 MMACs/s), while achieving higher SI-SIR (20.8/24.6 vs 16.6/13.8 dB) and better interaural balance due to the two-stage mechanism.
- **18× reduction vs Tango baseline** (605.98 → 33.41 MMACs/s) despite operating at a 4× higher frame rate.
- The two-stage architecture yields **balanced left/right behavior** (desirable for stable spatial perception), unlike GTCRN which is strongly ear-asymmetric.
- Robustness to compression stems from the hybrid architecture where **neural networks guide the spatial filter** rather than directly reconstructing the signal.
- **Grouping sensitivity**: SN-DNN tolerates $G=8$ with negligible loss; MN-DNN degrades ~0.8–1 dB at $G=8$, motivating the asymmetric (SN=8, MN=2) strategy.
- **Temporal sparsification**: FRS preserves quality within 0.2 dB of baseline for both stages; learned skipping degrades MN-DNN SI-SDR from 4.5 to 3.3–3.8 dB.
- **Latency–quality trade-off**: asymmetric Hann synthesis window at 8 ms offers the best compromise; 4 ms further reduces latency but degrades quality.
- **Online SCM (RT-Tango-OS)**: SI-SIR comparable to offline, but SI-SDR/SI-SAR decrease slightly due to asymmetric STFT + online SCM; STOI/PESQ remain competitive with GTCRN at high frame rate while being far more computationally efficient.

## Key Contributions

1. A real-time distributed binaural SE framework combining ERB feature compression, grouped recurrent mask estimation, temporal sparsification, and asymmetric STFT within a single two-stage architecture.
2. Demonstration that the distributed two-stage Tango scheme can be compressed ~18× (in MACs/s) and operate at a 4× higher frame rate while preserving SE quality and interaural balance.
3. A strictly causal streaming variant (RT-Tango-OS) achieving 8 ms algorithmic latency with online recursive SCM estimation, suited to practical binaural hearing-aid deployment.
4. Systematic ablations isolating the contribution of grouping, temporal sparsification, and STFT configuration, including a comparison of fixed-rate vs. learned skipping strategies.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network (GRNN)]]
- [[concepts/fixed-rate-skipping|Fixed-Rate Skipping (FRS)]]
- [[concepts/asymmetric-stft|Asymmetric STFT]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/audio-latency|Audio Latency]]

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in ANC: From O(N²) to GPU-Accelerated DSP]]
