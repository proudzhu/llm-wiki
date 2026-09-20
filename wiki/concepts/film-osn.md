---
type: concept
created: 2026-09-20
updated: 2026-09-20
sources:
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - neural-directional-filtering
  - hearing-aids
  - low-latency
  - binaural
  - deep-learning
  - state-space-model
---

# FiLM-OSN

**FiLM-OSN** (FiLM-OnlineSpatialNet) is a low-latency neural directional filtering architecture introduced by [[entities/lennart-uphaus|Uphaus]] et al. (2026) for binaural speech enhancement in behind-the-ear (BTE) hearing aids. It extends the **OnlineSpatialNet (OSN)** (Quan & Li 2024) — a causal multi-channel speech enhancement network built from interleaved cross-band and narrow-band blocks with a [[concepts/mamba|Mamba]] state-space sequence model — with a [[concepts/film-layer|FiLM]] conditioning layer that steers the directivity pattern at inference, achieving a **10 ms total latency** (8 ms STFT window + 2 ms hop) where prior [[concepts/neural-directional-filtering|NDF]] approaches require 40–50 ms.

## Architecture

- **Input**: concatenated real/imaginary STFT coefficients of $Q=4$ BTE microphones ($2Q=8$ features per TF bin), $\sqrt{\mathrm{Hann}}$ window 8 ms / hop 2 ms.
- **Conditioning**: a 72-dimensional directivity-pattern vector (sampled at 5° intervals) is linearly mapped to the channel dimension $C=96$ by the FiLM layer, conditioning the narrow-band blocks toward the desired pattern.
- **Core**: $L=4$ interleaved blocks of [cross-band block → FiLM → narrow-band block]:
  - *Cross-band block*: two frequency-convolution modules + one full-band linear module, processing spectral and spatial information independently per time frame.
  - *Narrow-band block*: a [[concepts/mamba|Mamba]] SSM + a time-convolutional module (channel width $C'=196$), processing each frequency bin independently.
- **Output**: linear layer → 2-channel complex STFT estimate → iSTFT → binaural left/right time-domain signals (the anechoic direct-path signals weighted by the directivity pattern).

Parameters: 700k (SpatialNet-small configuration with $L$ reduced for complexity; FiLM output reduced from 512 to 96 channels).

## Why OSN rather than FT-JNF for low latency

The FT-JNF backbone of earlier NDF systems (FiLM-JNF) degrades sharply when its STFT window is shortened to 8 ms (PESQ 2.10→1.72, SI-SDR 4.70→2.98 dB) because the shorter window yields lower frequency resolution and hence a shorter sequence for the spectral (wide-band) LSTM. OSN replaces the spectral LSTM with frequency convolutions and the temporal LSTM with a Mamba SSM that models long-term dependencies better — recovering baseline-level quality at 8 ms windows (PESQ 2.06, SI-SDR 5.72 dB with the IPD loss) with fewer parameters.

## Losses

Trained with batch-aggregated normalized $\mathcal{L}_1$ plus the [[concepts/ipd-preservation-loss|IPD preservation loss]] ($\alpha=0.03$). The IPD term is essential: with $\mathcal{L}_1$ alone the network achieves strong quality metrics but entirely disregards the conditioned directivity pattern and the cross-channel spectral coherence; with the IPD term, the estimated pattern and coherence align with the target while ITD is preserved in both cases.

## Key Findings (Uphaus et al. 2026)

- Matches the relaxed-latency (32 ms) FiLM-JNF baseline on PESQ while exceeding it on ESTOI (0.77 vs 0.74) and SI-SDR (5.72 vs 4.70 dB), at 10 ms latency and 700k vs 950k parameters.
- Generalizes across head geometries: trained and tested on disjoint sets of hearing-aid-related transfer functions (HARTFs) covering different head diameters and BTE placements.
- Handles hearing-device-specific constraints: head shadow, varying microphone positions, and reduction (not elimination) of interferers for spatial awareness.

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/mamba|Mamba]]
- [[concepts/ipd-preservation-loss|IPD Preservation Loss]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — the introducing paper
