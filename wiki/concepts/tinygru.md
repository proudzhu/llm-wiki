---
type: concept
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/pandey-2025-ultra-low-compute/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - low-compute
  - deep-learning
---

# TinyGRU (TGRU)

**TinyGRU (TGRU)** is an ultra-low-compute DNN for complex spectral masking of multichannel speech, introduced by [[entities/ashutosh-pandey|Ashutosh Pandey]] and [[entities/juan-azcarreta|Juan Azcarreta]] (Meta Reality Labs) in [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025]]. It targets edge devices (smart glasses, hearables) where the entire enhancement pipeline must run causally, on-device, within tens of MMACs per second.

## Architecture

TGRU decouples spatial and temporal processing into two low-compute blocks:

1. **[[concepts/spatial-convolution|Spatial convolution block]]** — a stack of MIMO per-frequency convolution layers that mimics a frequency-domain filter-and-sum beamformer in the real domain. Input is the multichannel STFT with real/imaginary parts concatenated (2C real channels). The reference implementation for 8 channels uses 4 layers (input channels 16, 8, 4, 2 → output 8, 4, 2, 1), each followed by PReLU; the first layer's output is normalized frame-wise (mean/variance over channel and frequency), which together with the masking approach renders the model **scale-invariant**. The single-channel spatial output is combined with linear-transformed [[concepts/erb-scale|ERB]] features of the reference microphone.
2. **[[concepts/splitgru|SplitGRU]] temporal block** — 3 layers with hidden size 96 and split factor 2, providing causal recurrence at $1/R$ the compute of a full-width GRU. A final linear layer projects to $2F$, split into real/imaginary components of a complex mask.

The mask is applied with the simplified complex multiplication (real and imaginary parts multiplied separately), which is cheaper than full complex multiplication with equivalent performance.

## TGRU + MCWF + TGRU Framework

TGRU is deployed in a two-stage hybrid pipeline:

- **Stage 1**: TGRU estimates the enhanced complex spectrum $\hat{\mathbf{S}}_r$ at the reference microphone, which drives closed-form [[concepts/multi-channel-wiener-filter|MCWF]] weight computation via online cumulative covariances and Sherman-Morrison-Woodbury $\mathcal{O}(N^2)$ inversion.
- **Stage 2**: a second TGRU (identical structure, separate weights, stage-1 frozen) refines the beamformed output via complex masking, taking the concatenation of the MCWF output and the noisy multichannel input.

Training uses a time-domain SNR loss in two phases (stage 1 from scratch, then stage 2 with stage 1 frozen) rather than the iterative mask-then-re-estimate alternation of earlier hybrid studies.

## Performance

On a simulated 8-microphone array with DNS Challenge data (SNR [−10, 10] dB), the two-stage framework reaches STOI 78.9 / NB-PESQ 2.38 / SNR 8.7 dB at 50 MMACs/s and 16 ms latency (304k params), and STOI 81.7 / NB-PESQ 2.55 / SNR 9.7 dB at 54 MMACs/s and 32 ms latency (625k params) — outperforming the oracle [[concepts/mvdr-beamformer|MVDR]] beamformer and the [[concepts/gtcrn|GTCRN]] baseline while beating oracle MCWF in PESQ.

A key empirical finding: complex ratio masking only outperforms magnitude masking **once the MCWF is in the loop** — the spatial information provided by the MCWF enables more precise phase estimation. Conversely, magnitude-only ERB models (MC-CRN) degrade when paired with MCWF.

TGRU also serves as a comparison baseline in later work, e.g., [[concepts/neuralpmwf|NeuralPMWF]] (Grinstein et al. 2025), where the "TinyGRU+MWF" hybrid is one of the comparably-sized baselines beaten on all metrics in a 5-mic smart-glasses simulation.

## Related Concepts

- [[concepts/spatial-convolution|Spatial Convolution]] — the trainable per-frequency spatial processing block
- [[concepts/splitgru|SplitGRU]] — the compute-efficient recurrent temporal processing
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the DNN-guided spatial filter
- [[concepts/complex-ratio-mask|Complex Ratio Mask]] — the masking formulation
- [[concepts/gtcrn|GTCRN]] — the low-compute baseline family it compares against
- [[concepts/erb-scale|ERB Scale]] — the input feature compression

## Related Sources

- [[sources/pandey-2025-ultra-low-compute|Pandey & Azcarreta 2025: Ultra Low-Compute Complex Spectral Masking for Multichannel Speech Enhancement]]
