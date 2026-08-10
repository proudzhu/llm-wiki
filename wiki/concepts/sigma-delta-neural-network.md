---
type: concept
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md
tags:
  - spiking-neural-networks
  - neuromorphic-computing
  - neural-network-architecture
  - speech-enhancement
  - low-power
---

# Sigma-Delta Neural Network (SDNN)

The sigma-delta neural network (SDNN) is a feedforward ReLU architecture adapted to neuromorphic computation via **sparse message passing (sigma-delta encoding)** and **temporal computation via axonal delays**. It is the baseline solution released with the [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] ([[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023]]), designed to run efficiently on [[concepts/loihi-2|Loihi 2]] and to demonstrate that even a simple neuromorphic-aware architecture can achieve substantial power/resource advantages over conventional baselines.

## Core Mechanisms

### Sigma-delta encoding

Sigma-delta neurons exploit temporal similarity in the data to sparsify inter-layer communication:

- **Delta encoding** transmits only changes that exceed a certain threshold — the *delta* — so temporally smooth signals generate few messages.
- **Sigma encoding** reconstructs the original signal at the receiving end by accumulating deltas.
- A **sigma-delta neuron** wraps a dynamics or non-linearity (ReLU in the N-DNS baseline) with these units.

The result is a significant reduction in synaptic computations on neuromorphic hardware, where computation is event-driven: only emitted deltas trigger synaptic operations.

### Axonal delays

The network is endowed with **learnable axonal delays** that provide short-term memory, allowing features originating at different points in time to interact. Learnable delays have been shown to increase network expressivity and performance, particularly for spatio-temporal applications such as audio denoising.

## Generality

The sigma-delta sparsification principle is **general**:

- It can be applied to any conventional ReLU-like nonlinearity.
- It can be applied to the dynamics present in typical neuromorphic neuron models (leaky integrators, resonators).
- It is one of many neuromorphic features available to N-DNS Challenge participants (alongside sparse connectivity, recurrence, synaptic plasticity, etc.).

## N-DNS Challenge Baseline Configuration

| Component | Configuration |
|-----------|---------------|
| **Encoder** | STFT of noisy audio (window 512, hop 128 → 8 ms timestep at 16 kHz) + delta encoding of STFT magnitude |
| **N-DNS network** | 3-layer feedforward sigma-delta ReLU network with axonal delays; predicts a multiplicative mask at some delay |
| **Decoder** | Combine predicted mask with delayed STFT magnitude and phase; ISTFT (same window/hop as encoder) |
| **Training** | Lava-dl (extended SLAYER surrogate-gradient backpropagation); quantization-aware (matching Loihi 2 fixed precision); loss = −SI-SNR + STFT-magnitude MSE; RADAM optimizer |

## Performance (Track 1, Intel N-DNS Validation Set)

| Metric | SDNN baseline | Microsoft NsNet2 | Intel DNS (proprietary) |
|--------|---------------|-------------------|--------------------------|
| SI-SNR (dB) | 12.50 | 11.89 | 12.71 |
| DNSMOS OVRL | 2.71 | 2.95 | 3.09 |
| Latency total (ms) | 32.036 | 20.024 | 32.036 |
| Power proxy (M-Ops/s) | **14.54** | 136.13 | — |
| PDP proxy (M-Ops) | **0.44** | 2.72 | — |
| Params (×10³) | **525** | 2,681 | 1,901 |
| Model size (KB) | **465** | 10,500 | 3,802 |

The SDNN baseline achieves NsNet2-comparable SI-SNR with **9.4× lower power proxy, 5× fewer parameters, and 22× smaller model size** — quantization-aware training (matching Loihi 2's 1–8 bit synaptic weights) accounts for much of the model-size reduction. DNSMOS OVRL is lower than NsNet2 (training targeted SI-SNR, not perceptual quality), but substantially improved over the noisy input (2.71 vs. 2.45).

## Neuromorphic Features Utilized

The SDNN baseline deliberately uses only 4 of 8 performant Loihi 2 features, leaving substantial room for improvement:

| Feature | In baseline |
|---------|-------------|
| Sparse activity | ✓ |
| Sparse connectivity | ✗ |
| Recurrence | ✗ |
| Stateful neurons | ✓ |
| Neuron temporal dynamics | ✗ |
| Synaptic plasticity | ✗ |
| Graded spikes | ✓ |
| Delay as computational element | ✓ |

## Distinction from Other SNN-SE Architectures

The SDNN baseline is a *converted-from-ANN* architecture (sigma-delta sparsification wrapped around ReLU), in contrast to *spike-native* architectures such as [[concepts/sse-net|SSE-Net]] ([[sources/liu-2026-sse-net|Liu et al. 2026]]) whose every block is designed natively for spike signals. SSE-Net reports a power proxy of 19.70 M Ops/s — comparable to the SDNN baseline's 14.54 M Ops/s — while achieving substantially higher audio quality (WB-PESQ 2.89 on VoiceBank+DEMAND), illustrating the trajectory of SNN-SE progress beyond the N-DNS Challenge baseline.

## Related Concepts

- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]]
- [[concepts/loihi-2|Loihi 2]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/nsnet2|NSNet2]] — Microsoft DNS 2022 baseline used for comparison
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge]] — introduces the SDNN as the challenge baseline
- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]] — reports SNN-SE results against the N-DNS Challenge power-proxy landscape including the SDNN baseline
