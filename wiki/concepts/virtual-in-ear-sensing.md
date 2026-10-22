---
type: concept
created: 2026-10-22
updated: 2026-10-22
sources:
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
tags:
  - anc
  - open-ear
  - hearables
  - deep-learning
  - virtual-sensing
---

# Virtual In-ear Sensing

**Virtual in-ear sensing** is the estimation of the acoustic signal at a user's ear canal — or of the [[concepts/active-noise-control|ANC]] control filters that map wearable-frame microphones to it — using only sensors mounted on the wearable's frame, without any physical in-ear (error) microphone. The term was introduced by Yuan, Liu & Xiao et al. (2026) for ANC on open-ear wearables, where the unoccluded ear makes a physical error sensor impossible.

## Key Idea

Open-ear devices (smart glasses, AR/VR headsets, headbands) leave the ear canal unoccluded, so conventional feedforward ANC cannot measure the residual noise that adaptive algorithms (e.g., [[concepts/filtered-x-lms-algorithm|filtered-x LMS]]) need as feedback. Virtual in-ear sensing replaces the feedback loop with a **learned feedforward mapping**: because a rigid frame fixes the spatial relationship between frame microphones and the ear, noise diffracting around the head produces correlated measurements at both, and a neural network can learn the relative transfer behavior from spatial cues (interchannel phase/level differences) — generalizing to unseen users and environments without prior acoustic measurement.

Formally, the network $f$ maps the $M$ frame microphone signals directly to the causal control filters that minimize the ear residual:

$$f(x_{1}[n],\dots,x_{M}[n])=\{w_{1}[n],\dots,w_{M}[n]\},\qquad \min \mathcal{L}=\|d[n]+\hat{s}[n]*\textstyle\sum_{m}(w_{m}[n]*x_{m}[n])\|_{1}.$$

Notably the loss optimizes the **residual at the ear** (through the estimated secondary path), not a reconstruction of the ear signal — the network learns "which filters cancel," not "what the ear signal looks like."

## Implementation (Yuan et al. 2026)

- Input features: reference-channel spectrogram (Re/Im), IPD (sin/cos), ILD — 11 channels from 4 mics per side
- U-Net encoder–decoder with squeeze-and-excitation skips and LSTM bottleneck; user-specific [[concepts/secondary-path-modeling|secondary path]] injected via a [[concepts/film-layer|FiLM]] layer (~512 bytes per user instead of retraining)
- Output: 4 × 2048-tap time-domain FIR filters per ear, refreshed every 200 ms; applied on a DSP at 113 µs end-to-end latency via [[concepts/hybrid-partitioned-convolution|hybrid partitioned convolution]]
- Result: 9.6 dB mean reduction (100–1000 Hz) with no calibration, 11.2 dB with user calibration, across 11 unseen users × 8 unseen environments — within 4.3 dB of an oracle Wiener filter that uses a physical in-ear microphone

## Relation to Prior Virtual Sensing

This is a wearable instantiation of [[concepts/virtual-sensing|virtual sensing]] and the [[concepts/remote-microphone-technique|remote microphone technique]] family: prior systems placed sensors in the environment or assumed fixed, pre-measured geometries (e.g., active headrests), confining quiet zones to bounded regions. Virtual in-ear sensing instead exploits the *on-body* fixed geometry of the wearable itself, enabling mobile operation in uncharacterized environments. It also connects to [[concepts/relative-transfer-function|relative transfer function]] estimation: the learned filters are RTFs between frame microphones and the ear.

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/hybrid-partitioned-convolution|Hybrid Partitioned Convolution]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/hearables|Hearables]]

## Related Sources

- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]]
- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective ANC Systems]] — six-microphone AR-glasses array for SSANC, same open-ear platform challenges
- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]
