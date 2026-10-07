---
type: source
created: 2026-04-28
updated: 2026-10-07
sources:
  - raw/papers/frank-2026-low-latency-roi-beamforming/full-text.md
  - https://ieeexplore.ieee.org/abstract/document/11462987
  - zotero://select/items/0_DE8N9LJ7
tags:
  - beamforming
  - wearable-audio
  - smart-glasses
  - low-latency
  - roi-beamforming
  - time-domain
  - stft
---

# Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses

**Authors**: [[entities/ariel-frank|Ariel Frank]], [[entities/israel-cohen|Israel Cohen]]
**Institution**: Andrew and Erna Viterbi Faculty of Electrical and Computer Engineering, Technion — Israel Institute of Technology, Haifa
**Year**: 2026
**Type**: Conference Paper
**Venue**: ICASSP 2026 — IEEE International Conference on Acoustics, Speech and Signal Processing, pp. 14727–14731
**DOI**: [10.1109/ICASSP55912.2026.11462987](https://doi.org/10.1109/ICASSP55912.2026.11462987)
**Zotero**: [DE8N9LJ7](zotero://select/items/0_DE8N9LJ7)

## Summary

This paper presents a head-to-head comparison of time-domain and STFT-domain implementations of least-distortion maximum-gain (LDMG) region-of-interest (ROI) beamformers for smart glasses. A unified formulation subsumes both implementations, makes their modeling approximations explicit, and enables a fair, streaming-aware comparison. Using real multichannel recordings from a 6-microphone smart-glasses platform, the authors show that the time-domain implementation delivers higher performance (directivity factor, white noise gain, own-voice reduction) with 2× lower algorithmic latency, at the cost of increased computation.

## Problem Formulation

Smart glasses with integrated microphone arrays need low-latency, low-power spatial filtering on resource-constrained hardware. Even tens of milliseconds of algorithmic latency can disrupt lip-sync and conversational turn-taking, while compute and memory budgets are bounded by thermal and battery limits. [[concepts/roi-beamforming|ROI beamforming]] is well-suited: rather than preserving a single direction of arrival (DOA), it preserves signals from a spatial region while suppressing sounds from elsewhere, accommodating DOA uncertainty due to head motion, moving or switching sources, background noise, and reverberation. The paper asks: which domain — time or STFT — better serves ROI beamforming for smart-glasses front ends?

### Signal Model

A desired source $x(t)$ is recorded by $M$ microphones. The signal at microphone $m$ contains the source filtered by the acoustic response $g_m(t)$ (including reflections from the wearer) plus noise $v_m(t)$:

$$
y_m(t) = g_m(t) * x(t) + v_m(t) = d_m(t) * x_1(t) + v_m(t) = x_m(t) + v_m(t), \quad m = 1, \dots, M
$$

where $d_m(t)$ is a noncausal infinite impulse response filter relative to Microphone 1. The objective is to estimate $x_1(t)$ from $\{y_m(t)\}_{m=1}^{M}$.

Two ROI beamforming approaches were proposed in 2025 — a time-domain implementation (Frank & Cohen, IEEE/ACM TASLP 2025) and an STFT-domain implementation (Itzhak & Cohen, IEEE/ACM TASLP 2025). Each starts from the signal model but adopts a different approximation:

- **STFT-domain**: Under the multiplicative transfer function (MTF) approximation, $x_m(k, r) = d_m(k)\, x_1(k, r)$ with a complex scalar $d_m(k)$ per frequency bin. The steering vector $\mathbf{d}(k)$ has length $M$. Without MTF, $x_m(k,r)$ depends on neighboring frequency/time bins; neglecting these terms yields a suboptimal estimate.
- **Time-domain**: Each $d_m(t)$ is approximated by a noncausal FIR filter of length $L_d$ with $\Delta$ noncausal coefficients. The observation vector has length $M L_y$ (frame of $L_y$ samples per channel) and the time-domain steering matrix $\mathbf{D}$ is $M L_y \times L$ with $L = L_d + L_y - 1$.

### Unified ROI Formulation

The noisy signal is filtered by $\mathbf{h}$ — a real spatiotemporal filter of length $M L_y$ (time) or a complex spatial filter of length $M$ per bin (STFT):

$$
z = \mathbf{h}^H \mathbf{y} = x_{\mathrm{fd}} + v_{\mathrm{rn}}
$$

A distortionless response requires $x_{\mathrm{fd}} = x_1$. In the STFT domain this gives $\mathbf{h}^H(k)\, \mathbf{d}(k) = 1$; in the time domain any element of the desired-signal vector may be targeted, $\mathbf{h}^T \mathbf{D} = \mathbf{i}_l^T$. The practical choice is the frame center, $l = \Delta + \lfloor L_y/2 \rfloor + 1$, yielding a latency of $\lfloor L_y/2 \rfloor$ samples — half the STFT latency of $L_y$ samples (the STFT must accumulate a full frame to compute its spectrum).

Because the source may lie anywhere in the ROI $\Omega$ (a set of polar/azimuthal angles), the beamformer minimizes the **average distortion** across the ROI, which has a unified expression for both implementations:

$$
J_{\mathrm{d},\Omega} = \mathbf{h}^H \boldsymbol{\Gamma}_{\Omega} \mathbf{h} - \mathbf{h}^H \mathbf{d}_{\Omega} - \mathbf{d}_{\Omega}^H \mathbf{h} + 1
$$

where $\mathbf{d}_{\Omega}$ and $\boldsymbol{\Gamma}_{\Omega}$ are the ROI averages of the steering vector/matrix and its outer product, respectively. Minimizing yields the **minimum-distortion constraint** $\boldsymbol{\Gamma}_{\Omega} \mathbf{h} = \mathbf{d}_{\Omega}$.

### Optimal Beamforming (LDMG)

Both implementations maximize the average array gain over the ROI,

$$
\mathcal{G}_{\Omega} = \frac{\mathbf{h}^H \boldsymbol{\Gamma}_{\Omega} \mathbf{h}}{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{v}} \mathbf{h}},
$$

subject to the minimum-distortion constraint. The problem is solved via generalized eigenvalue decomposition of $\boldsymbol{\Gamma}_{\mathbf{v}}^{-1} \boldsymbol{\Gamma}_{\Omega}$, with robustness parameters $K$ (number of eigenvectors retained) and $\mu \geq 0$ (regularization):

$$
\mathbf{h}_{K,\mu} = \left[ \sum_{p=1}^{K} \frac{\mathbf{t}_p \mathbf{t}_p^H}{\lambda_p + \mu} \right] \mathbf{d}_{\Omega}
$$

A final normalization $\mathbf{h} = \mathbf{h}_{K,\mu} / \sqrt{\mathbf{h}_{K,\mu}^H \boldsymbol{\Gamma}_{\Omega} \mathbf{h}_{K,\mu}}$ enforces an average desired-signal reduction factor of 1. Decreasing $K$ and increasing $\mu$ improve array gain but degrade distortion.

## Experimental Setup

### Recording Campaign

- **Hardware**: Smart glasses with $M = 6$ microphones worn by a manikin
- **Environment**: Anechoic chamber; manikin on a rotating podium completing a 360° azimuthal revolution in 10.4 minutes at elevation $\theta = 0°$
- **Excitation**: Stationary broadband white noise from a loudspeaker across from the manikin
- **Sampling**: 16 kHz; recording spatial resolution of 1° (frames within $\phi \pm 0.5°$)
- **ROI**: Azimuths $\phi \in [-5°, 5°]$ in front of the glasses

### Parameter Estimation

Per-direction steering statistics are estimated from the rotating recordings, then averaged over the ROI (per-direction estimation first, because the empirical variance of $x_1$ changes with loudspeaker direction).

- **STFT**: Hamming synthesis window of length $L_y$ with the corresponding biorthogonal analysis window, 75% overlap
- **Time domain**: $L = 2 L_y - 1$ and $\Delta = \lceil L_y/2 \rceil - 1$, with estimation hops of $0.25 L_y$ to match the STFT's data usage

Diagonal loading $\boldsymbol{\Gamma}_{\mathbf{v}} \leftarrow 0.99\, \boldsymbol{\Gamma}_{\mathbf{v}} + 0.01\, \mathbf{I}$ ensures $\boldsymbol{\Gamma}_{\mathbf{v}}$ is well conditioned.

### Three Beamformer Types

| Beamformer | Noise covariance $\boldsymbol{\Gamma}_{\mathbf{v}}$ | Optimization goal |
|------------|-----------------------------------------------------|-------------------|
| Maximum DF | Averaged over 360° azimuth | Maximize directivity factor (diffuse-noise attenuation) |
| Maximum WNG | Identity matrix | Maximize white noise gain (thermal-noise attenuation) |
| Maximum OV | Estimated from own-voice recordings (loudspeaker at manikin's mouth) | Maximize own-voice suppression |

Each was derived in both implementations for frame lengths $L_y \in \{16, 32, 64, 128\}$ — latencies $\{0.5, 1, 2, 4\}$ ms (time) and $\{1, 2, 4, 8\}$ ms (STFT). For a fair comparison, $K$ and $\mu$ were tuned so that every beamformer's SI-SDR equaled 14.9 dB: choose the smallest $K$ whose SI-SDR exceeds 14.9 dB, then increase $\mu$ until SI-SDR reaches exactly 14.9 dB.

## Results

![[raw/papers/frank-2026-low-latency-roi-beamforming/figures/94fa50cb5f6b1d317047b7d9704b13e21ee46fba843c0b1eb0c8f4dd576a8b9e.jpg|Fig. 1]]

*Figure 1: (a) Directivity factor, (b) white noise gain, and (c) own-voice reduction factor versus frame length for ROI beamformers optimized for maximum DF (triangles), maximum WNG (squares), and maximum own-voice reduction (circles). Solid lines: time-domain; dotted lines: STFT-domain.*

### Key Findings

1. **Each beamformer is best at its own objective**: the maximum-DF beamformers have the highest DF, and analogously for WNG and own-voice reduction. All metrics increase monotonically with frame length.

2. **Time-domain wins across the board**: for every noise field and every frame length, the time-domain implementation achieves higher DF, WNG, and own-voice reduction than the STFT-domain implementation — while also halving the latency.

3. **Attribution of the advantage**: the time implementation filters the waveform directly (spatiotemporal filtering), whereas the STFT implementation relies on the MTF approximation, which is inaccurate when the frame length is shorter than the effective support of the relative impulse responses.

4. **Latency vs complexity trade-off**:

| Frame length $L_y$ | Time latency | STFT latency | Time complexity | STFT complexity |
|--------------------|--------------|--------------|-----------------|-----------------|
| 16 | 0.5 ms | 1 ms | $M L_y^2$ real mults | $\mathcal{O}(M L_y \log_2 L_y)$ |
| 32 | 1 ms | 2 ms | $M L_y^2$ | $\mathcal{O}(M L_y \log_2 L_y)$ |
| 64 | 2 ms | 4 ms | $M L_y^2$ | $\mathcal{O}(M L_y \log_2 L_y)$ |
| 128 | 4 ms | 8 ms | $M L_y^2$ | $\mathcal{O}(M L_y \log_2 L_y)$ |

The STFT cost decomposes per frame into analysis windowing ($M L_y$), $M$ FFTs (each $\frac{L_y}{2}[\log_2(L_y) - 3] + 2$ real multiplications), per-bin beamforming ($4M(\lfloor L_y/2 \rfloor + 1)$), one inverse FFT, and synthesis windowing — repeated $\frac{R}{100-R}$ times per $L_y$ samples at $R$% overlap. The time-domain cost of $M L_y^2$ real multiplications per $L_y$ output samples is higher, but acceptable when modest additional on-device compute is available.

## Key Contributions

1. **Unified formulation** spanning time- and STFT-domain LDMG ROI beamformers, making each domain's modeling approximations (noncausal FIR vs MTF), latency, and real-time complexity explicit.
2. **Real-world evaluation** on multichannel smart-glasses recordings (anechoic manikin rotation campaign), not simulations.
3. **Latency-complexity-performance guidance**: when low latency is critical and modest additional on-device computing power is available, time-domain ROI beamforming is the preferred choice for smart-glasses front ends.

## Related Concepts

- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/signal-processing|Signal Processing]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Entities

- [[entities/ariel-frank|Ariel Frank]]
- [[entities/israel-cohen|Israel Cohen]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — appears in the application-driven architecture comparison (smart glasses → time-domain ROI beamforming)
