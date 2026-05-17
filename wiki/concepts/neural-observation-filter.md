---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - virtual-sensing
  - deep-learning
  - anc
  - remote-microphone
  - cnn
---

# Neural Observation Filter

A **Neural Observation Filter** uses a neural network to estimate the coefficients of the observation filter $\mathbf{O}(z)$ in the **[[concepts/remote-microphone-technique|Remote Microphone Technique (RMT)]]** for virtual sensing in active noise control. Unlike conventional RMT where filters are pre-computed offline for fixed scenarios, neural observation filters estimate coefficients online, adapting to **variable virtual microphone positions** and changing acoustic conditions.

## Motivation

Traditional RMT computes observation filters during a training phase via cross-correlations or cross-spectral densities, storing them in a database indexed by acoustic scenario and virtual position. During operation, a selection mechanism chooses the appropriate filter set. This approach has several limitations:

- **Scalability**: Covering all possible acoustic scenarios and virtual positions requires an impractically large database
- **No continuous adaptation**: Filter selection is discrete; interpolating between stored filters adds complexity
- **Fixed virtual positions**: Each filter is computed for a specific virtual microphone location

## Architecture

Neural observation filters share a common architectural pattern:

### 1. Input Feature Extraction

Raw microphone signals are pre-processed into compact features before the neural network:
- **GCC-PHAT** features between all unique remote microphone pairs (phase-transformed generalized cross-correlation)
- `$R \choose 2$` GCCs for $R$ remote microphones, each cropped to the array aperture
- **Position coordinates** (e.g., 3D Cartesian coordinates of the virtual microphone) concatenated at the bottleneck

This preprocessing enables **asynchronous computation**: the feature extraction and neural inference can run on an external co-processor at a slower rate than the real-time filtering.

### 2. Neural Network

Two architectural families have been demonstrated:

- **CNN-based** (Holzmuller & Sontacchi 2025): Encoder-decoder 1D CNN with 4 compression stages, bottleneck linear layers with position concatenation, and 4 expansion stages. Outputs FIR coefficients directly. ~367k parameters, 1.34M MACs/inference.

- **Conv-TasNet-based** (Holzmuller & Sontacchi 2026, Obs-TasNet): Modified Conv-TasNet with temporal convolutional network (TCN) blocks and a learnable separation kernel. Reduces parameters by ~40% compared to CNN baseline while improving accuracy.

### 3. Asynchronous Dual-Loop Operation

```
┌─────────────────────┐    ┌─────────────────────┐
│  Low-Latency Loop   │    │  Co-Processor Loop  │
│  (Real-time DSP)    │    │  (Every ~500ms)     │
├─────────────────────┤    ├─────────────────────┤
│ ANR ├→ Filtering ──┤    │ Mic → GCC-PHAT → NN │
│ w/   │              │    │ │ inference → O(z)  │
│ Ŝ(z) ├← O(z) ──────┤    └─────────│───────────┘
│      │              │          O(z) update
│      └──→ ê(z) ───────┘
└───────┘
```
- **Low-latency filtering loop**: FIR filtering with current $\mathbf{O}(z)$ coefficients runs on dedicated DSP hardware (low latency)
- **Co-processor loop**: GCC-PHAT computation + neural inference runs on separate NPU/CPU at a slower rate (e.g., 2 Hz), updating coefficients asynchronously

## Key Advantages

- **Variable virtual position**: Position coordinates are input features, enabling arbitrary virtual microphone placement
- **No filter selection**: Single network handles all scenarios, no pre-computed database or selection logic needed
- **Acoustic adaptation**: GCC-PHAT inputs reflect the current acoustic scene, enabling implicit adaptation
- **Computational separation**: Expensive inference offloaded from the real-time audio path

## Training

Training uses synthetic data with known ground truth:
- **Loss**: MSE between predicted $\hat{d}_e[n]$ and true $d_e[n]$ primary disturbances at the virtual microphone, normalized by RMS of target signal
- **Simulated environments**: Pyroomacoustics, random source positions, colored noise sources
- **Multiple virtual positions**: Each training sample has a randomly placed virtual microphone

## Performance

- With accurate position data: −33.53 dB NMSE (CNN, Holzmuller 2025)
- Without position data: −13.42 dB NMSE (same network, same data)
- Low-frequency estimation error below −40 dB
- ~0.5-1 dB NMSE degradation per cm of virtual microphone offset from array center
- Source direction has no statistically significant impact on estimation quality

## Related Concepts

- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/neural-networks|Neural Networks]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control|Holzmuller & Sontacchi 2025: Deep Observation Filter for Virtual Sensing ANC]] — First CNN-based neural observation filter
- [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller & Sontacchi 2026: Obs-TasNet for Virtual Sensing]] — Conv-TasNet follow-up
