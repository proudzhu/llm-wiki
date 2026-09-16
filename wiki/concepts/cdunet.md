---
type: concept
created: 2026-09-16
updated: 2026-09-16
sources:
  - raw/papers/wen-2025-neural-directed-speech-enhancement/full-text.md
tags:
  - directional-speech-enhancement
  - multi-channel
  - beamforming
  - u-net
  - low-complexity
  - causal
---

# CDUNet

**CDUNet** (causal-directed U-Net) is a dual-microphone directional speech enhancement model introduced by Wen et al. (ICASSP 2025). It integrates classical beamforming with a causal U-Net through the [[concepts/triple-steering-spatial-selection|triple-steering spatial selection method]], creating a non-linear filter that can be flexibly steered toward a target direction with a tunable enhancement region — at only 74.4K parameters and in real time.

## Architecture

CDUNet uses a convolutional U-Net encoder–decoder with skip connections:

- **Encoder**: 3 two-dimensional convolutional (Conv2D) blocks encoding the input into a latent representation.
- **Sequence modeling bottleneck**: a frequency sequence layer and an LSTM layer following the [[concepts/dprnn|DPRNN]] framework.
- **Decoder**: 3 two-dimensional transposed convolutional (ConvTrans2D) blocks; the Convolutional Block Attention Module (CBAM), combining channel and spatial attention, is applied within the decoder and on skip connections to recalibrate time-frequency feature maps.
- **Output**: the decoder-generated TF mask is applied to the **near microphone channel** — the mic closer to the target direction (channel 1 if the target angle is below 90°, else channel 2).
- **Causal**: operates streaming-compatible, targeting low-latency on-device applications.

## Inputs

- Frequency-domain representations (magnitude + phase) of the two raw microphone signals — STFT window 512, hop 256.
- Beamformer outputs at the target angle $\varphi_{target}$ and the two edge angles $\varphi_{target} \pm \varphi_{width}$ (magnitude + phase) — a 10-channel frequency-domain input in total.
- The **enhancement width** $\varphi_{width}$ (via its effect on the edge-angle steering vectors) — the first directed enhancement model to take width as an input parameter.

## Training

- **Loss**: $\mathcal{L} = \alpha_1 \sum_{i \in I} \mathcal{L}^{(i)}_{\text{MR-STFT}} + \alpha_2 \mathcal{L}_{\text{SI-SNR}}$ — SI-SNR stabilizes learning but alone over-suppresses low frequencies; the MR-STFT term mitigates this.
- **Data**: 250,000 simulated mixtures per dataset (fixed-target and variable-target) from LibriSpeech + internal corpora, dual-mic 30 mm spacing, SNR −5 to 10 dB, T60 0.2–0.5 s.

## Key Results

- Fixed target (0 dB / 5 dB): avg. PESQ 2.50 / 2.82 (fixed training) — best among DAS, GSC, JNF, U-Net, IPD U-Net, BF U-Net.
- Variable target: avg. PESQ 2.52 at 0 dB, consistent across target directions (2.47–2.60) where fixed-area U-Net collapses to 1.56.
- Downstream ASR: lowest WER at both SNRs (4.35% / 3.11% at 0 / 5 dB).
- Learns all 180 directional filters in one model with ~1400 examples per direction, versus ~250,000 for a single-direction U-Net.

## Related Concepts

- [[concepts/triple-steering-spatial-selection|Triple-Steering Spatial Selection]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter]]
- [[concepts/u-net-post-filter|U-Net Post Filter]]
- [[concepts/dprnn|DPRNN]]
- [[concepts/causality|Causality]]

## Related Sources

- [[sources/wen-2025-neural-directed-speech-enhancement|Wen et al. 2025: Neural Directed Speech Enhancement with Dual Microphone Array in High Noise Scenario]] — the introducing paper
